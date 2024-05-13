import time
import smbus
import paho.mqtt.client as mqtt
import json
from paho.mqtt.client import MQTTv311

#Configuration du serveur broker MQTT
SERVEUR = '169.254.3.30'
#Intervale de capture et d'envoi des donnees
INTERVALE = 5
next_reading = time.time()
#Configuration du packet envoye à la carte
sensor_data = {'eCO2 (ppm)' : 0, 'AQI (1-5)' : 0, 'information' : 0}

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv311)

#Connection au Pi3 via le port MQTT par defaut and un keepalive de 60s (temps d'abandon)
client.connect(SERVEUR, 1883, 60)
client.loop_start()

# Define I2C address of the sensor
SENSOR_ADDR = 0x53

# Define register addresses for sensor data
AQI_REGISTER = 0x35
#TVOC_REGISTER = 0x38
ECO2_REGISTER = 0x37
#0x01, 0x20, 0x36, 0x81 = 256
#0x35 = 1
#0x37 = petites valeurs qui varient
#0x38 = grosses valeurs qui varient
#0x80 = 24577
#0x7F = 96

# Initialize I2C bus
bus = smbus.SMBus(4) # Assuming Raspberry Pi 3 uses I2C bus 1

# Function to read sensor data
def read_sensor_data(register):
    # Read 2 bytes of data from the specified register
    data = bus.read_i2c_block_data(SENSOR_ADDR, register, 2)
    # Combine the bytes into a single 16-bit value
    value = (data[0] << 8) + data[1]
    return value

while True:
    # Read sensor data
    aqi = read_sensor_data(AQI_REGISTER)
    #tvoc = read_sensor_data(TVOC_REGISTER)
    eco2 = read_sensor_data(ECO2_REGISTER)
    sensor_data['eCO2 (ppm)'] = eco2
    sensor_data['AQI (1-5)'] = aqi
    
    # Print sensor data
    print("AQI (1-5):", aqi)
    #print("TVOC (ppb):", tvoc)
    print("eCO2 (ppm):", eco2)
    print()

    if eco2 > 800 :
        print('Ouvrir les fenêtres')
        sensor_data['information'] = 'Ouvrir les fenêtres'

    #Publication des donnees sous forme de fichier json sur le topic 'co2' du broker MQTT
    client.publish('co2',json.dumps(sensor_data),1)
    
    next_reading += INTERVALE
    sleep_time = next_reading-time.time()
    if sleep_time > 0:
        time.sleep(sleep_time)

client.loop_stop()
client.disconnect()
