from sensors.sensor import Sensor


class SmokeSensor(Sensor):
    def __init__(self, sensor_id):
        super().__init__(sensor_id, "smoke", False)