
import time

from communication.mqtt_client import MQTTClient
from security.alarm import AlarmManager
from security.modes import ModeManager

from sensors.sensors import SensorManager
from sensors.simulation import SimulationManager
from sensors.temperature import TemperatureSensor
from sensors.motion import MotionSensor
from sensors.door import DoorSensor
from sensors.window import WindowSensor
from sensors.smoke import SmokeSensor
from sensors.water import WaterSensor


def sensor_configuration(sensors):
    sensors.add_sensor(TemperatureSensor("temp_01"))
    sensors.add_sensor(MotionSensor("motion_01"))
    sensors.add_sensor(DoorSensor("door_01"))
    sensors.add_sensor(WindowSensor("window_01"))
    sensors.add_sensor(SmokeSensor("smoke_01"))
    sensors.add_sensor(WaterSensor("water_01"))


def simulate_sensors(simulation, sensors):
    simulation.update()

    readings = sensors.read_all()

    print(readings)
    return readings


def get_system_status(alarms, modes, sensors):
    return {
        "mode": modes.get_mode(),
        "armed": sensors.is_armed(),
        "active_alarms": alarms.get_active_alarms(),
        "blocked_sensors": list(sensors.blocked_sensors),
        "disabled_sensors": [
            sensor_id
            for sensor_id, sensor in sensors.sensors.items()
            if not sensor.enabled
        ],
        "sensors": [
            {
                "id": sensor_id,
                "type": sensor.sensor_type,
                "enabled": sensor.enabled,
                "blocked": sensors.is_blocked(sensor_id)
            }
            for sensor_id, sensor in sensors.sensors.items()
        ]
    }


def handle_command(topic, data, alarms, modes, sensors):
    command = data.get("command")
    sensor_id = data.get("sensor_id")

    if topic == "building/commands/mode":
        mode = data.get("mode")

        if not isinstance(mode, str):
            return False, "Invalid mode", []

        success = modes.set_mode(mode)
        return success, "Mode updated" if success else "Invalid mode", []

    elif topic == "building/commands/alarm":
        if command == "arm":
            sensors.arm()
            return True, "System armed", []

        elif command == "disarm":
            sensors.disarm()
            return True, "System disarmed", []

        elif command == "reset_all":
            events = alarms.reset_all()
            return True, "All alarms reset", events

        elif command == "reset_one":
            alarm_id = data.get("alarm_id")

            for alarm in alarms.get_active_alarms():
                if alarm.get("alarm_id") == alarm_id:
                    event = alarms.reset_alarm(alarm["sensor_id"])
                    return True, "Alarm reset", [event]

            return False, "Alarm not found", []

        elif command in ("block_sensor", "unblock_sensor"):
            if sensor_id == "all":
                ids = list(sensors.sensors)
            elif isinstance(sensor_id, str) and sensor_id in sensors.sensors:
                ids = [sensor_id]
            else:
                return False, "Sensor not found", []

            for sid in ids:
                if command == "block_sensor":
                    sensors.block_sensor(sid)
                else:
                    sensors.unblock_sensor(sid)

            return True, "Sensor blocking updated", []

    elif topic == "building/commands/sensor":
        if command not in ("enable", "disable"):
            return False, "Unknown sensor command", []

        if sensor_id == "all":
            ids = list(sensors.sensors)
        elif isinstance(sensor_id, str) and sensor_id in sensors.sensors:
            ids = [sensor_id]
        else:
            return False, "Sensor not found", []

        for sid in ids:
            if command == "enable":
                sensors.enable_sensor(sid)
            else:
                sensors.disable_sensor(sid)

        return True, "Sensor state updated", []

    return False, "Unknown command", []


def main():
    mqtt = MQTTClient()
    alarms = AlarmManager()
    modes = ModeManager()
    sensors = SensorManager()

    sensor_configuration(sensors)
    simulation = SimulationManager(sensors)

    print("Sensors configured")

    try:
        mqtt.connect()

        mqtt.publish(
            "building/status",
            get_system_status(alarms, modes, sensors),
            retain=True
        )

        print("Security system turned on")

        while True:
            # Handle incoming commands
            for topic, data in mqtt.get_commands():
                print(f"Received command: {topic} {data}")

                success, message, events = handle_command(
                    topic, data, alarms, modes, sensors
                )

                mqtt.publish("building/responses", {
                    "command_id": data.get("command_id"),
                    "success": success,
                    "message": message
                })

                for event in events:
                    mqtt.publish("building/alerts", event)

                if success:
                    mqtt.publish(
                        "building/status",
                        get_system_status(alarms, modes, sensors),
                        retain=True
                    )

            # Update simulation and read sensors
            sensor_data = simulate_sensors(simulation, sensors)

            # Check threats
            new_alarms = alarms.alarm_check(
                sensor_data, sensors, modes
            )

            # Publish sensor readings
            mqtt.publish("building/sensors", sensor_data)

            # Publish new alarms
            for alarm in new_alarms:
                mqtt.publish("building/alerts", alarm)
                print(f"Alarm activated: {alarm}")

            # Update status when new alarms appear
            if new_alarms:
                mqtt.publish(
                    "building/status",
                    get_system_status(alarms, modes, sensors),
                    retain=True
                )

            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping security system...")

    finally:
        mqtt.disconnect()


if __name__ == "__main__":
    main()
