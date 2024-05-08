import requests
from bs4 import BeautifulSoup
import bs4
import time
import Adafruit_DHT

# URL du site météo d'Annecy
url = "https://weather.com/fr-FR/temps/parheure/l/601b46db2f3e72e86d806343a425a9b4c3a6b1b3d506ffb051abd3cb503e6431"
sensor = Adafruit_DHT.DHT22
pin = 4 # pin 7 du Raspberry PI donc GPIO4
# Faire une requête GET pour récupérer le contenu de la page
response = requests.get(url)

# Vérifier si la requête s'est bien passée
while True:
    if response.status_code == 200:
        # Utiliser BeautifulSoup pour analyser le contenu HTML de la page
        soup = BeautifulSoup(response.content, "html.parser")

        # Trouver l'élément contenant la température actuelle
        temperature_element = soup.find("span", class_="DetailsTable--value--2YD0-")

        if temperature_element:
            temperatureBrut = temperature_element.get_text()
            print("Température actuelle à Annecy :", temperatureBrut)
        else:
            print("Impossible de trouver la température actuelle.")

        # Trouver l'élément contenant l'humidité actuelle
        humidite_element = soup.find("span", attrs={"class":"DetailsTable--value--2YD0-", "data-testid":"PercentageValue"})

        if humidite_element:
            humidityBrut = humidite_element.get_text()
            print("Humidité actuelle à Annecy :", humidityBrut)
        else:
            print("Impossible de trouver l'humidité actuelle.")
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    temperatureSite = float(temperature_element.get_text()[:2])
    humiditySite = float(humidite_element.get_text()[:2])
    if humidity is not None and temperature is not None:
         if temperature < 10 :
            print('Allumer le chauffage et/ou fermer les fenêtres')
         if temperature > 30 :
             if temperatureSite > temperature :
                 print('Eteindre le chauffage et/ou fermer les fenêtres')
             if temperatureSite < temperature :
                 print('Eteindre le chauffage et/ou ouvrir les fenêtres')
         if (humidity > 60 and temperature > 10 and temperature < 30):
             if humiditySite > humidity :
                 print('Fermer les fenêtres')
             if humiditySite < humidity :
                 print('Ouvrir les fenêtres')
         if (humidity < 40 and temperature > 10 and temperature < 30):
             if humiditySite > humidity :
                print('Ouvrir les fenêtres')
             if humiditySite < humidity :
                print('Fermer les fenêtres')
    print('Température = {0:0.1f}C  Humidité = {1:0.1f}%'.format(temperature, humidity))    
    time.sleep(0.5)
