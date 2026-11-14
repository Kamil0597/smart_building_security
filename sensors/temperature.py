from sensors.sensor import Sensor


class TemperatureSensor(Sensor):
    def __init__(self, sensor_id):
        super().__init__(sensor_id, "temperature", 22.0)