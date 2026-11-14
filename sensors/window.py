from sensors.sensor import Sensor


class WindowSensor(Sensor):
    def __init__(self, sensor_id):
        super().__init__(sensor_id, "window", False)