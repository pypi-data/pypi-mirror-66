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


__version__ = '1.4.1'

import os
import time
import argparse
import sys
import json
import signal
import platform
from collections import OrderedDict
import requests
import serial
import serial.tools.list_ports as list_ports
import paho.mqtt.client as mqtt

# Choices allowed for 'get' command
CHOICES_FOR_GET = [
    'pressure', 'flow', 'o2', 'bpm', 'backup',
    'tidal', 'peep', 'temperature', 'power_mode',
    'battery', 'version', 'alarm', 'warning',
    'run', 'mode', 'rate', 'ratio',
    'assist_ptrigger', 'assist_flow_min',
    'ptarget', 'pressure_support', 'backup_enable', 'backup_min_rate',
    'all', 'calib', 'calibv', 'stats'
]

# Choices allowed for 'set' command
CHOICES_FOR_SET = [
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

# Measurements returned from 'get all' command
MEASUREMENTS_RETURNED = [
    'p_patient', 'f_total', 'o2', 'bpm', 'v_total', 'peep', 'temp', 'bat_pwr',
    'bat_charge', 'p_peak', 'v_total_insp', 'v_total_exhl', 'v_minute'
]

# Verbosity option
verbose = False
rate = 10
ser = None
terminate = False


def convert_json_to_csv(json_file, csv_file):
    """Convert JSON log to CSV"""
    # Load JSON data in OrderedDict, to preserve current order
    json_data = json.load(json_file, object_pairs_hook=OrderedDict)

    # Print out the header based on JSON contents

    # Compact Format
    if "format" in json_data:
        # Create header
        for idx, elem in enumerate(json_data['format']):
            csv_file.write("{0}{1}".format('' if idx == 0 else ',', elem))
        csv_file.write('\n')

        # Write out data
        if "data" in json_data:
            for elem in json_data['data']:
                csv_file.write(','.join(map(str, elem)) + '\n')

    # Non-compact format
    else:
        if "data" in json_data:
            for idx, (key, value) in enumerate(json_data['data'][0].items()):
                csv_file.write("{0}{1}".format('' if idx == 0 else ',', key))
            csv_file.write('\n')

            for row in json_data['data']:
                for idx, (key, value) in enumerate(row.items()):
                    csv_file.write("{0}{1}".format(
                        '' if idx == 0 else ',', value))
                csv_file.write('\n')


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
        sys.exit(-1)

    settings_to_load = prev_log["settings"]
    for setting in settings_to_load:
        # Write all settable settings back to ESP32
        if setting in CHOICES_FOR_SET and setting != "run":
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
    for setting in CHOICES_FOR_GET:
        if setting in CHOICES_FOR_SET and setting != "run":
            resp = get_mvm_param(ser, setting)
            if resp is not False:
                # Needed for handling inconsistencies between firmware and mock
                if resp == "unknown":
                    resp = "NaN"
                else:
                    # This is dirty, but effective
                    try:
                        resp = int(resp)
                    except Exception:
                        resp = float(resp)
                settings_resp[setting] = resp

    return settings_resp


def parse_response(ser):
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
    while num_tries < MAX_RESP_TRIES and time.time() < (start_time + TIMEOUT):
        # Remove the terminator(s)
        # Use read_until() as it should time out
        response = ser.read_until().decode('utf-8').strip()
        try:
            if response is not None:
                check, value = response.split('=')
                if check.lower() == 'valore':
                    return value
        except Exception:
            pass

        num_tries = num_tries + 1

    return False


def get_mvm_param(ser, param):
    """Request the ESP32 get the value for a given parameter and transmit it"""
    num_tries = 0
    while num_tries < 3:
        try:
            request = 'get ' + str(param) + '\r\n'
            ser.write(request.encode('utf-8'))
            response = parse_response(ser)
        except Exception as e:
            print("Error communicating with device")
            print(e)
            return False

        if response is not False:
            if response == 'no_data':
                print("Invalid or unknown command")
                return False
            if response[0:5] == 'ERROR':
                if verbose:
                    print("Command Error, Retrying...")
            else:
                return response

        num_tries = num_tries + 1

    return False


def set_mvm_param(ser, param, value):
    """Request the ESP32 set a parameter to a given value"""
    num_tries = 0
    while num_tries < 3:
        try:
            request = 'set ' + str(param) + ' ' + str(value) + '\r\n'
            ser.write(request.encode('utf-8'))
            response = parse_response(ser)
        except Exception as e:
            print("Error communicating with device")
            print(e)
            return False

        try:
            if response is not False:
                if response.lower() == 'ok':
                    return True
                if verbose:
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
        sys.exit(-1)


def cmd_set(args):
    """Set command wrapper"""
    global verbose

    result = set_mvm_param(ser, args.param, args.value)
    if result is not False:
        if verbose:
            print("Success")
    else:
        sys.exit(-1)


def url_retrieve(url, outfile):
    """Retrieve content from a URL and put it intoa file"""
    resp = requests.get(url, allow_redirects=True)
    if resp.status_code != 200:
        raise ConnectionError('could not download {}\nerror code: {}'
                              ''.format(url, resp.status_code))

    with open(outfile, "wb+") as dfile:
        dfile.write(resp.content)


def cmd_log(args):
    """Log command wrapper"""
    global terminate
    global ser
    global rate
    global verbose

    # Set up remote monitoring
    if args.monitor is not None:

        # Get configuration parameters
        try:
            with open(args.monitorconfigfile, "r") as mcfgfile:
                monitorconfig = json.load(mcfgfile)
        except Exception as e:
            print("Error")
            print(e)
            sys.exit(-1)

        # Set up and connect to the broker
        stats = {}  # Used by callback functions
        mqttclient = mqtt.Client(userdata=stats)
        if not os.path.isfile(monitorconfig["cacertfile"]):
            url_retrieve(
                monitorconfig["cacerturl"], monitorconfig["cacertfile"])
        mqttclient.tls_set(ca_certs=monitorconfig["cacertfile"])
        mqttclient.username_pw_set(args.monitor[0], args.monitor[1])
        mqttclient.on_connect = on_connect
        mqttclient.on_publish = on_publish
        mqttclient.connect(
            monitorconfig["broker"], monitorconfig["brokerport"], 60)
        mqttclient.loop_start()
        topic = "mvm/%s/%s/%s" % (monitorconfig["institute"],
                                  args.campaign, args.run)
        print("\n\tmeasurements are visible at %s" %
              monitorconfig["dashboard"])
        # Set minimum reading interval to 0.1 s (<10 Hz) when using remote monitoring
        if rate < 0.1:  # s
            rate = 0.1  # s

        # Set minimum send interval
        if args.sendinterval < 5.:  # s
            sendinterval = 5.  # s
        else:
            sendinterval = args.sendinterval

        # Stats for callback functions
        stats["topic"] = topic
        if args.logfile is not sys.stdout or args.nolog:
            stats["lineend"] = "\r"
        else:
            stats["lineend"] = "\r\n"
        stats["sendinterval"] = sendinterval  # s
        stats["sentcounter"] = 0
        stats["datacounter"] = 0  # MB

        print("\t  last data sent at\t   run time  measurements\t succ./  "
              "sent\t    tot. data\t message size\t      data rate\t\tmvm/"
              "institute/campaign/run")
        payload = []

    # Disable verbose if logging to stdout
    if args.logfile is not sys.stdout and verbose:
        verbose = True
    else:
        verbose = False

    # If the run is active, turn it off and wait a bit
    # so the device can settle before restart
    if not args.override_run:
        if get_mvm_param(ser, "run") == "1":
            set_mvm_param(ser, "run", 0)

    # Should we configure the ESP32 with settings from a previous logfile?
    if args.use_cfg is not None:
        set_log_settings(args.use_cfg, verbose)
        # Wait some time for those settings to come into effect
        time.sleep(3)

    # Run through the dict getting our responses
    settings_resp = get_log_settings()

    # Dump out the settings to the log file
    if not args.nolog:
        args.logfile.write("{\n  \"settings\": " +
                           json.dumps(settings_resp, indent=2) + ",\n")

    # Start the data portion of the log file
    if not args.nolog and args.compact:
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

    if not args.nolog:
        args.logfile.write("\"data\": [\n")
    first = True  # Used to print the ',' between entries

    # Start run
    set_mvm_param(ser, "run", 1)
    start_time_offset = time.time()
    lasttime = start_time_offset
    if args.monitor is not None:
        # Prepare settings for payload
        monitorcounter = 0
        logcounter = 0
        payloadsettings = settings_resp
        payloadsettings["firmware"] = get_mvm_param(
            ser, "version")  # Firmware version
        payloadsettings["type"] = "setting"  # Set type label
        stats["logstarttime"] = start_time_offset

    while 1:

        # Get all measurements
        resp = get_mvm_param(ser, 'all')
        if resp is False:
            sys.exit(-1)

        if verbose:
            print(resp)

        # Ugly, but split up the data and use some sort of name that makes
        # sense the variable names used inside the Arduino code are a bit
        # hard to parse/grok
        data_split = resp.split(',')

        if not args.nolog and args.compact:
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

        elif not args.nolog:
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

        # Remote monitoring
        if args.monitor is not None:

            # Dump the measurements to the payload
            payload.append(dict(zip(
                # Keys
                MEASUREMENTS_RETURNED+["alarm", "warning",
                                       "firmware", "type", "timestamp"],
                # Values
                json.loads("["+resp+"]")+[
                    int(get_mvm_param(ser, "alarm")),
                    int(get_mvm_param(ser, "warning")),
                    get_mvm_param(ser, "version"),
                    "measurement",
                    time.time()])))

            # Send data to the monitoring server every <sendinterval> seconds
            if time.time() - (lasttime > sendinterval):

                # Dump the settings to the payload
                payloadsettings["timestamp"] = time.time()
                payload.append(payloadsettings)

                # Send data
                monitorcounter += 1
                payloadsize = len(json.dumps(payload).encode('utf-8'))/1024.
                stats["payloadsize"] = payloadsize
                stats["logcounter"] = logcounter
                stats["monitorcounter"] = monitorcounter
                mqttclient.publish(topic, json.dumps(payload), qos=2)
                print_monitoring_stats(stats)

                # At last
                lasttime = time.time()
                payload = []

            logcounter += 1

        if first:
            first = False

        if terminate or (
                        (args.time != 0) and time.time() >= (start_time_offset + args.time)):
            if not args.nolog:
                args.logfile.write("]}\n")
                if args.also_csv:
                    args.logfile.seek(0, 0)
                    with open(
                            args.logfile.name[0:-4] + "csv", "w+"
                    ) as csvfile:
                        convert_json_to_csv(args.logfile, csvfile)
                args.logfile.close()
            if not args.override_run:
                set_mvm_param(ser, "run", 0)
            print('')
            sys.exit(0)

        time.sleep(rate)


def on_connect(client, stats, flags, rc):
    """Callback function used when connection to the broker is established."""
    if rc != 0:
        print("could not connect: "+rc)


def on_publish(client, stats, mid):
    """Callback function used when data is successfully sent."""
    stats["sentcounter"] += 1
    stats["datacounter"] += stats["payloadsize"]/1024.  # MB
    print_monitoring_stats(stats)


def print_monitoring_stats(stats):
    """Print monitoring stats on the same line over and over again."""
    sys.stdout.write("\t%s    %s\t   %s\t%s/%s\t%s MB\t%s kB\t%s kB/s\t\t%s%s" %
                     (time.strftime("%Y-%m-%d %H:%M:%S"),
                      get_time_string(time.time()-stats["logstarttime"]),
                      "{:06}".format(stats["logcounter"]),
                      "{:06}".format(stats["sentcounter"]),
                      "{:06}".format(stats["monitorcounter"]),
                      "{:10.3f}".format(stats["datacounter"]),  # MB
                      "{:10.1f}".format(stats["payloadsize"]),  # kB
                      "{:10.1f}".format(stats["payloadsize"] / \
                                        stats["sendinterval"]),  # kB/s
                      stats["topic"], stats["lineend"]))


def get_time_string(seconds):
    """Convert seconds into a string of days, hours, minutes and seconds."""
    d = int(seconds//(60*60*24))
    seconds = seconds % (60*60*24)
    h = int(seconds//(60*60))
    seconds = seconds % (60*60)
    m = int(seconds//(60))
    s = round(seconds % (60))
    return ("%s %s:%s:%s" % ("{:03}".format(d), "{:02}".format(h),
                             "{:02}".format(m), "{:02}".format(s)))


def cmd_console_log(args):
    """Console Log command wrapper"""
    global terminate
    global ser
    global verbose

    # Disable verbose if logging to stdout
    if args.logfile is sys.stdout:
        verbose = False

    # If the run is active, turn it off and wait a bit
    # so the device can settle before restart
    if not args.override_run:
        if get_mvm_param(ser, "run") == "1":
            set_mvm_param(ser, "run", 0)

    # Should we configure the ESP32 with settings from a previous logfile?
    if args.use_cfg is not None:
        set_log_settings(args.use_cfg)

        # Wait a bit and clear out the old settings
        time_to_poll = time.time()
        while time.time() < (time_to_poll + 3.0):
            resp = ser.read_until().decode('utf-8').strip()
            time.sleep(0.01)

    # Run through the dict getting our responses
    settings_resp = get_log_settings()

    # Dump out the settings to the log file
    args.logfile.write("{\n  \"settings\": \n" +
                       json.dumps(settings_resp, indent=2) + ",\n")

    if args.compact:
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
    if resp is False:
        sys.exit(-1)

    if verbose:
        print(resp)

    while 1:

        # Ugly, but split up the data and use some sort of name that makes
        # sense the variable names used inside the Arduino code are a bit
        # hard to parse/grok

        # Can't use 'get' call here, as console log just spews out messages
        # unrequested
        resp = ser.read_until().decode('utf-8').strip()
        if verbose:
            print(resp)

        if first:
            start_time_offset = time.time()

        data_split = resp.split(',')

        if args.compact:
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

        if first:
            first = False

        if terminate or (
                (args.time != 0) and time.time() >= (start_time_offset + args.time)
        ):
            # Turn off console logging
            set_mvm_param(ser, 'console', 0)
            args.logfile.write("]}\n")

            if args.also_csv:
                args.logfile.seek(0, 0)
                with open(args.logfile.name[0:-4] + "csv", "w+") as csvfile:
                    convert_json_to_csv(args.logfile, csvfile)

            args.logfile.close()

            if not args.override_run:
                set_mvm_param(ser, "run", 0)
            print('')
            sys.exit(0)

        # Brief sleep so this script doesn't lock up CPU
        time.sleep(0.005)


def cmd_convert(args):
    """Command to convert JSON log file to CSV"""
    convert_json_to_csv(args.jsonfile, args.csvfile)


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

        # Convert command
        parser_convert = subparsers.add_parser(
            'convert',
            help='convert <jsonfile> <csvfile>',
            usage="%(prog)s <jsonfile> <csvfile>"
        )
        parser_convert.add_argument(
            'jsonfile',
            type=argparse.FileType('r'),
            help="JSON file to convert to CSV")
        parser_convert.add_argument(
            'csvfile',
            type=argparse.FileType('w+'),
            help="CSV file to create")
        parser_convert.set_defaults(func=cmd_convert)

        # Get command
        parser_get = subparsers.add_parser(
            'get',
            help="get <param>",
            usage="%(prog)s <param>")
        parser_get.add_argument(
            "param",
            choices=CHOICES_FOR_GET,
            help=' '.join(CHOICES_FOR_GET),
            metavar='param')
        parser_get.set_defaults(func=cmd_get)

        # Set command
        parser_set = subparsers.add_parser(
            'set',
            usage="%(prog)s <param> <value>",
            help="set <param> <value>")
        parser_set.add_argument(
            "param",
            choices=CHOICES_FOR_SET,
            help=' '.join(CHOICES_FOR_SET),
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
            '-a',
            '--also-csv',
            action='store_true',
            help='Also create CSV file')
        parser_log.add_argument(
            '-c',
            '--compact',
            action='store_true',
            help="Generate compact log")
        parser_log.add_argument(
            '-n',
            '--no-log',
            dest='nolog',
            action='store_true',
            help="Do not print to screen nor save to file")
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
        parser_log.add_argument(
            '-m',
            '--monitor',
            nargs=2,
            metavar=('username', 'password'),
            default=None,
            help="Client username and password to"
            " send data for remote monitoring")
        parser_log.add_argument(
            '-mc',
            '--monitor-config',
            metavar="<file>",
            dest="monitorconfigfile",
            default="monitorconfig.json",
            type=str,
            help="Remote monitoring configuration file")
        parser_log.add_argument(
            '--campaign',
            default=time.strftime("%Y%m%d"),
            metavar="<campaign>",
            help="Campaign name")
        parser_log.add_argument(
            '--run',
            default="test",
            metavar="<run>",
            help="Run name")
        parser_log.add_argument(
            '--sendinterval',
            default=5.,
            metavar="<sendinterval>",
            help="Time interval to send monitoring data")
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
            '-a',
            '--also-csv',
            action='store_true',
            help='Also create CSV file')
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
        sys.exit(-1)

    # Try to establish connection with ESP32
    try:
        if args.port is None and len(get_available_serial_ports()) > 0:
            args.port = get_available_serial_ports()[0]

        if args.force_dtr is None:
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
        if args.port is None:
            print("No serial port available, is the cable unplugged?")
        else:
            print("Failed to connect to serial port " + args.port)
            print("Available serial ports:")
            print(' \n'.join(get_available_serial_ports()))
        sys.exit(-1)

    # Run requested subcommand function
    # This is a fix for python3 + argparse...
    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")

    func(args)

    sys.exit(0)


if __name__ == "__main__":
    main()
