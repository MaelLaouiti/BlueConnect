import Adafruit_DHT

sensor = Adafruit_DHT.DHT22

pin = '7'

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
"""
from machine import Pin
from time import sleep
import dht

capteur = dht.DHT22(Pin(23))

while True:
  try:
    sleep(1)     # le DHT22 renvoie au maximum une mesure toute les 2s
    capteur.measure()     # Recuperère les mesures du capteur
    print(f"Temperature : {capteur.temperature():.1f}°C")
    print(f"Humidite    : {capteur.humidity():.1f}%")
  except OSError as e:
    print("Echec reception")
      """
