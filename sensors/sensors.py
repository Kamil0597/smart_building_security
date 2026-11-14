class SensorManager:
    def __init__(self):
        self.sensors = {}

    def add_sensor(self, sensor):
        self.sensors[sensor.sensor_id] = sensor

    def simulate_all(self):
        for sensor in self.sensors.values():
            sensor.simulate()

    def read_all(self):
        readings = {}

        for sensor_id, sensor in self.sensors.items():
            readings[sensor_id] = sensor.read()

        return readings