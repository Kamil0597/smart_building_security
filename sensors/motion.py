from sensors.sensor import Sensor


class MotionSensor(Sensor):
    def __init__(self, sensor_id):
        super().__init__(sensor_id, "motion", False)