import json

import paho.mqtt.client as mqtt


class MQTTClient:
    def __init__(self, host="localhost", port=1883):
        self.client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )

        self.host = host
        self.port = port

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print(f"MQTT connection failed: {reason_code}")
            return

        print("Connected to MQTT broker")
        client.subscribe("building/commands")

    def on_message(self, client, userdata, message):
        try:
            data = json.loads(message.payload.decode("utf-8"))
            print(f"Received MQTT message: {data}")
        except (UnicodeDecodeError, json.JSONDecodeError):
            print("Invalid MQTT message")

    def connect(self):
        self.client.connect(self.host, self.port)
        self.client.loop_start()

    def publish(self, topic, data):
        payload = json.dumps(data)
        self.client.publish(topic, payload)

    def disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()