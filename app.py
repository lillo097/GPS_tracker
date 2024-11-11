from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import threading
import time
import psutil  # For system monitoring
import json
import requests
import os
import logging
import subprocess
from email_sender import *

# Configure logging to show only INFO level (for Localtunnel link and Flask output)
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

localtunnel_link = None  # Variable to store the Localtunnel link
email_sent = False  # Flag to ensure only one email is sent


def start_localtunnel():
    """Start the Localtunnel process to expose the server publicly."""
    global localtunnel_link, email_sent
    try:
        # Run Localtunnel on port 8080
        lt_process = subprocess.Popen(["lt", "--port", "8080"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            output = lt_process.stdout.readline().decode()
            if output == '' and lt_process.poll() is not None:
                break  # Exit if no more output and process has finished
            if "your url is" in output:
                public_url = output.split("is")[-1].strip()

                if localtunnel_link != public_url:  # Check if the link has already been generated
                    localtunnel_link = public_url
                    logging.info(f"\nLocaltunnel link: {public_url}\n")

                    subject = "Your Localtunnel Link"
                    body = f"Ciao,\n\nEcco il tuo link al tunnel Localtunnel: {public_url}\n\nSaluti."
                    #send_email(subject, body)  # Chiamata alla funzione send_email per inviare l'email

                    break  # Stop after finding the first link

    except Exception as e:
        logging.error(f"Error starting Localtunnel: {e}")



# Start Localtunnel in a separate thread
localtunnel_thread = threading.Thread(target=start_localtunnel)
localtunnel_thread.daemon = True
localtunnel_thread.start()


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


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8080, debug=True)
    except KeyboardInterrupt:
        logging.info("Shutting down server.")
