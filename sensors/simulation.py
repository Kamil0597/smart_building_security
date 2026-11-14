
import random
import time


class SimulationManager:
    EVENT_DURATIONS = {
        "motion": (2, 5),
        "door": (4, 9),
        "window": (6, 15),
        "smoke": (8, 15),
        "water": (10, 18),
        "temperature": (20, 30)
    }

    def __init__(self, sensors):
        self.sensors = sensors

        self.active_event = None
        self.next_event_time = time.monotonic() + random.uniform(3, 7)
        self.last_update = time.monotonic()

        self.normal_temperature = 22.0
        self.target_temperature = 22.0

    def update(self):
        now = time.monotonic()
        dt = now - self.last_update
        self.last_update = now

        # Finish active event
        if self.active_event is not None:
            if now >= self.active_event["end_time"]:
                self.finish_event()
                self.next_event_time = now + random.uniform(5, 12)

        # Start new event
        elif now >= self.next_event_time:
            self.start_random_event()

        # Update temperature every cycle
        self.update_temperature(dt)

    def start_random_event(self):
        available = [
            sensor
            for sensor in self.sensors.sensors.values()
            if sensor.enabled
        ]

        if not available:
            self.next_event_time = time.monotonic() + 10
            return

        sensor = random.choice(available)
        sensor_type = sensor.sensor_type

        duration_range = self.EVENT_DURATIONS.get(sensor_type)

        if duration_range is None:
            self.next_event_time = time.monotonic() + 10
            return

        duration = random.uniform(*duration_range)

        self.active_event = {
            "sensor_id": sensor.sensor_id,
            "type": sensor_type,
            "end_time": time.monotonic() + duration
        }

        if sensor_type == "temperature":
            self.target_temperature = random.uniform(65, 85)
        else:
            sensor.set_value(True)

        print(
            f"[SIMULATION] Event started: {sensor.sensor_id} "
            f"(duration: {duration:.1f}s)"
        )

    def finish_event(self):
        event = self.active_event

        sensor = self.sensors.get_sensor(event["sensor_id"])

        if event["type"] == "temperature":
            self.target_temperature = self.normal_temperature

        elif sensor is not None:
            sensor.set_value(False)

        print(f"[SIMULATION] Event finished: {event['sensor_id']}")

        self.active_event = None

    def update_temperature(self, dt):
        temperature_sensor = next(
            (
                sensor
                for sensor in self.sensors.sensors.values()
                if sensor.sensor_type == "temperature"
            ),
            None
        )

        if temperature_sensor is None or not temperature_sensor.enabled:
            return

        current = temperature_sensor.value

        # Heating is faster than cooling
        rate = 4.0 if self.target_temperature > current else 2.0

        max_change = rate * dt
        difference = self.target_temperature - current

        change = max(-max_change, min(max_change, difference))

        # Small natural fluctuations
        noise = random.uniform(-0.03, 0.03)

        temperature_sensor.set_value(
            round(current + change + noise, 2)
        )
