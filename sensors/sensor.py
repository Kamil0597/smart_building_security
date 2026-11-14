from abc import ABC, abstractmethod


class Sensor(ABC):
    def __init__(self, sensor_id):
        self.sensor_id = sensor_id
        self.enabled = True

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def simulate(self):
        pass

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False