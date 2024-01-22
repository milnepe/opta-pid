#!/usr/bin/env python3
# https://pymodbustcp.readthedocs.io/en/latest/
"""Write registers"""

from pyModbusTCP.client import ModbusClient


# init modbus client
c = ModbusClient(host='192.168.1.40', port=502, unit_id=255, debug=True, auto_open=True)

Kp = 64
Ki = 10
Kd = int(0 * 100)  # Scale to int
window_size = 5000
setpoint = 70

constants = [Kp, Ki, Kd, window_size, setpoint]

c.write_multiple_registers(24577, constants)

print(constants)
