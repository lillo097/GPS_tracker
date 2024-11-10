import serial
import time
import re
import requests
from datetime import datetime
import serial.tools.list_ports
import json
import threading  # Per inviare i dati senza interrompere la lettura seriale


def convert_latitude(lat, direction):
    """Converts latitude from NMEA format to decimal degrees."""
    if lat:
        match = re.match(r'(\d{2})(\d{2}\.\d+)', lat)
        if match:
            degrees = float(match.group(1))
            minutes = float(match.group(2))
            decimal_lat = degrees + minutes / 60.0
            return decimal_lat if direction == 'N' else -decimal_lat
    return None


def convert_longitude(lon, direction):
    """Converts longitude from NMEA format to decimal degrees."""
    if lon:
        match = re.match(r'(\d{3})(\d{2}\.\d+)', lon)
        if match:
            degrees = float(match.group(1))
            minutes = float(match.group(2))
            decimal_lon = degrees + minutes / 60.0
            return decimal_lon if direction == 'E' else -decimal_lon
    return None


def parse_nmea_sentences(nmea_sentence):
    """Parses a single NMEA sentence and returns useful information."""
    data = {}
    parts = nmea_sentence.split(',')

    # Controlla che ci siano abbastanza parti nella riga NMEA
    if len(parts) < 6:
        print("Riga NMEA incompleta:", nmea_sentence)
        return None

    if nmea_sentence.startswith('$GNGGA'):  # Global Positioning System Fix Data
        if len(parts) >= 10:  # Assicurati che ci siano almeno 10 campi per il GNGGA
            data['fix_time'] = parts[1]
            data['latitude'] = convert_latitude(parts[2], parts[3])
            data['longitude'] = convert_longitude(parts[4], parts[5])
            data['fix_quality'] = parts[6]
            data['num_satellites'] = parts[7]
            data['altitude'] = parts[9]

    elif nmea_sentence.startswith('$GNRMC'):  # Recommended Minimum Specific GPS Data
        if len(parts) >= 10:  # Assicurati che ci siano almeno 10 campi per il GNRMC
            data['fix_time'] = parts[1]
            data['status'] = parts[2]
            data['latitude'] = convert_latitude(parts[3], parts[4])
            data['longitude'] = convert_longitude(parts[5], parts[6])
            data['speed_over_ground'] = parts[7]
            data['course_over_ground'] = parts[8]
            data['date'] = parts[9]

    return data


def print_gps_data(data):
    """Prints GPS data in a formatted way."""
    print("GPS Data:")
    for key, value in data.items():
        print(f"{key.replace('_', ' ').capitalize()}: {value}")
    print("\n" + "-" * 20 + "\n")


def send_to_flask(data):
    """Send the parsed GPS data to Flask."""
    url = 'http://127.0.0.1:8080/update_coordinates'  # Flask server URL
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Data successfully sent to Flask!")
    else:
        print(f"Failed to send data: {response.status_code}")


def write_to_json(data, filename="gps_log.json"):
    """Appends GPS data to a JSON file."""
    log_data = {
        "timestamp": data["time"],
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude")
    }
    with open(filename, "a") as json_file:
        json.dump(log_data, json_file)
        json_file.write("\n")

ports = serial.tools.list_ports.comports()
list_of_ports = [port.device for port in ports]
serial_port = list_of_ports[-1]

try:
    with serial.Serial(serial_port, baudrate=9600, timeout=1) as ser:  # Imposta baudrate alto
        ser.reset_input_buffer()
        print("Listening for GPS data...")
        index = 0
        while True:
            line = ser.readline().decode('ascii', errors='replace').strip()
            if line.startswith('$GNGGA') or line.startswith('$GNRMC'):  # Solo dati rilevanti
                data = parse_nmea_sentences(line)
                if data:
                    current_time = time.time()
                    formatted_time = datetime.fromtimestamp(current_time).strftime('%H:%M:%S')
                    data['time'] = formatted_time
                    data['index'] = index
                    print_gps_data(data)

                    # Invia dati al server Flask in un thread separato
                    threading.Thread(target=send_to_flask, args=(data,)).start()
                    write_to_json(data)

                index += 1
            # Riduci il ritardo tra letture
            time.sleep(0.1)

except serial.SerialException as e:
    print(f"Error opening serial port: {e}")