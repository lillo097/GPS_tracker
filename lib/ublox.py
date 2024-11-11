import serial
import time
import re
import requests
from datetime import datetime
import serial.tools.list_ports
import json
import threading
from queue import Queue  # Importa Queue

# Funzioni per la conversione e il parsing
def convert_latitude(lat, direction):
    if lat:
        match = re.match(r'(\d{2})(\d{2}\.\d+)', lat)
        if match:
            degrees = float(match.group(1))
            minutes = float(match.group(2))
            decimal_lat = degrees + minutes / 60.0
            return decimal_lat if direction == 'N' else -decimal_lat
    return None

def convert_longitude(lon, direction):
    if lon:
        match = re.match(r'(\d{3})(\d{2}\.\d+)', lon)
        if match:
            degrees = float(match.group(1))
            minutes = float(match.group(2))
            decimal_lon = degrees + minutes / 60.0
            return decimal_lon if direction == 'E' else -decimal_lon
    return None

def parse_nmea_sentences(nmea_sentence):
    data = {}
    parts = nmea_sentence.split(',')

    if len(parts) < 6:
        print("Riga NMEA incompleta:", nmea_sentence)
        return None

    if nmea_sentence.startswith('$GNGGA'):
        if len(parts) >= 10:
            data['fix_time'] = parts[1]
            data['latitude'] = convert_latitude(parts[2], parts[3])
            data['longitude'] = convert_longitude(parts[4], parts[5])
            data['fix_quality'] = parts[6]
            data['num_satellites'] = parts[7]
            data['altitude'] = parts[9]
    elif nmea_sentence.startswith('$GNRMC'):
        if len(parts) >= 10:
            data['fix_time'] = parts[1]
            data['status'] = parts[2]
            data['latitude'] = convert_latitude(parts[3], parts[4])
            data['longitude'] = convert_longitude(parts[5], parts[6])
            data['speed_over_ground'] = parts[7]
            data['course_over_ground'] = parts[8]
            data['date'] = parts[9]

    return data

def print_gps_data(data):
    print("GPS Data:")
    for key, value in data.items():
        print(f"{key.replace('_', ' ').capitalize()}: {value}")
    print("\n" + "-" * 20 + "\n")

def send_to_flask(data):
    url = 'http://127.0.0.1:8080/update_coordinates'
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Data successfully sent to Flask!")
    else:
        print(f"Failed to send data: {response.status_code}")

def write_to_json(data, filename="gps_log.json"):
    with open(filename, "a") as json_file:
        json.dump(data, json_file)
        json_file.write("\n")

# Inizializza la coda per gestire i dati GPS
q = Queue()

# Impostazione della porta seriale
ports = serial.tools.list_ports.comports()
list_of_ports = [port.device for port in ports]
serial_port = list_of_ports[-1]

try:
    with serial.Serial(serial_port, baudrate=10250, timeout=1) as ser: #10250
        ser.reset_input_buffer()
        print("Listening for GPS data...")
        index = 0
        data_batch = []

        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('ascii', errors='replace').strip()
                if line.startswith('$GNGGA') or line.startswith('$GNRMC'):
                    data = parse_nmea_sentences(line)
                    if data:
                        current_time = time.time()
                        formatted_time = datetime.fromtimestamp(current_time).strftime('%H:%M:%S')
                        data['time'] = formatted_time
                        data['index'] = index
                        print_gps_data(data)

                        # Aggiungi dati alla coda per l'invio a Flask
                        q.put(data)
                        send_to_flask(data)

                        # Aggiungi dati al batch per JSON
                        data_batch.append(data)
                        if len(data_batch) >= 10:
                            write_to_json(data_batch)
                            data_batch = []

                    index += 1
            else:
                print("Buffer vuoto, in attesa di nuovi dati...")
            time.sleep(0.05)

except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
