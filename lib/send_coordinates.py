# import requests
# import time
# import random
#
# # URL dell'API per l'aggiornamento delle coordinate
# url = 'http://127.0.0.1:5000/update_coordinates'
#
# while True:
#     # Simulazione di coordinate GPS
#     latitude = random.uniform(-90, 90)
#     longitude = random.uniform(-180, 180)
#
#     data = {'latitude': latitude, 'longitude': longitude}
#
#     # Invia le coordinate al server Flask
#     response = requests.post(url, json=data)
#
#     print(f"Inviate nuove coordinate: {latitude}, {longitude}")
#     time.sleep(10)  # Attendi 2 secondi prima di inviare altre coordinate
#

import requests
import time
import random

# URL dell'API per l'aggiornamento delle coordinate
url = 'http://127.0.0.1:8080/update_coordinates'


# Funzione per simulare un piccolo spostamento
# def generate_new_coordinates(lat, lon):
#     # Delta rappresenta il piccolo spostamento in latitudine e longitudine
#     delta_lat = random.uniform(0.00001, 0.00005)  # Spostamento verticale (latitudine)
#     delta_lon = random.uniform(0.00001, 0.00005)  # Spostamento orizzontale (longitudine)
#
#     # Simulare il movimento in avanti o indietro in modo controllato
#     direction_lat = random.choice([1, -1])  # 1 = avanti, -1 = indietro
#     direction_lon = random.choice([1, -1])  # 1 = destra, -1 = sinistra
#
#     # Aggiorna le coordinate con i piccoli cambiamenti
#     new_lat = lat + (delta_lat * direction_lat)
#     new_lon = lon + (delta_lon * direction_lon)
#
#     return new_lat, new_lon
#
#
# while True:
#     # Genera nuove coordinate vicine per simulare il movimento
#     latitude, longitude = generate_new_coordinates(latitude, longitude)
#
#     # Crea il payload con le nuove coordinate
#     data = {'latitude': latitude, 'longitude': longitude}
#
#     # Invia le coordinate al server Flask
#     response = requests.post(url, json=data)
#
#     # Stampa le coordinate inviate per il debug
#     print(f"Inviate nuove coordinate: Latitudine = {latitude}, Longitudine = {longitude}")
#
#     # Attendi 2 secondi prima di inviare nuove coordinate
#     time.sleep(10)


