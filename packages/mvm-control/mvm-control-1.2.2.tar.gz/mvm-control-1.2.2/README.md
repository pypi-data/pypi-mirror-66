# mvm-control

Script to control the Mechanical Ventilator Milano

## Installation

To install

   `pip install mvm-control`

## Upgrade

To upgrade

   `pip install -U mvm-control`

## Usage

`mvm-control [options] <subcommand> [sub options] ...`

The following subcommands are available:

- set
- get
- load
- save
- log
- clog

### Example

`mvm-control -p /dev/ttyUSB0 log run_001.json`

### Options

  - Force the DTR bit on the serial port, if the board resets every time you issue a command, try forcing this high or low

    `--force-dtr [0/1]`

  - Increase the verbosity of output

	`-v / --verbose`

  - Specify the serial port to use

    `-p / --port <port>`

  - Print the version out and exit

	`--version`

### Set

Sets a parameter on the ESP32

`mvm-control set <param> <value>`

#### Example

`mvm-control set mode 1`

### Get

Gets a parameter on the ESP32 and return its string value

`mvm-control get <param>`

#### Example

`mvm-control get mode`

### Log

Logs the ESP32 response to `get all` to a file, hit CTRL+C to break.

`mvm-control log <file>`

#### Options

  - Set the logging rate in hertz: `-r / --rate <hertz>`
  - Setup the ESP32 using a configuration or log file: `-u / --use-cfg <file>`

#### Example

`mvm-control log -r 20 -u cfg.json run_001.json`

### Console_log

Sets the ESP32 into console mode, and logs the ESP32 debug messages

`mvm-control clog my_log.json`

#### Options

  - Setup the ESP32 using a configuration or log file: `-u / --use-cfg <file>`

#### Example

`mvm-control clog --use-cfg cfg.json run_001.json`

### Load

Loads a JSON configuration files settings into an ESP32.

`mvm-control load <file>`

#### Example

`mvm-control load file.json`

**Note**: This works on configuration files and log files

### Save

Saves an ESP32 configuration to a JSON file

`mvm-control save <file>`

#### Example

`mvm-control save file.json`

## Examples

### log file

```
{
	"settings": {
		"warning": "0",
		"assist_ptrigger": "4.00",
		"run": "0",
		"battery": "100.00",
		"power_mode": "0",
		"alarm": "0",
		"backup_min_rate": "0.00",
		"pressure_support": "20.00",
		"rate": "15.00",
		"version": "HW_V3_2020_04_15_00",
		"ptarget": "20.00",
		"mode": "0",
		"backup_enable": "0",
		"ratio": "0.61",
		"backup": "0",
		"assist_flow_min": "5.00"
	},
	"data": [{
		"time": 1587000784.05,
		"last_pressure": 0.00,
		"flux": 239.54,
		"last_o2": 21.70,
		"last_bpm": 0.00,
		"tidalvolume": 0.00,
		"last_peep": 0.00,
		"temperature": 24.00,
		"battery_powered": 0,
		"current_battery_charge": 100.00,
		"current_p_peak": 0.00,
		"current_t_visnp": 0.00,
		"current_t_vesp": 0.00,
		"current_vm": 0.00
	},
    {
        "time": 1587000784.06,
        "last_pressure": 0.00,
        "flux": 239.54,
        "last_o2": 21.70,
        "last_bpm": 0.00,
        "tidalvolume": 0.00,
        "last_peep": 0.00,
        "temperature": 24.00,
        "battery_powered": 0,
        "current_battery_charge": 100.00,
        "current_p_peak": 0.00,
        "current_t_visnp": 0.00,
        "current_t_vesp": 0.00,
        "current_vm": 0.00
    }]
}
```
