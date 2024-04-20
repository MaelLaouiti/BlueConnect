import Adafruit_DHT
import time

sensor = Adafruit_DHT.DHT22
pin = 4 # pin 7 du Raspberry PI donc GPIO4

while True :
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        if humidity < 20 :
            print('Température={0:0.1f}*C  Humidité={1:0.1f}%, Taux d\'humidité beaucoup trop faible !'.format(temperature, humidity))
        elif humidity < 40 :
            print('Température={0:0.1f}*C  Humidité={1:0.1f}%, Taux d\'humidité trop faible !'.format(temperature, humidity))
        elif humidity < 60 :
            print('Température={0:0.1f}*C  Humidité={1:0.1f}%, Taux d\'humidité correct !'.format(temperature, humidity))
        elif humidity < 80 :
            print('Température={0:0.1f}*C  Humidité={1:0.1f}%, Taux d\'humidité trop élevé !'.format(temperature, humidity))
        else :
            print('Température={0:0.1f}*C  Humidité={1:0.1f}%, Taux d\'humidité beaucoup trop élevé !'.format(temperature, humidity))
    else:
        print('Failed to get reading. Try again!')            
    time.sleep(1)
