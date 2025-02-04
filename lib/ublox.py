import serial
import time
import re
import requests
from datetime import datetime
import json
from queue import Queue
import os
from lib.multimeter import *
#from multimeter import *

# Conversion and parsing functions
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

    def safe_float(value, default=0.0):
        try:
            return float(value) if value.strip() else default
        except ValueError:
            return default

    def safe_int(value, default=0):
        try:
            return int(value) if value.strip() else default
        except ValueError:
            return default
    
    if nmea_sentence.startswith('$GNGGA'):
        if len(parts) >= 10:
            data['fix_time'] = parts[1]
            data['latitude'] = convert_latitude(parts[2], parts[3])
            data['longitude'] = convert_longitude(parts[4], parts[5])
            data['fix_quality'] = parts[6]
            data['num_satellites'] = safe_int(parts[7])
            data['altitude'] = safe_float(parts[9])
            data['speed_over_ground'] = None
            data['course_over_ground'] = None
    elif nmea_sentence.startswith('$GNRMC'):
        if len(parts) >= 10:
            data['fix_time'] = parts[1]
            data['status'] = parts[2]
            data['latitude'] = convert_latitude(parts[3], parts[4])
            data['longitude'] = convert_longitude(parts[5], parts[6])
            data['speed_over_ground'] = safe_float(parts[7]) * 1.852
            data['course_over_ground'] = safe_float(parts[8])
            data['date'] = parts[9]
            data['num_satellites'] = None
        data['altitude'] = None

    return data

def print_gps_data(data):
    print("GPS Data:")
    for key, value in data.items():
        print(f"{key.replace('_', ' ').capitalize()}: {value}")
    print("\n" + "-" * 20 + "\n")
    
port = 8080
def send_to_flask(data):
    url = f'http://127.0.0.1:{port}/update_coordinates'
    response = requests.post(url, json=data)
    #if response.status_code == 200:
        #print("Data successfully sent to Flask!")
    #else:
        #print(f"Failed to send data: {response.status_code}")

def write_to_json(data, filename="gps_log.json"):
    with open(filename, "a") as json_file:
        json.dump(data, json_file)
        json_file.write("\n")

# Define a dictionary to store the current state of GPS data
current_data = {
    "latitude": None,
    "longitude": None,
    "speed_over_ground": None,
    "course_over_ground": None,
    "altitude": None,
    "num_satellites": None,
}

# Function to check if all required fields are populated
def is_data_complete(data):
    required_fields = ["latitude", "longitude", "speed_over_ground", "course_over_ground", "altitude", "num_satellites"]
    return all(data.get(field) is not None for field in required_fields)

def process_gps_data(data):
    global current_data

    # Update current data with the new values
    for key, value in data.items():
        if key in current_data and value is not None:
            current_data[key] = value

    # Immediately send latitude and longitude
    if current_data["latitude"] is not None and current_data["longitude"] is not None:
        send_to_flask({
            "latitude": current_data["latitude"],
            "longitude": current_data["longitude"]
        })
    
    if isinstance(data['voltage'], float):
        
        send_to_flask({
        "voltage": data['voltage'],
        "current": data['current'],
        "avg_voltage": data['avg_voltage']
    })
        

    # Check if the data is complete
    if is_data_complete(current_data):
        # Send the complete data and clear the buffer
        send_to_flask(current_data)
       # write_to_json(current_data)  # Optionally log data
        #print_gps_data(current_data)
        
        # Reset current data after sending
        current_data = {key: None for key in current_data}
        
def calculate_battery_percentage(voltage_avg, max_voltage=4.2, min_voltage=3):
    if voltage_avg <= min_voltage:
        return 0.0
    elif voltage_avg >= max_voltage:
        return 100.0
    else:
        return int(((voltage_avg - min_voltage) / (max_voltage - min_voltage)) * 100.0)
        

# Serial port for the GPS module
serial_port = '/dev/serial0'  # Adjust this for your system

file_json = 'multimeter_data.json'
if os.path.exists(file_json):
    os.remove(file_json)

def runUblox():
    shutdown_threshold = 2.85  # Imposta la soglia desiderata
    
    try:
        with serial.Serial(serial_port, baudrate=57600, timeout=1) as ser:
            ser.reset_input_buffer()
            index = 0
            v = 0
            c = 0
            i = 0

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

                            voltage, current = run_multimeter()
                            
                            if voltage <= shutdown_threshold:
                                print("Battery voltage too low! Shutting down...")
                                os.system("sudo shutdown")
                                return

                            v += voltage
                            c += current
                            
                            if i == 500:
                                i = 1
                                v = voltage
                                c = current
                            else:     
                                i += 1
                          
                            data['voltage'] = round(voltage, 2)
                            data['current'] = round(current, 2)
                            data['avg_voltage'] = calculate_battery_percentage(v / i)
                            data['avg_current'] = round((c/i), 2)
                            print('Iteration:', index)
                            if index % 1000 == 0:
                                print('----------------------------------------------------------> Writing into JSON...')
                                try:
                                    with open('battery_data.json', 'r') as f:
                                        dati = json.load(f)
                                except FileNotFoundError:
                                    dati = []
                                
                                nuovo_dato = {
                                    "avg_voltage": round(calculate_battery_percentage(v / i), 2),
                                    "avg_current": round((c/i), 2),
                                    "voltage": round(voltage, 2),
                                    "current": round(current, 2),
                                    "data_ora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                }
                                dati.append(nuovo_dato)
                                            
                                with open('battery_data.json', 'w') as f:
                                    json.dump(dati, f, indent=4)
                            if i == 0:
                                i = 1

                            print('Voltage:', round(voltage, 2))
                            print('Current:', round(current, 2))
                            print('Avg Voltage:', round(v / i, 2))
                            print('Avg Current:', round(c / i, 2))
                            print(calculate_battery_percentage(v / i), '%')
                            print('-' * 50)
                        
                            process_gps_data(data)
                            index += 1
                
                time.sleep(0.01)
    
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
#runUblox()
