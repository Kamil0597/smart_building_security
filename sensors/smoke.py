import random

from sensors.sensor import Sensor


class SmokeSensor(Sensor):
    def __init__(self, sensor_id):
        super().__init__(sensor_id)
        self.smoke_detected = False

    def read(self):
        if not self.enabled:
            return None
        return self.smoke_detected

    def simulate(self):
        if self.enabled:
            self.smoke_detected = random.random() < 0.01