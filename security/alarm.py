
class AlarmManager:
    TEMPERATURE_THRESHOLD = 60

    def __init__(self):
        self.active_alarms = {}
        self.next_alarm_id = 1

    def activate_alarm(self, sensor_id, alarm_type):
        if sensor_id in self.active_alarms:
            return None

        alarm = {
            "alarm_id": f"alarm_{self.next_alarm_id:03d}",
            "sensor_id": sensor_id,
            "type": alarm_type,
            "status": "active"
        }

        self.next_alarm_id += 1
        self.active_alarms[sensor_id] = alarm

        return alarm

    def reset_alarm(self, sensor_id):
        alarm = self.active_alarms.pop(sensor_id, None)

        if alarm is not None:
            return {**alarm, "status": "reset"}

        return None

    def reset_all(self):
        reset_alarms = []

        for sensor_id in list(self.active_alarms):
            reset_alarms.append(self.reset_alarm(sensor_id))

        return reset_alarms

    def get_active_alarms(self):
        return list(self.active_alarms.values())


    def alarm_check(self, sensor_data, sensors, modes):
        new_alarms = []

        for sensor_id, value in sensor_data.items():

            # Ignore disabled or blocked sensors
            if value is None or sensors.is_blocked(sensor_id):
                continue

            # Sensor type from ID, e.g. temp_01 -> temp
            sensor_type = sensor_id.rsplit("_", 1)[0]

            alarm_type = None

            # Safety sensors - always monitored
            if sensor_type == "smoke" and value is True:
                alarm_type = "fire"

            elif sensor_type == "water" and value is True:
                alarm_type = "flood"

            elif sensor_type == "temp" and value > self.TEMPERATURE_THRESHOLD:
                alarm_type = "high_temperature"

            # Intrusion sensors - depend on mode and arming
            elif sensors.is_armed() and modes.is_sensor_monitored(sensor_type):
                if value is True:
                    alarm_type = "intrusion"

            # Activate new alarm
            if alarm_type is not None:
                alarm = self.activate_alarm(sensor_id, alarm_type)

                if alarm is not None:
                    new_alarms.append(alarm)

        return new_alarms