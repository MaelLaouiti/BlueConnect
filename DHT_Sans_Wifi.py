import requests
import time
import Adafruit_DHT
import paho.mqtt.client as mqtt
import json
from paho.mqtt.client import MQTTv311

#Configuration du serveur broker MQTT
SERVEUR = '169.254.3.30'
#Intervale de capture et d'envoi des donnees
INTERVALE = 5
next_reading = time.time()
#Configuration du packet envoye à la carte
site_data = {'temperature site': 0, 'humidite site' : 0, 'information site' : 0}
sensor_data = {'temperature' : 0, 'humidite' : 0, 'information' : 0}

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv311)

#Connection au Pi3 via le port MQTT par defaut and un keepalive de 60s (temps d'abandon)
client.connect(SERVEUR, 1883, 60)
client.loop_start()

# URL du site météo d'Annecy
sensor = Adafruit_DHT.DHT22
pin = 4 # pin 7 du Raspberry PI donc GPIO4
# Faire une requête GET pour récupérer le contenu de la page
temperatureSite = 15
humiditySite = 80
temperatureCible = 20
# Vérifier si la requête s'est bien passée
while True:
        
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    print('Température = {0:0.1f}C  Humidité = {1:0.1f}%'.format(temperature, humidity))
    if humidity is not None and temperature is not None:
         if temperature < temperatureCible :
            print('Allumer le chauffage et/ou fermer les fenêtres')
            sensor_data['information'] = 'Allumer le chauffage et/ou fermer les fenêtres'
         if temperature > temperatureCible :
             if temperatureSite > temperature :
                 print('Eteindre le chauffage et/ou fermer les fenêtres')
                 sensor_data['information'] = 'Eteindre le chauffage et/ou fermer les fenêtres'
         if (humidity > 60 and temperature > temperatureCible and temperature < temperatureCible):
             if humiditySite > humidity :
                 print('Fermer les fenêtres')
                 sensor_data['information'] = 'Fermer les fenêtres'
             if humiditySite < humidity :
                 print('Ouvrir les fenêtres')
                 sensor_data['information'] = 'Ouvrir les fenêtres'
         if (humidity < 40 and temperature > temperatureCible and temperature < temperatureCible):
             if humiditySite > humidity :
                print('Ouvrir les fenêtres')
                sensor_data['information'] = 'Ouvrir les fenêtres'
             if humiditySite < humidity :
                print('Fermer les fenêtres')
                sensor_data['information'] = 'Fermer les fenêtres'
    sensor_data['temperature'] = temperature
    sensor_data['humidite'] = humidity  
    #Envois des donnees capteurs au Deck
    client.publish('hum_temp',json.dumps(sensor_data),1)  

    next_reading += INTERVALE
    sleep_time = next_reading-time.time()
    if sleep_time > 0:
        time.sleep(sleep_time)

client.loop_stop()
client.disconnect()
