# mvm-control

Script to control the Mechanical Ventilator Milano

## Installation

To install `pip install mvm-control`

## Upgrade

To upgrade `pip install -U mvm-control`

## Usage

- To set a parameter
`mvm-control set <param> <value>`

- To get a parameter
`mvm-control get <param>`

- To log (don't pass a filename to log to stdout)
`mvm-control log <file>`

- To log at a 20 Hz rate to a file
`mvm-control -r 20 log > my_log_file.json`

- To set a parameter on a device on a specific serial port
`mvm-control -p /dev/ttyUSB1 set run 1`

## Example log output

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
