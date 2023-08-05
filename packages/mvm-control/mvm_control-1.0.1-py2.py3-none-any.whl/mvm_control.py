"""
Simple command line tool to access a MVM ESP32 via the serial port
There are three available commands

For help on usage type: python mvm_control.py -h

For help on command usage type: python mvm_contro.py <get/set/log> -h

Note: The log command can either output to a log file or stdout

The log format is as follows:

{
    "settings": { ... },
    "data": [
        { ... },
        { ... }
    ]
}

Where "settings" is a JSON object containing reasonable settings to store (at
the time of this writing)

Each 'data' entry contains the contents of the 'get all' command, and and an
extra parameter 'time' that is a unix timestamp of when it was received.
"""

__version__ = '1.0.1'

import serial
import time
import argparse
import sys
import json
import signal

# Choices allowed for 'get' command
choices_for_get = [
    'pressure', 'flow', 'o2', 'bpm', 'backup',
    'tidal', 'peep', 'temperature', 'power_mode',
    'battery', 'version', 'alarm', 'warning',
    'run', 'mode', 'rate', 'ratio',
    'assist_ptrigger', 'assist_flow_min',
    'ptarget', 'pressure_support', 'backup_enable', 'backup_min_rate',
    'all', 'calib', 'calibv', 'stats'
]

# Choices allowed for 'set' command
choices_for_set = [
    'run', 'mode', 'rate', 'ratio',
    'assist_ptrigger', 'assist_flow_min',
    'ptarget', 'pressure_support', 'peep',
    'pid_p', 'pid_i', 'pid_d',
    'pid_p2', 'pid_i2', 'pid_d2',
    'pause_inhale', 'pause_lg', 'pause_lg_time',
    'pause_exhale', 'pid_limit', 'alarm_snooze',
    'alarm', 'watchdog_reset', 'console',
    'timestamp', 'wdenable', 'backup_enable',
    'backup_min_rate', 'stats_clear'
]

# Verbosity option
verbose = False
rate = 10

terminate = False


def signal_handling(signum, frame):
    global terminate
    terminate = True


signal.signal(signal.SIGINT, signal_handling)


def _parse_response(response):
    """Parse a response and check if its valid from the ESP32, format is
    'valore=...'"""
    response = response.strip()  # Remove the terminator(s)
    try:
        check, value = response.decode('utf-8').split('=')
        if(check.lower() == 'valore'):
            return value
        else:
            return False
    except Exception:
        print("Error parsing response! (" + str(response) + ")")
        return False


def get_mvm_param(ser, param):
    """Request the ESP32 get the value for a given parameter and transmit it"""
    try:
        request = 'get ' + str(param) + '\r\n'
        ser.write(request.encode('utf-8'))
        response = _parse_response(ser.readline())
    except Exception as e:
        print("Error communicating with device")
        print(e)
        return False

    if(response is not False):
        if(response == 'no_data'):
            print("Invalid or unknown command")
            return False
        elif(response[0:5] == 'ERROR'):
            print(response)
            return False
        else:
            return response


def set_mvm_param(ser, param, value):
    """Request the ESP32 set a parameter to a given value"""
    try:
        request = 'set ' + str(param) + ' ' + str(value) + '\r\n'
        ser.write(request.encode('utf-8'))
        response = _parse_response(ser.readline())
    except Exception as e:
        print("Error communicating with device")
        print(e)
        return False

    try:
        if(response is not False):
            if (response.lower() == 'ok'):
                return True
            else:
                print("Bad or unknown response! (" + str(response) + ")")
                return False
        else:
            return False
    except Exception:
        print("Error parsing response! (" + str(response) + ")")
        return False


def cmd_get(args):
    """Get command wrapper"""
    result = get_mvm_param(ser, args.param)
    if result is not False:
        print(result)
    else:
        exit(-1)


def cmd_set(args):
    """Set command wrapper"""
    result = set_mvm_param(ser, args.param, args.value)
    if result is not False:
        if(verbose):
            print("Success")
    else:
        exit(-1)


def cmd_log(args):
    """Log command wrapper"""
    global terminate

    with args.logfile as log_file:
        # Step one, gather up the settings!
        settings = [
           'backup', 'power_mode', 'battery', 'version', 'alarm', 'warning',
           'run', 'mode', 'rate', 'ratio', 'assist_ptrigger',
           'assist_flow_min', 'ptarget', 'pressure_support', 'backup_enable',
           'backup_min_rate'
        ]

        # Run through the dict getting our responses
        settings_resp = {}
        for setting in settings:
            resp = get_mvm_param(ser, setting)
            if(resp is not False):
                settings_resp[setting] = resp

        # Dump out the settings to the log file
        log_file.write("{\"settings\": " + json.dumps(settings_resp))

        # Start the data portion of the log file

        log_file.write(",\"data\": [\n")
        first = True  # Used to print the ',' between entries

        while(1):
            resp = get_mvm_param(ser, 'all')
            if(resp is False):
                exit(-1)

            # Don't print the data if we are logging to standard out or not in
            # verbose mode
            if(log_file is not sys.stdout and verbose):
                print(resp)

            # Ugly, but split up the data and use some sort of name that makes
            # sense the variable names used inside the Arduino code are a bit
            # hard to parse/grok
            data_split = resp.split(',')
            log_file.write(
                '{13}{{"time": {14}, "last_pressure": {0}, '
                '"flux": {1}, "last_o2": {2}, "last_bpm": {3}, '
                '"tidalvolume": {4}, "last_peep": {5}, "temperature": {6}, '
                '"battery_powered": {7}, "current_battery_charge": {8}, '
                '"current_p_peak": {9}, "current_t_visnp": {10}, '
                '"current_t_vesp": {11}, "current_vm": {12}}}\n'.format(
                    data_split[0],
                    data_split[1],
                    data_split[2],
                    data_split[3],
                    data_split[4],
                    data_split[5],
                    data_split[6],
                    data_split[7],
                    data_split[8],
                    data_split[9],
                    data_split[10],
                    data_split[11],
                    data_split[12],
                    '' if first else ',',
                    float(time.time())))
            if(first):
                first = False

            if terminate:
                log_file.write("]}\n")
                log_file.close()
                exit(0)

            time.sleep(rate)

    exit(0)


try:
    parser = argparse.ArgumentParser(prog='read_mvm_data')
    parser.add_argument(
        '--port', '-p',
        default="/dev/ttyUSB0",
        help="Serial port to connect to")
    parser.add_argument(
        '--rate', '-r',
        default=10,
        type=int,
        help="Default logging rate")
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help="Add verbose response, useful for debugging")
    subparsers = parser.add_subparsers(
        title='Subcommands',
        help='Commands available')

    # Get command
    parser_get = subparsers.add_parser('get', help="get <param>")
    parser_get.add_argument("param", choices=choices_for_get)
    parser_get.set_defaults(func=cmd_get)

    # Set command
    parser_set = subparsers.add_parser('set', help="set <param> <value>")
    parser_set.add_argument("param", choices=choices_for_set)
    parser_set.add_argument("value")
    parser_set.set_defaults(func=cmd_set)

    # Log command
    parser_log = subparsers.add_parser('log', help="log <file>")
    parser_log.add_argument(
        'logfile',
        nargs='?',
        type=argparse.FileType('w+'),
        default=sys.stdout,
        help="Optional, leave blank for stdout")
    parser_log.set_defaults(func=cmd_log)

    args = parser.parse_args()
    verbose = args.verbose
    try:
        rate = 1 / args.rate
    except Exception:
        rate = 0.1

except Exception as e:
    print(e)
    exit(-1)

# Try to establish connection with ESP32
try:
    ser = serial.Serial(
        args.port,
        baudrate=115200,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=2)
except Exception:
    print("Failed to connect to serial port " + args.port)
    exit(-1)

# Run requested subcommand function
try:
    args.func(args)
except Exception as e:
    print(e)

exit(0)
