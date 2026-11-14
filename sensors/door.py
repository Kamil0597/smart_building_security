import random

from sensors.sensor import Sensor


class DoorSensor(Sensor):
    def __init__(self, sensor_id):
        super().__init__(sensor_id)
        self.is_open = False

    def read(self):
        if not self.enabled:
            return None
        return self.is_open

    def simulate(self):
        if self.enabled and random.random() < 0.05:
            self.is_open = not self.is_open