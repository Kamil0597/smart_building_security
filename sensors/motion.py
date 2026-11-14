import random

from sensors.sensor import Sensor


class MotionSensor(Sensor):
    def __init__(self, sensor_id):
        super().__init__(sensor_id)
        self.motion = False

    def read(self):
        if not self.enabled:
            return None
        return self.motion

    def simulate(self):
        if self.enabled:
            self.motion = random.random() < 0.1