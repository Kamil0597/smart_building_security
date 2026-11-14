import random

from sensors.sensor import Sensor


class WaterSensor(Sensor):
    def __init__(self, sensor_id):
        super().__init__(sensor_id)
        self.water_detected = False

    def read(self):
        if not self.enabled:
            return None
        return self.water_detected

    def simulate(self):
        if self.enabled:
            self.water_detected = random.random() < 0.01