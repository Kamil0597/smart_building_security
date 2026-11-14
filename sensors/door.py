from sensors.sensor import Sensor


class DoorSensor(Sensor):
    def __init__(self, sensor_id):
        super().__init__(sensor_id, "door", False)