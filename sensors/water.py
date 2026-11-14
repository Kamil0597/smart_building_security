from sensors.sensor import Sensor


class WaterSensor(Sensor):
    def __init__(self, sensor_id):
        super().__init__(sensor_id, "water", False)