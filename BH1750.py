import smbus
import time
import paho.mqtt.client as mqtt
import json
#import random
from paho.mqtt.client import MQTTv311

#Configuration du serveur broker MQTT
SERVEUR = '169.254.3.30'
#Intervale de capture et d'envoi des donnees en secondes
INTERVALE = 5
next_reading = time.time()
#Configuration du packet envoye à la carte
sensor_data = {'luminosite' : 0}

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv311)

# Define I2C address for BH1750 sensor
BH1750_ADDR = 0x23

# Define command to measure continuously in high resolution mode
CONTINUOUS_HIGH_RES_MODE = 0x10

# Create an instance of the smbus module to communicate with I2C
bus = smbus.SMBus(1)

#Connection au Pi3 via le port MQTT par defaut and un keepalive de 60s (temps d'abandon)
client.connect(SERVEUR, 1883, 60)
client.loop_start()

#Fonction de test de la transmission MQTT sans materiel
#def read_light_intensity():
#	return round(random.uniform(0,100), 2)

#Function to read light intensity from the sensor
def read_light_intensity():
    # Send command to measure light intensity
    bus.write_byte(BH1750_ADDR, CONTINUOUS_HIGH_RES_MODE)
    
    # Wait for measurement to be ready (depends on the integration time)
    time.sleep(0.2)  # Adjust this value according to your sensor's integration time
    
    # Read 2 bytes of data from the sensor
    data = bus.read_i2c_block_data(BH1750_ADDR, 0x00, 2)
    
    # Convert the data to lux
    light_intensity = (data[1] + (256 * data[0])) / 1.2
    
    return light_intensity

try:
    while True:
        # Read light intensity
        intensity = read_light_intensity()
        
        # Print the light intensity
        print("Light Intensity: {} lux".format(intensity))
        sensor_data['luminosite'] = intensity
        #Publication des donnees sous forme de fichier json sur le topic 'lum' du broker MQTT
        client.publish('lum',json.dumps(sensor_data),1)
        
        # Wait for some time before taking the next measurement
        next_reading += INTERVALE
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)

except KeyboardInterrupt:
    print("Measurement stopped by the user")
client.loop_stop()
client.disconnect()
