import serial
import time
import requests
import json
import psutil  # Libreria per monitorare le risorse di sistema
import os

# Configurazione della connessione seriale con il SIM808
url = 'http://127.0.0.1:8080/update_coordinates'
# port = '/dev/cu.usbserial-1420'  # Verifica quale porta è corretta
# baud_rate = 9600  # Velocità di comunicazione per il SIM808

# Apri la connessione seriale
#ser = serial.Serial(port, baud_rate, timeout=1)

# Funzione per inviare comandi AT e ricevere la risposta
def send_at_command(command, delay=1):
    ser.write((command + '\r').encode())  # Invia il comando
    time.sleep(delay)  # Aspetta la risposta
    response = ser.read(ser.inWaiting()).decode()  # Legge la risposta
    return response

# Funzione per monitorare l'uso di memoria e CPU
def monitor_resources():
    process = psutil.Process(os.getpid())  # Ottiene il processo corrente
    mem_info = process.memory_info()
    cpu_usage = process.cpu_percent(interval=1)
    mem_usage = mem_info.rss / (1024 ** 2)  # Memoria in MB
    return cpu_usage, mem_usage

# Accende il modulo GPS
# print("Accensione del GPS...")
# response = send_at_command('AT+CGNSPWR=1', delay=2)
# print(f"Risposta GPS: {response}")

# File JSON per salvare le coordinate
#json_file_path = 'gps_data_2secs.json'

# Funzione per salvare i dati GPS nel file JSON
def save_to_json(data):
    with open(json_file_path, 'a') as json_file:  # Apri in modalità append
        json.dump(data, json_file)
        json_file.write('\n')  # Scrivi una nuova riga per ogni entry

# try:
#     while True:
#         print("Richiesta delle informazioni GPS...")
#         response = send_at_command('AT+CGNSINF', delay=1)
#
#         # Verifica se il modulo ha un fix GPS
#         if ',1,' in response:
#             print(f"Coordinate GPS ricevute: {response}")
#
#             # Parsing delle coordinate
#             parts = response.split(',')
#             latitude = parts[3]  # Latitudine
#             longitude = parts[4]  # Longitudine
#             altitude = parts[7]   # Quota (m)
#             speed = parts[6]      # Velocità (km/h)
#
#             data = {
#                 'latitude': latitude,
#                 'longitude': longitude,
#                 'altitude': altitude,
#                 'speed': speed
#             }
#
#             print(f"Latitudine: {latitude}, Longitudine: {longitude}, Quota: {altitude} m, Velocità: {speed} km/h")
#
#             # Invia le coordinate al server Flask
#             response = requests.post(url, json=data)
#
#             # Salva le coordinate nel file JSON
#             save_to_json(data)
#
#             # Stampa le coordinate inviate per debug
#             print(f"Inviate nuove coordinate: Latitudine = {latitude}, Longitudine = {longitude}, Quota = {altitude} m, Velocità = {speed} km/h")
#
#         else:
#             print("Ancora in attesa di un fix GPS...")
#
#         # Monitoraggio delle risorse
#         cpu_usage, mem_usage = monitor_resources()
#         print(f"Uso CPU: {cpu_usage}%, Uso RAM: {mem_usage} MB")
#
#         time.sleep(2)  # Attendi 2 secondi prima di inviare nuovamente il comando

# try:
#     while True:
#         with open('/Users/liviobasile/Documents/Machine Learning/gitRepos/GPS_tracker/lib/gps_data_2secs.json',
#                   encoding='utf8') as f:
#             for row in f:
#                 data = json.loads(row)
#                 response = requests.post(url, json=data)
#
#                 time.sleep(2)
#
# except KeyboardInterrupt:
#     print("Interruzione da parte dell'utente. Chiusura della connessione seriale.")
#
# finally:
#     ser.close()

def get_project_path(*subdirs):

    current_dir = os.path.dirname(os.path.abspath(__file__))
    ING_dev_folder = current_dir.replace("\lib", "")
    full_path = os.path.join(ING_dev_folder, *subdirs)

    return full_path

print(get_project_path('gps_data_2secs.json'))

with open(get_project_path('gps_data_2secs.json'), 'r') as json_file:
    print(json_file.read())
