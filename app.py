from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pyngrok import ngrok
import threading
import time
import psutil  # For system monitoring
import json
import requests
import os
import logging

# Configure logging to show only INFO level (for Ngrok link and Flask output)
logging.basicConfig(level=logging.INFO, format="%(message)s")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# GPS data dictionary with altitude and speed
gps_data = {
    'latitude': 0.0,
    'longitude': 0.0,
    'altitude': 0.0,  # Initialize to 0.0 or a predefined value
    'speed_kmh': 0.0  # Initialize to 0.0 or a predefined value
}

def start_ngrok():
    """Start the Ngrok tunnel if not already active."""
    try:
        tunnels = ngrok.get_tunnels()
        if tunnels:
            logging.info("Ngrok is already running.")
            return
        public_url = ngrok.connect(8080)
        # Only display the public URL in a simple, clear format
        print(f"\nNgrok tunnel link: {public_url}\n")
    except Exception as e:
        logging.error(f"Error starting Ngrok: {e}")

def get_project_path(*subdirs):
    """Constructs the full path from the current directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(current_dir, *subdirs)
    return full_path

# Start the Ngrok service in a separate thread
ngrok_thread = threading.Thread(target=start_ngrok)
ngrok_thread.daemon = True  # Allows the thread to exit when the main program exits
ngrok_thread.start()

@app.route('/')
def index():
    return render_template('index_iphone.html')  # Serve HTML from the templates folder

@app.route('/update_coordinates', methods=['POST'])
def update_coordinates():
    global gps_data
    data = request.get_json()
    gps_data.update(data)  # Update GPS data
    return jsonify({'status': 'success', 'message': 'Coordinates updated'})

@app.route('/get_coordinates', methods=['GET'])
def get_coordinates():
    return jsonify(gps_data)

@app.route('/ram_usage', methods=['GET'])
def ram_usage():
    """Returns the current RAM usage of the application."""
    process = psutil.Process()  # Get the current process
    memory_info = process.memory_info()  # Get memory info
    ram_usage = {
        'rss': memory_info.rss / (1024 * 1024),  # Resident Set Size in MB
        'percent': process.memory_percent()  # Percentage of RAM used by the process
    }
    return jsonify(ram_usage)


def send_coordinates():
    """Send GPS coordinates to the Flask app in a continuous loop."""
    url = 'http://127.0.0.1:8080/update_coordinates'

    # Start reading GPS data
    gps_generator = gps_info(serial_port)

    while True:
        try:
            # Get the latest GPS data from the generator
            gps_data = next(gps_generator)

            # Send the GPS data to Flask API
            response = requests.post(url, json=gps_data)
            if response.status_code == 200:
                logging.info(f"Coordinates sent successfully.")
            else:
                logging.error(f"Failed to send coordinates. Status code: {response.status_code}")

            time.sleep(2)  # Send data every 2 seconds

        except (requests.ConnectionError, json.JSONDecodeError) as e:
            logging.error(f"Error encountered: {e}")
            time.sleep(5)  # Retry after a short delay
        except StopIteration:
            logging.error("GPS data generator stopped.")
            break


# Start the coordinates-sending function in a separate thread
coordinates_thread = threading.Thread(target=send_coordinates)
coordinates_thread.daemon = True
coordinates_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
