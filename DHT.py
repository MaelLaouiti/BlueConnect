import Adafruit_DHT
import time
import paho.mqtt.client as mqtt
import json
from paho.mqtt.client import MQTTv311

#Configuration du serveur broker MQTT
SERVEUR = '169.254.3.30'
#Intervale de capture et d'envoi des donnees
INTERVALE = 5
next_reading = time.time()
#Configuration du packet envoye à la carte
sensor_data = {'temperature' : 0, 'humidite' : 0, 'information' : 0}

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv311)

#Connection au Pi3 via le port MQTT par defaut and un keepalive de 60s (temps d'abandon)
client.connect(SERVEUR, 1883, 60)
client.loop_start()

sensor = Adafruit_DHT.DHT22
pin = 4 # pin 7 du Raspberry PI donc GPIO4
try:
    while True :
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if humidity is not None and temperature is not None:
            if humidity < 20 :
                print('Température={0:0.1f}*C  Humidité={1:0.1f}%, Taux d\'humidité beaucoup trop faible !'.format(temperature, humidity))
                sensor_data['information'] = 'Taux d\'humidité beaucoup trop faible !'
            elif humidity < 40 :
                print('Température={0:0.1f}*C  Humidité={1:0.1f}%, Taux d\'humidité trop faible !'.format(temperature, humidity))
                sensor_data['information'] = 'Taux d\'humidité beaucoup trop faible !'
            elif humidity < 60 :
                print('Température={0:0.1f}*C  Humidité={1:0.1f}%, Taux d\'humidité correct !'.format(temperature, humidity))
                sensor_data['information'] = 'Taux d\'humidité beaucoup correct !'
            elif humidity < 80 :
                print('Température={0:0.1f}*C  Humidité={1:0.1f}%, Taux d\'humidité trop élevé !'.format(temperature, humidity))
                sensor_data['information'] = 'Taux d\'humidité beaucoup trop élevé !'
            else :
                print('Température={0:0.1f}*C  Humidité={1:0.1f}%, Taux d\'humidité beaucoup trop élevé !'.format(temperature, humidity))
                sensor_data['information'] = 'Taux d\'humidité beaucoup trop élevé !'
        else:
            print('Failed to get reading. Try again!')
            sensor_data['information'] = 'Failed to get reading. Try again!'

        sensor_data['temperature'] = temperature
        sensor_data['humidite'] = humidity
        #Publication des donnees sous forme de fichier json sur le topic 'hum_temp' du broker MQTT
        client.publish('hum_temp',json.dumps(sensor_data),1)

        next_reading =+ INTERVALE
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass
client.loop_stop()
client.disconnect()
