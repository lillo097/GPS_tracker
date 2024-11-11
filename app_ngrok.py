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
        if not tunnels:
            public_url = ngrok.connect(8080)
            logging.info(f"\nNgrok tunnel link: {public_url}\n")
        else:
            logging.info("Ngrok is already running.")
    except Exception as e:
        logging.error(f"Error starting Ngrok: {e}")

def stop_ngrok():
    """Stop the Ngrok tunnel gracefully."""
    try:
        ngrok.kill()
        logging.info("Ngrok tunnel stopped.")
    except Exception as e:
        logging.error(f"Error stopping Ngrok: {e}")

# Start the Ngrok service in a separate thread
ngrok_thread = threading.Thread(target=start_ngrok)
ngrok_thread.daemon = True
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
    process = psutil.Process()
    memory_info = process.memory_info()
    ram_usage = {
        'rss': memory_info.rss / (1024 * 1024),  # Resident Set Size in MB
        'percent': process.memory_percent()  # Percentage of RAM used by the process
    }
    return jsonify(ram_usage)

def send_coordinates(event):
    """Send GPS coordinates to the Flask app in a continuous loop."""
    url = 'http://127.0.0.1:8080/update_coordinates'
    gps_generator = gps_info(serial_port)  # Assuming serial_port is defined globally

    while not event.is_set():
        try:
            gps_data = next(gps_generator)
            response = requests.post(url, json=gps_data)
            if response.status_code == 200:
                logging.info("Coordinates sent successfully.")
            else:
                logging.warning(f"Failed to send coordinates. Status: {response.status_code}")
            event.wait(2)  # Wait for 2 seconds or exit if event is set
        except (requests.ConnectionError, json.JSONDecodeError) as e:
            logging.error(f"Error encountered: {e}")
            event.wait(5)  # Retry after delay on error
        except StopIteration:
            logging.error("GPS data generator stopped.")
            break

if __name__ == '__main__':
    try:
        # Start the coordinates-sending function in a separate thread
        stop_event = threading.Event()
        coordinates_thread = threading.Thread(target=send_coordinates, args=(stop_event,))
        coordinates_thread.start()

        app.run(host='0.0.0.0', port=8080, debug=True)
    except KeyboardInterrupt:
        logging.info("Shutting down server.")
    finally:
        stop_event.set()  # Signal the coordinates thread to stop
        coordinates_thread.join()  # Wait for the thread to finish
        stop_ngrok()  # Stop Ngrok when server exits
