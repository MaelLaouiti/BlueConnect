Prerequisites:
Make sure both Raspberry Pi devices are connected to the same WiFi network.
Install necessary software on both devices.
Steps:
1. Set up MQTT Broker:
You can use a public MQTT broker or set up your own broker on one of your Raspberry Pi devices. Popular public MQTT brokers include HiveMQ and Mosquitto. If you want to set up your own broker:

On Raspberry Pi 3:

sudo apt-get update
sudo apt-get install mosquitto mosquitto-clients
2. Configure MQTT Broker:
On Raspberry Pi 3:
Edit the Mosquitto configuration file:

sudo nano /etc/mosquitto/mosquitto.conf
Add the following lines at the end of the file:

allow_anonymous false
password_file /etc/mosquitto/passwd
Save the file and create a username/password for authentication:

sudo mosquitto_passwd -c /etc/mosquitto/passwd your_username
3. Install MQTT Client on Raspberry Pi Pico W:
Use a MicroPython MQTT library, such as umqtt.simple or umqtt.robust, to implement MQTT on the Raspberry Pi Pico W.
4. Python Script on Raspberry Pi 3:
Install the Python MQTT client library:

pip install paho-mqtt
Write a Python script on Raspberry Pi 3 to publish messages:


import paho.mqtt.publish as publish

broker_address = "your_broker_address"
port = 1883
topic = "your_topic"
message = "Hello from Raspberry Pi 3"

publish.single(topic, message, hostname=broker_address, port=port, auth={'username':"your_username", 'password':"your_password"})
5. Python Script on Raspberry Pi Pico W:
Write a MicroPython script on the Raspberry Pi Pico W to subscribe to messages:

from umqtt.simple import MQTTClient
import time

broker_address = "your_broker_address"
topic = "your_topic"
client_id = "your_client_id"
username = "your_username"
password = "your_password"

def callback(topic, msg):
    print(f"Received message: {msg}")

client = MQTTClient(client_id, broker_address, user=username, password=password)
client.set_callback(callback)
client.connect()

client.subscribe(topic)

while True:
    client.wait_msg()
