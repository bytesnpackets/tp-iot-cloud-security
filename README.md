# Smart Agriculture IoT Sensor Simulator (AWS IoT Core)

School project: Cloud Security (COST), Diploma in Cybersecurity & Digital Forensics, Temasek Polytechnic (Oct to Dec 2025). Part of a group IoT project covering IoT sensors, MQTT and a web app with a historian database; this repo is the device side.

`device_sim.py` simulates a field sensor. It connects to AWS IoT Core over MQTT with mutual TLS (X.509 device certificate), publishes temperature, soil moisture and humidity every 5 seconds to `agri/telemetry`, and listens on `agri/commands` to switch a simulated water pump on.

## Run
```bash
pip install awsiotsdk
```
Create an IoT Thing in AWS IoT Core, download its certificate and private key, then put `certificate.pem.crt`, `private.pem.key` and `AmazonRootCA1.pem` next to the script. Set `ENDPOINT` to your own IoT endpoint and run `python device_sim.py`.

Certificates and keys are git-ignored and are never committed.
