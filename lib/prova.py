import serial
import time
import re
import requests  # Import requests to send data to a server
import time
from datetime import datetime


def convert_latitude(lat, direction):
    """Converts latitude from NMEA format to decimal degrees."""
    if lat:
        # Match and extract degrees and minutes
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
        # Match and extract degrees and minutes
        match = re.match(r'(\d{3})(\d{2}\.\d+)', lon)
        if match:
            degrees = float(match.group(1))
            minutes = float(match.group(2))
            decimal_lon = degrees + minutes / 60.0
            return decimal_lon if direction == 'E' else -decimal_lon
    return None

def parse_nmea_sentences(nmea_sentences):
    """Parses a list of NMEA sentences and aggregates useful information."""
    data = {}

    for nmea_sentence in nmea_sentences:
        parts = nmea_sentence.split(',')

        if parts[0] == '$GNGGA':  # Global Positioning System Fix Data
            data['fix_time'] = parts[1]
            data['latitude'] = convert_latitude(parts[2], parts[3])  # Convert latitude
            data['longitude'] = convert_longitude(parts[4], parts[5])  # Convert longitude
            data['fix_quality'] = parts[6]
            data['num_satellites'] = parts[7]
            data['horizontal_dilution'] = parts[8]
            data['altitude'] = parts[9]
            data['altitude_units'] = parts[10]

        elif parts[0] == '$GNRMC':  # Recommended Minimum Specific GPS Data
            data['fix_time'] = parts[1]
            data['status'] = parts[2]
            data['latitude'] = convert_latitude(parts[3], parts[4])  # Convert latitude
            data['longitude'] = convert_longitude(parts[5], parts[6])  # Convert longitude
            data['speed_over_ground'] = parts[7]
            data['course_over_ground'] = parts[8]
            data['date'] = parts[9]

        elif parts[0] == '$GNVTG':  # Course over ground and Ground speed
            data['course_over_ground'] = parts[1]
            data['speed_knots'] = parts[5]
            data['speed_kmh'] = parts[7]

    #print(data)
    return data

def print_gps_data(data):
    """Prints GPS data in a formatted way."""
    print("GPS Data:")
    for key, value in data.items():
        print(f"{key.replace('_', ' ').capitalize()}: {value}")
    print("\n" + "-"*20 + "\n")

def send_to_flask(data):
    """Send the parsed GPS data to Flask."""
    # data_to_send = {
    #     'latitude': data['latitude'],
    #     'longitude': data['longitude'],
    #     'altitude': data['altitude'],
    #     'Speed kmh': data['Speed kmh'],
    # }
    print(data)
    url = 'http://127.0.0.1:8080/update_coordinates'  # Replace with your actual Flask server URL
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Data successfully sent to Flask!")
    else:
        print(f"Failed to send data: {response.status_code}")


serial_port = '/dev/cu.usbserial-1420'
"""Reads and returns GPS data from the NEO-M8N module in an infinite loop."""
"""Reads and displays GPS information from the NEO-M8N module."""
try:
    # Open the serial port
    with serial.Serial(serial_port, baudrate=9600, timeout=1) as ser:
        print("Listening for GPS data...")

        # Create a dictionary to hold aggregated GPS data
        aggregated_data = {}

        buffer = []
        index = 0
        while True:
            try:
                # Read a line of data from the GPS module
                line = ser.readline().decode('ascii', errors='replace').strip()
                if line.startswith('$'):
                    buffer.append(line)

                    # Check if we have at least 3 sentences to parse
                    if len(buffer) >= 3:
                        # Parse the accumulated NMEA sentences
                        data = parse_nmea_sentences(buffer)

                        buffer.clear()  # Clear buffer for the next batch of sentences

                        # Merge the data into the aggregated data dictionary
                        aggregated_data.update(data)

                        # Print the aggregated GPS data
                        current_time = time.time()

                        # Format the time to HH:MM
                        formatted_time = datetime.fromtimestamp(current_time).strftime('%H:%M:%S')
                        aggregated_data['time'] = formatted_time
                        aggregated_data['index'] = index
                        if aggregated_data:
                            print_gps_data(aggregated_data)
                            send_to_flask(aggregated_data)

                # Wait a bit before reading the next line
                time.sleep(0.5)
                index += 1

            except KeyboardInterrupt:
                print("Stopping GPS data reading.")
                break

except serial.SerialException as e:
    print(f"Error opening serial port: {e}")






# Specify the port name here. For example: 'COM3' on Windows or '/dev/ttyUSB0' on Linux


