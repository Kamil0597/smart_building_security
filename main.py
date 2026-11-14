
import time

from communication.mqtt_client import MQTTClient
from security.alarm import AlarmManager
from security.modes import ModeManager

from sensors.sensors import SensorManager
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

def simulate_sensors(sensors):
    sensors.simulate_all()

    readings = sensors.read_all()

    print(readings)
    return readings

def main():
    mqtt = MQTTClient()
    alarms = AlarmManager()
    modes = ModeManager()
    sensors = SensorManager()

    sensor_configuration(sensors)
    print("Sensors configured")

    mqtt.connect()
    print("Mqtt connected")

    try:
        while True:
            time.sleep(1)

            sensor_data = simulate_sensors(sensors)

            mqtt.publish(
                "building/sensors",
                sensor_data
            )

    except KeyboardInterrupt:
        print("Stopping security system...")

    finally:
        mqtt.disconnect()

if __name__ == '__main__':
    main()