import random

from sensors.sensor import Sensor


class TemperatureSensor(Sensor):
    def __init__(self, sensor_id):
        super().__init__(sensor_id)
        self.temperature = 22.0

    def read(self):
        if not self.enabled:
            return None
        return round(self.temperature, 2)

    def simulate(self):
        if self.enabled:
            self.temperature += random.uniform(-0.5, 0.5)