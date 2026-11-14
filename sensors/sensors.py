
class SensorManager:
    def __init__(self):
        self.sensors = {}
        self.armed = False
        self.blocked_sensors = set()

    def add_sensor(self, sensor):
        self.sensors[sensor.sensor_id] = sensor

    def read_all(self):
        return {
            sensor_id: sensor.read()
            for sensor_id, sensor in self.sensors.items()
        }

    def get_sensor(self, sensor_id):
        return self.sensors.get(sensor_id)

    def arm(self):
        self.armed = True

    def disarm(self):
        self.armed = False

    def is_armed(self):
        return self.armed

    def enable_sensor(self, sensor_id):
        sensor = self.get_sensor(sensor_id)

        if sensor is None:
            return False

        sensor.enable()
        return True

    def disable_sensor(self, sensor_id):
        sensor = self.get_sensor(sensor_id)

        if sensor is None:
            return False

        sensor.disable()
        return True

    def block_sensor(self, sensor_id):
        if sensor_id not in self.sensors:
            return False

        self.blocked_sensors.add(sensor_id)
        return True

    def unblock_sensor(self, sensor_id):
        if sensor_id not in self.sensors:
            return False

        self.blocked_sensors.discard(sensor_id)
        return True

    def is_blocked(self, sensor_id):
        return sensor_id in self.blocked_sensors
