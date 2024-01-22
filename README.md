# opta-pid
Arduino Opta PID controller with ModbusTCP interface

# Installation
Copy the Arduino script to the Opta and setup the shared variables.

Install Python scripts to your ModbusTCP host. 
```
$ cd python/opta-pid
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install pyModbusTCP
```

# Configure
Start Opta
Run configuration client with PID constants and setpoint
```
(venv) $ python write_registers.py
```
Run plant simulation
```
(venv) $ python plant_temperature_simulator.py
```
Check output log in ./output.log and tune PID constants

