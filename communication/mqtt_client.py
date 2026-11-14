
import json
from queue import Queue, Empty
from threading import Event

import paho.mqtt.client as mqtt


class MQTTClient:
    def __init__(self, host="localhost", port=1883):
        self.host = host
        self.port = port

        self.commands = Queue()
        self.connected = Event()

        self.client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print(f"MQTT connection failed: {reason_code}")
            return

        client.subscribe("building/commands/+", qos=1)
        self.connected.set()
        print("Connected to MQTT broker")

    def on_disconnect(self, client, userdata, disconnect_flags,
                      reason_code, properties):
        self.connected.clear()

    def on_message(self, client, userdata, message):
        try:
            data = json.loads(message.payload.decode("utf-8"))

            if not isinstance(data, dict):
                raise ValueError("Command must be a JSON object")

            if message.retain:
                return

            self.commands.put((message.topic, data))

        except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
            print("Invalid MQTT message")

    def connect(self):
        self.client.connect(self.host, self.port)
        self.client.loop_start()

        if not self.connected.wait(timeout=5):
            self.disconnect()
            raise ConnectionError("MQTT connection timeout")

    def publish(self, topic, data, retain=False):
        payload = json.dumps(data)
        return self.client.publish(
            topic, payload, qos=1, retain=retain
        )

    def get_commands(self):
        commands = []

        while True:
            try:
                commands.append(self.commands.get_nowait())
            except Empty:
                break

        return commands

    def disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()
