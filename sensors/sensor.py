
class Sensor:
    def __init__(self, sensor_id, sensor_type, initial_value):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.value = initial_value
        self.enabled = True

    def read(self):
        if not self.enabled:
            return None

        return self.value

    def set_value(self, value):
        self.value = value

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
