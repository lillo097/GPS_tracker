from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import threading
import time
import psutil
import json
import requests
import os
import logging
import subprocess
from lib.email_sender import *
from lib.get_ip import *
from lib.bypass_tunnel import runBypass

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

# localtunnel_thread.start()







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


# @app.route('/ram_usage', methods=['GET'])
# def ram_usage():
#     """Returns the current RAM usage of the application."""
#     process = psutil.Process()
#     memory_info = process.memory_info()
#     ram_usage = {
#         'rss': memory_info.rss / (1024 * 1024),  # Resident Set Size in MB
#         'percent': process.memory_percent()  # Percentage of RAM used by the process
#     }
#     return jsonify(ram_usage)

import time
def runApp():
    try:
        # Porta da esporre
        port = '8000'
# Avvia Serveo in un thread separato
        app.run(host='0.0.0.0', port=int(port), debug=False, use_reloader=False)
        
    except KeyboardInterrupt:
        logging.info("Shutting down server.")



