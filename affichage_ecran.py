#ATTENTION - Actuellement l'écran s'affiche mais ne reçois rien. Debuggage en cours.

from tkinter import *
import time
import paho.mqtt.client as mqtt
import json
from paho.mqtt.client import MQTTv311
import threading

#Defintion des variables globales
temp_transmis = 0
hum_transmis = 0
lum_transmis = 0
co2_transmis = 0
#configuration du serveur broker MQTT
SERVEUR = 'localhost'

#Configuration des topics de sub
TOPICS = ['hum_temp', 'lum', 'co2']

#Fonction de depacketage des fichiers json reçu en fonction du topic
def on_message(client,userdata,message):
    global temp_transmis, hum_transmis, lum_transmis, co2_transmis
    topic = message.topic
    payload = json.loads(message.payload.decode())
    #Affichage des json dump reçu pour debuggage manuel
    print(f"Received message on topic '{topic}': {payload}")
    if topic == 'hum_temp':
        temp_transmis = payload.get('temperature', 0)
        hum_transmis = payload.get('humidite', 0)
        
    elif topic == 'lum':
        lum_transmis = payload.get('luminosite', 0)
        
    elif topic == 'co2':
        co2_transmis = payload.get('co2', 0)
        

#Creation d'un client MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv311)

#Connexion au brokeer MQTT
client.connect(SERVEUR, 1883, 60)

#Sub aux topics MQTT
for topic in TOPICS:
    client.subscribe(topic)
    
#Demarrage de la loop MQTT
mqtt_thread = threading.Thread(target=client.loop_forever)
mqtt_thread.daemon = False  #Empêche de terminer le thread lorsque le programme principal se termine
mqtt_thread.start()

def interface_change():
    global current_frame
    if current_frame == fenetre_principal_frame:
        current_frame.grid_forget()
        current_frame = notifications_frame
    else:
        current_frame.grid_forget()
        current_frame = fenetre_principal_frame
    current_frame.grid(row=0, column=0, padx=10, pady=10)
    
#récup des valeurs des capts
def get_sensor_data():
    co2_valeur = co2_transmis
    temp_valeur = temp_transmis
    hum_valeur = hum_transmis
    lum_valeur = lum_transmis
    return co2_valeur, temp_valeur, hum_valeur, lum_valeur

# mise à jour les valeurs des capts
def maj_valeurs():
    co2, temp, hum, lum = get_sensor_data()
    co2_var.set(co2)
    temp_var.set(temp)
    hum_var.set(hum)
    lum_var.set(lum)
    fenetre.after(1000, maj_valeurs)  # Mise à jour toutes les 1 seconde

# tester les seuils des capteurs et affichage
def check_thresholds():
    co2, temp, hum, lum = get_sensor_data()
    if lum > 700 and not lum_notification_displayed.get():
        ajout_notif("Fermer les vollets - Luminosité élevée")
        lum_notification_displayed.set(True)
    if temp > 25 and co2 > 50 and not temp_co2_notification_displayed.get():
        ajout_notif("Fermer la fenêtre - Température élevée et taux de CO2 élevé")
        temp_co2_notification_displayed.set(True)
    fenetre.after(1000, check_thresholds)  # Vérification toutes les 1 seconde

# ajout de notifs
def ajout_notif(comment):
    current_time = time.strftime("%H:%M:%S")
    notification_text = f"[{current_time}] {comment}"
    notifications_liste.insert(END, notification_text)

# suppression de notif
def suppr_notif():
    selected_index = notifications_liste.curselection()
    if selected_index:
        notifications_liste.delete(selected_index[0])

# Création de la fenêtre principale
fenetre = Tk()
fenetre['bg'] = 'white'
fenetre.geometry("800x480")
fenetre.title("Blue Connect")

# Frames pour les différentes interfaces
fenetre_principal_frame = Frame(fenetre)
notifications_frame = Frame(fenetre)

# Var pour stocker les valeurs des capts
co2_var = StringVar()
temp_var = StringVar()
hum_var = StringVar()
lum_var = StringVar()

# Variables pour indiquer si les notifications sont affichées
lum_notification_displayed = BooleanVar()
temp_co2_notification_displayed = BooleanVar()

# labels pour les valeurs des capts dans l'affichage pricipale'
Label(fenetre_principal_frame, text="CO2:", width=10, height=2).grid(row=0, column=0)
Label(fenetre_principal_frame, text="Température:", width=10, height=2).grid(row=1, column=0)
Label(fenetre_principal_frame, text="Humidité:", width=10, height=2).grid(row=2, column=0)
Label(fenetre_principal_frame, text="Luminosité:", width=10, height=2).grid(row=3, column=0)

Label(fenetre_principal_frame, textvariable=co2_var, width=10, height=2).grid(row=0, column=1)
Label(fenetre_principal_frame, textvariable=temp_var, width=10, height=2).grid(row=1, column=1)
Label(fenetre_principal_frame, textvariable=hum_var, width=10, height=2).grid(row=2, column=1)
Label(fenetre_principal_frame, textvariable=lum_var, width=10, height=2).grid(row=3, column=1)

# Bouton pour suppr une notif
delete_button = Button(notifications_frame, text="Supprimer Notification Sélectionnée", command=suppr_notif)

# Liste des notif
notifications_liste = Listbox(notifications_frame, width=60, height=10)
notifications_liste.grid(row=1, column=0, columnspan=2, padx=10, pady=10)


# Initialisation del'affichage
current_frame = fenetre_principal_frame
fenetre_principal_frame.grid(row=0, column=0, padx=10, pady=10)

# Mise à jour des valeurs des capts
maj_valeurs()

# Vérification des seuils des capts
check_thresholds()

# Bp pour basculer entre les interfaces
bouton_allez = Button(fenetre_principal_frame, text="Changer d'interface", command=interface_change)
bouton_allez.grid(row=4, column=0, pady=10)

# Bp pour revenir à la fenêtre principale depuis la fenêtre des notif
bouton_retour = Button(notifications_frame, text="Retour", command=interface_change)
bouton_retour.grid(row=2, column=0, columnspan=2, pady=10)

# Démarrer la boucle principale de l'interface
fenetre.mainloop()
