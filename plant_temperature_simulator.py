"""Modbus TCP Plant Temperature Simulator client"""
import logging
import time
from temperature_profile import TemperatureProfile
from time import sleep
from threading import Lock
from threading import Event
from pyModbusTCP.client import ModbusClient
from enum import Enum


logging.basicConfig(filename='output.log', format='%(asctime)s %(message)s', datefmt='%I:%M:%S', encoding='utf-8', level=logging.DEBUG)


class State(Enum):
    COOLING = 0
    HEATING = 1


def tows(integer_16: int) -> int:
    """Converts negative 16bit integers to positive ints in 2s compliment form"""
    if integer_16 is not None:
        return int(bin(integer_16 % (1 << 16)), 2)
    else:
        return 0


class PlantTemperatureSimulator():
    # Shared mutex lock ensures the temperature profile class instance can only
    # be updated by one profile at a time.
    shared_lock = Lock()
    # Events start and stop each profile accoring to the heating/cooling state
    heating_event = Event()
    cooling_event = Event()

    # Create a separate heating & cooling profiles that govern the temperature behaviour of the plant
    heating_profile = TemperatureProfile('Heating', shared_lock, heating_event, 1, 2)
    cooling_profile = TemperatureProfile('Cooling', shared_lock, cooling_event, -1, 2)

    # Init modbus client
    c = ModbusClient(host='192.168.1.40', port=502, unit_id=255, debug=False, auto_open=True)

    def __init__(self):
        previous_state = State.COOLING.value  # Set initial state

        PlantTemperatureSimulator.heating_profile.start()
        PlantTemperatureSimulator.cooling_profile.start()

        while True:
            # Get the state of the heater coil from the PLC
            try:
                register = PlantTemperatureSimulator.c.read_holding_registers(24575, 7)
                # Inject the heaters state into the simulation from register[0]
                # 0 -> HEATER OFF
                # 1 -> HEATER ON
                current_state = register[0]
                setpoint = register[6]
                if previous_state != current_state:
                    # State has changed
                    if current_state == State.HEATING.value:
                        PlantTemperatureSimulator.cooling_event.clear()
                        PlantTemperatureSimulator.heating_event.set()
                        print(f'Heating...')
                    else:
                        PlantTemperatureSimulator.heating_event.clear()
                        PlantTemperatureSimulator.cooling_event.set()
                        print(f'Cooling...')
                    previous_state = current_state
            except:
                print("Oops!  ModbusTCP Error, tring again...")
            try:
                # Send a two's compliment value as int in range 0 - 65535
                PlantTemperatureSimulator.c.write_single_register(24576, tows(TemperatureProfile.temperature))
            except:
                print("Oops!  ModbusTCP Error, tring again...")
            logging.info("%s %s", TemperatureProfile.temperature, setpoint)
            print(f'Temperature: {TemperatureProfile.temperature} Setpoint: {setpoint}')
            sleep(1)


if __name__ == '__main__':
    PlantTemperatureSimulator()
