"""Model temperature profile that changes at a constant rate"""
from time import sleep
from threading import Thread
from threading import Lock
from threading import Event
from pyModbusTCP.client import ModbusClient


class TemperatureProfile(Thread):
    """Sets a fixed amount by which the temperature is incremented or decremented per second."""
    temperature = 90  # Class instance

    def __init__(self, identity, lock, event, dtemp, dtime):
        """Sets the rate of change for the temperature.
        dtemp = number of degrees change each cycle
        dtime = number of seconds between temperature changes"""
        Thread.__init__(self)
        self.dtemp = dtemp
        self.dtime = dtime
        self.identity = identity
        self.lock = lock
        self.event = event

    def run(self):
        """Updates the class temperature instance from within its own thread"""
        while True:
            if TemperatureProfile.temperature is not None:
                self.event.wait()
                with self.lock:  # Acquire the lock
                    TemperatureProfile.temperature = TemperatureProfile.temperature + self.dtemp
                    sleep(self.dtime)
