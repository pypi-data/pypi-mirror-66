"""
Simple command line tool to access a MVM ESP32 via the serial port

For help on usage type:
python mvm_control.py -h

For help on command usage type:
python mvm_control.py [get/set/log/clog/load/save] -h

Note: The log command can either output to a log file or stdout

The log format is as follows:
{
    "settings": { ... },
    "data": [
        { ... },
        { ... }
    ]
}

The config format is simple the same as the log, with no 'data' field:
{
    "settings": { ... }
}

Where "settings" is a JSON object containing reasonable settings to store (at
the time of this writing)

Each 'data' entry contains the contents of the 'get all' command, and and an
extra parameter 'time' that is a unix timestamp of when it was received.

The compact log format is as follows:
{
    "settings": { ... },
    "format": ['field1','field2', ..., 'fieldN']
    "data": [
        [ ... ],
        [ ... ]
    ]
}

Where 'format' is a list of the data array field names

Where 'data' is now an array of arrays, with the inner array consisting of the
raw values read out
"""


__version__ = '1.3.1'

import serial
import time
import argparse
import sys
import json
import signal
import platform
import serial.tools.list_ports as list_ports

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

# Settings to store when starting a log file
"""
settings_to_store = [
    'backup', 'power_mode', 'battery', 'version', 'alarm', 'warning',
    'run', 'mode', 'rate', 'ratio', 'assist_ptrigger',
    'assist_flow_min', 'ptarget', 'pressure_support', 'backup_enable',
    'backup_min_rate'
]
"""

# Verbosity option
verbose = False
rate = 10
ser = None
terminate = False


def get_available_serial_ports():
    """Gets the available serial ports"""
    ports = [comport.device for comport in list_ports.comports()]
    # Mac OSX seems to have this com port, and it messes things up
    # so hide it from the list of choices
    if '/dev/cu.Bluetooth-Incoming-Port' in ports:
        ports.remove('/dev/cu.Bluetooth-Incoming-Port')
    return ports


def signal_handling(signum, frame):
    """Capture signal and tells log loop to terminate gracefully"""
    global terminate
    terminate = True


signal.signal(signal.SIGINT, signal_handling)


def set_log_settings(log_file, verbose=False):
    """Sends the log settings to the device"""
    try:
        prev_log = json.load(log_file)
    except Exception as e:
        print(e)
        exit(-1)

    settings_to_load = prev_log["settings"]
    for setting in settings_to_load:
        # Write all settable settings back to ESP32
        if setting in choices_for_set and setting != "run":
            if verbose:
                print("Setting " + setting + " to " +
                      str(settings_to_load[setting]))
            set_mvm_param(ser, setting, settings_to_load[setting])
        else:
            if verbose:
                print("Setting " + str(setting) + " is no longer available")


def get_log_settings():
    """Gets the log settings from the device"""
    settings_resp = {}
    for setting in choices_for_get:
        if setting in choices_for_set and setting != "run":
            resp = get_mvm_param(ser, setting)
            if(resp is not False):
                settings_resp[setting] = resp

    return settings_resp


def _parse_response(ser):
    """Parse a response and check if its valid from the ESP32, format is
    'valore=...'"""
    # Sometimes the simpliest solution is best
    # Since we don't know how many messages might have snuck in
    # Or been sent (like a device failure log message)
    # Just skip anything that doesn't work for a bit

    # This might seem absurd, but I need it for my setup with no flow sense
    MAX_RESP_TRIES = 200  # Worst case, no sensors, 170 tries needed
    TIMEOUT = 5.0  # Don't try for longer than this
    num_tries = 0
    start_time = time.time()
    while(num_tries < MAX_RESP_TRIES and time.time() < (start_time + TIMEOUT)):
        # Remove the terminator(s)
        # Use read_until() as it should time out
        response = ser.read_until().decode('utf-8').strip()
        try:
            if(response is not None):
                check, value = response.split('=')
                if(check.lower() == 'valore'):
                    return value
        except Exception:
            pass

        num_tries = num_tries + 1

    return False


def get_mvm_param(ser, param):
    """Request the ESP32 get the value for a given parameter and transmit it"""
    num_tries = 0
    while(num_tries < 3):
        try:
            request = 'get ' + str(param) + '\r\n'
            ser.write(request.encode('utf-8'))
            response = _parse_response(ser)
        except Exception as e:
            print("Error communicating with device")
            print(e)
            return False

        if(response is not False):
            if(response == 'no_data'):
                print("Invalid or unknown command")
                return False
            elif(response[0:5] == 'ERROR'):
                if verbose:
                    print("Command Error, Retrying...")
            else:
                return response

        num_tries = num_tries + 1

    return False


def set_mvm_param(ser, param, value):
    """Request the ESP32 set a parameter to a given value"""
    num_tries = 0
    while(num_tries < 3):
        try:
            request = 'set ' + str(param) + ' ' + str(value) + '\r\n'
            ser.write(request.encode('utf-8'))
            response = _parse_response(ser)
        except Exception as e:
            print("Error communicating with device")
            print(e)
            return False

        try:
            if(response is not False):
                if (response.lower() == 'ok'):
                    return True
                elif(verbose):
                    print("Command Error, Retrying...")
            else:
                return False
        except Exception:
            print("Error parsing response! (" + str(response) + ")")
            return False
        num_tries = num_tries + 1

    print("Bad or unknown response! (" + str(response) + ")")
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
    global verbose

    result = set_mvm_param(ser, args.param, args.value)
    if result is not False:
        if(verbose):
            print("Success")
    else:
        exit(-1)


def cmd_log(args):
    """Log command wrapper"""
    global terminate
    global ser
    global rate
    global verbose

    # Disable verbose if logging to stdout
    if(args.logfile is not sys.stdout and verbose):
        verbose = True
    else:
        verbose = False

    # If the run is active, turn it off and wait a bit
    # so the device can settle before restart
    if(not args.override_run):
        if get_mvm_param(ser, "run") == "1":
            set_mvm_param(ser, "run", 0)
            time.sleep(5)

    # Should we configure the ESP32 with settings from a previous logfile?
    if(args.use_cfg is not None):
        set_log_settings(args.use_cfg, verbose)

    # Run through the dict getting our responses
    settings_resp = get_log_settings()

    # Dump out the settings to the log file
    args.logfile.write("{\n  \"settings\": " +
                       json.dumps(settings_resp, indent=2) + ",\n")

    # Start the data portion of the log file

    if(args.compact):
        args.logfile.write(
            '\"format\": ['
            '\"time\",'
            '\"p_patient\",'
            '\"f_total\",'
            '\"o2\",'
            '\"bpm\",'
            '\"v_total\",'
            '\"peep\",'
            '\"temp\",'
            '\"bat_pwr\",'
            '\"bat_charge\",'
            '\"p_peak\",'
            '\"v_total_insp\",'
            '\"v_total_exhl\",'
            '\"f_peak\"],\n')

    args.logfile.write("\"data\": [\n")
    first = True  # Used to print the ',' between entries

    # Start run
    set_mvm_param(ser, "run", 1)

    while(1):
        resp = get_mvm_param(ser, 'all')
        if(resp is False):
            exit(-1)

        if(verbose):
            print(resp)

        if(first):
            start_time_offset = time.time()

        # Ugly, but split up the data and use some sort of name that makes
        # sense the variable names used inside the Arduino code are a bit
        # hard to parse/grok
        data_split = resp.split(',')

        if(args.compact):
            args.logfile.write(
                '{13}[{14:.3f},{0},{1},{2},{3},{4},'
                '{5},{6},{7},{8},{9},{10},{11},{12}]\n'.format(
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
                    ' ' if first else ',',
                    0.000 if first else float(time.time()-start_time_offset)))

        else:
            args.logfile.write(
                '{13}{{"time":{14:.3f},"p_patient":{0},'
                '"f_total":{1},"o2":{2},"bpm":{3},'
                '"v_total":{4},"peep":{5},"temp":{6},'
                '"bat_pwr":{7},"bat_charge":{8},'
                '"p_peak":{9},"v_total_insp":{10},'
                '"v_total_exhl":{11},"f_peak":{12}}}\n'.format(
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
                    ' ' if first else ',',
                    0.000 if first else float(time.time()-start_time_offset)))

        if(first):
            first = False

        if terminate or (
            (args.time != 0) and time.time() >= (start_time_offset + args.time)
        ):
            args.logfile.write("]}\n")
            args.logfile.close()
            if(not args.override_run):
                set_mvm_param(ser, "run", 0)
            print('')
            exit(0)

        time.sleep(rate)


def cmd_console_log(args):
    """Console Log command wrapper"""
    global terminate
    global ser
    global verbose

    # Disable verbose if logging to stdout
    if(args.logfile is not sys.stdout and verbose):
        verbose = True
    else:
        verbose = False

    # If the run is active, turn it off and wait a bit
    # so the device can settle before restart
    if(not args.override_run):
        if get_mvm_param(ser, "run") == "1":
            set_mvm_param(ser, "run", 0)
            time.sleep(5)

    # Should we configure the ESP32 with settings from a previous logfile?
    if(args.use_cfg is not None):
        set_log_settings(args.use_cfg)

    # Run through the dict getting our responses
    settings_resp = get_log_settings()

    # Dump out the settings to the log file
    args.logfile.write("{\n  \"settings\": \n" +
                       json.dumps(settings_resp, indent=2) + ",\n")

    if(args.compact):
        args.logfile.write(
            '\"format\": ['
            '\"time\",'
            '\"ts\",'
            '\"flux_inhale\",'
            '\"p_valve\",'
            '\"p_patient\",'
            '\"pv1_ctrl\",'
            '\"p_slow\",'
            '\"pv2_ctrl\",'
            '\"f_vent_raw\",'
            '\"f_total\",'
            '\"v_total\",'
            '\"p_patient_dv2\"],\n')

    # Start the data portion of the log file
    args.logfile.write("\"data\": [\n")
    first = True  # Used to print the ',' between entries

    # Start run
    set_mvm_param(ser, "run", 1)

    # Start up console logger
    resp = set_mvm_param(ser, 'console', 1)
    if(resp is False):
        exit(-1)

    if(verbose):
        print(resp)

    while(1):

        # Ugly, but split up the data and use some sort of name that makes
        # sense the variable names used inside the Arduino code are a bit
        # hard to parse/grok

        # Can't use 'get' call here, as console log just spews out messages
        # unrequested
        resp = ser.read_until().decode('utf-8').strip()
        if(verbose):
            print(resp)

        if(first):
            start_time_offset = time.time()

        data_split = resp.split(',')

        if(args.compact):
            args.logfile.write(
                '{11}[{12:.3f},{0},{1},{2},{3},'
                '{4},{5},{6},{7},{8},{9},{10}]\n'.format(
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
                    ' ' if first else ',',
                    0.000 if first else float(time.time()-start_time_offset)))
        else:
            args.logfile.write(
                '{11}{{"time":{12:.3f},"ts":{0},'
                '"flux_inhale":{1},"p_valve":{2},"p_patient":{3},'
                '"pv1_ctrl":{4},"p_slow":{5},"pv2_ctrl":{6},'
                '"f_vent_raw":{7},"f_total":{8},'
                '"v_total":{9},"p_patient_dv2":{10}}}'.format(
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
                    '' if first else ',',
                    0.000 if first else float(time.time()-start_time_offset)))

        if(first):
            first = False

        if terminate or (
            (args.time != 0) and time.time() >= (start_time_offset + args.time)
        ):
            # Turn off console logging
            set_mvm_param(ser, 'console', 0)
            args.logfile.write("]}\n")
            args.logfile.close()
            if(not args.override_run):
                set_mvm_param(ser, "run", 0)
            print('')
            exit(0)

        # Brief sleep so this script doesn't lock up CPU
        time.sleep(0.005)


def cmd_load(args):
    """Command that loads the settings to the device"""
    set_log_settings(args.cfgfile)


def cmd_save(args):
    """Command that saves the settings from the device"""
    settings = get_log_settings()
    args.cfgfile.write(json.dumps({"settings": settings}, indent=2))
    args.cfgfile.close()


def main():
    """Main function"""
    global ser
    global verbose
    global rate

    try:
        parser = argparse.ArgumentParser(prog='mvm-control')
        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s ' + __version__)
        parser.add_argument(
            '--port', '-p',
            metavar="<port>",
            help="Serial port to connect to")
        parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help="Add verbose response, useful for debugging")
        parser.add_argument(
            '--force-dtr',
            type=int,
            choices=[1, 0],
            help="Force DTR to 1 or 0"
        )

        subparsers = parser.add_subparsers(
            title='Subcommands',
            help='Commands available')

        # Get command
        parser_get = subparsers.add_parser(
            'get',
            help="get <param>",
            usage="%(prog)s <param>")
        parser_get.add_argument(
            "param",
            choices=choices_for_get,
            help=' '.join(choices_for_get),
            metavar='param')
        parser_get.set_defaults(func=cmd_get)

        # Set command
        parser_set = subparsers.add_parser(
            'set',
            usage="%(prog)s <param> <value>",
            help="set <param> <value>")
        parser_set.add_argument(
            "param",
            choices=choices_for_set,
            help=' '.join(choices_for_set),
            metavar="param")
        parser_set.add_argument(
            "value",
            help="Value to set")
        parser_set.set_defaults(func=cmd_set)

        # Load configuration command
        parser_load = subparsers.add_parser(
            'load',
            usage="%(prog)s <file>",
            help="load <file>")
        parser_load.add_argument(
            'cfgfile',
            type=argparse.FileType('r'),
            help="JSON configuration to load")
        parser_load.set_defaults(func=cmd_load)

        # Save configuration command
        parser_save = subparsers.add_parser(
            'save',
            usage="%(prog)s -<file>",
            help="save <file>")
        parser_save.add_argument(
            'cfgfile',
            type=argparse.FileType('w+'),
            help="File to save configuration to")
        parser_save.set_defaults(func=cmd_save)

        # Log command
        parser_log = subparsers.add_parser(
            'log',
            usage="%(prog)s [option] <file>",
            help="log [option] <file>")
        parser_log.add_argument(
            '-c',
            '--compact',
            action='store_true',
            help="Generate compact log")
        parser_log.add_argument(
            '-o',
            '--override-run',
            action='store_true',
            help="Override run 0 on end-of-log")
        parser_log.add_argument(
            '-u',
            '--use-cfg',
            metavar="<file>",
            type=argparse.FileType('r'),
            help="Use config file or previous log to configure device")
        parser_log.add_argument(
            '-t',
            '--time',
            metavar="<time>",
            type=int,
            default=0,
            help="Time to run in seconds, may be fractional")
        parser_log.add_argument(
            '-r',
            '--rate',
            default=10,
            type=int,
            metavar="<rate>",
            help="Logging rate in hertz")
        parser_log.add_argument(
            'logfile',
            nargs='?',
            type=argparse.FileType('w+'),
            default=sys.stdout,
            help="Optional, leave blank for stdout")
        parser_log.set_defaults(func=cmd_log)

        # 'Console' Log command
        parser_clog = subparsers.add_parser(
            'clog',
            usage="%(prog)s [option] <file>",
            help="clog [option] <file>")
        parser_clog.add_argument(
            '-c',
            '--compact',
            action='store_true',
            help="Generate compact log")
        parser_clog.add_argument(
            '-o',
            '--override-run',
            action='store_true',
            help="Override run 0 on end-of-log")
        parser_clog.add_argument(
            '-u',
            '--use-cfg',
            metavar="<file>",
            type=argparse.FileType('r'),
            help="Use config file or previous log to configure device")
        parser_clog.add_argument(
            '-t',
            '--time',
            metavar="<time>",
            type=int,
            default=0,
            help="Time to run in seconds, may be fractional")
        parser_clog.add_argument(
            'logfile',
            nargs='?',
            type=argparse.FileType('w+'),
            default=sys.stdout,
            help="Optional, leave blank for stdout")
        parser_clog.set_defaults(func=cmd_console_log)

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
        if(args.port is None and len(get_available_serial_ports()) > 0):
            args.port = get_available_serial_ports()[0]

        if(args.force_dtr is None):
            plt = platform.system()
            if plt == "Windows":
                rts = False
                dtr = False
            else:
                rts = False
                dtr = True
        else:
            rts = False
            dtr = True if args.force_dtr == 1 else False
            print("Forcing DTR to " + str(dtr))
        ser = serial.serial_for_url(
            args.port,
            baudrate=115200,
            bytesize=8,
            parity='N',
            stopbits=1,
            rtscts=rts,
            dsrdtr=dtr,
            do_not_open=True,
            timeout=0.5)
        ser.rts = 1 if rts is True else 0
        ser.dtr = 1 if dtr is True else 0
        ser.open()
    except Exception:
        if(args.port is None):
            print("No serial port available, is the cable unplugged?")
        else:
            print("Failed to connect to serial port " + args.port)
            print("Available serial ports:")
            print(' \n'.join(get_available_serial_ports()))
        exit(-1)

    # Run requested subcommand function
    # This is a fix for python3 + argparse...
    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")

    func(args)

    exit(0)


if __name__ == "__main__":
    main()
