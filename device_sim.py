from awscrt import io, mqtt
from awsiot import mqtt_connection_builder
import time as t
import json
import random

# --- CONFIGURATION ---
ENDPOINT = "a1v01hr5unragq-ats.iot.us-east-1.amazonaws.com" # Got this from IoT Core > Settings
CLIENT_ID = "smartSensor"
PATH_TO_CERT = "certificate.pem.crt"
PATH_TO_KEY = "private.pem.key"
PATH_TO_ROOT = "AmazonRootCA1.pem"
TOPIC_DATA = "agri/telemetry"
TOPIC_CMD = "agri/commands"

# --- LOGIC ---
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print(f"Received Command: {payload.decode()}")
    # This is where your code would physically turn on the relay/pump
    command = json.loads(payload.decode())
    if command.get("pump") == "ON":
        print("💦 PUMP ACTIVATED! 💦")

# Spin up the connection
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=PATH_TO_CERT,
    pri_key_filepath=PATH_TO_KEY,
    client_bootstrap=client_bootstrap,
    ca_filepath=PATH_TO_ROOT,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=6
)

print(f"Connecting to {ENDPOINT}...")
mqtt_connection.connect().result()
print("Connected!")

# Subscribe to commands (Simulating the water pump listening)
mqtt_connection.subscribe(
    topic=TOPIC_CMD,
    qos=mqtt.QoS.AT_LEAST_ONCE,
    callback=on_message_received
)

# Start the loop
try:
    while True:
        # Simulate sensor data
        temp = round(random.uniform(20.0, 35.0), 1)
        moisture = round(random.uniform(10.0, 80.0), 1) 
        humidity = round(random.uniform(1.0, 15.0), 1)
        
        message = {
            "device_id": CLIENT_ID,
            "temperature": temp,
            "moisture": moisture,
            "humidity": humidity,
            "timestamp": int(t.time())
        }
        
        print(f"Sending: {message}")
        mqtt_connection.publish(
            topic=TOPIC_DATA,
            payload=json.dumps(message),
            qos=mqtt.QoS.AT_LEAST_ONCE
        )
        t.sleep(5) # Send data every 5 seconds

except KeyboardInterrupt:
    print("Disconnecting...")
    mqtt_connection.disconnect().result()