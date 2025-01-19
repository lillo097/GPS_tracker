from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import threading
import time
import os
import signal
import logging
import requests
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# GPS data dictionary with altitude and speed
gps_data = {
    "latitude": 0.0,  # Decimal degrees (positive for North, negative for South)
    "longitude": 0.0,  # Decimal degrees (positive for East, negative for West)
    "speed_over_ground": 0.0,  # Speed in kilometers per hour
    "course_over_ground": 0.0,  # Course in degrees (0-360, relative to true north)
    "altitude": 0.0,  # Altitude in meters
    "num_satellites": 0.0  # Number of satellites currently used for the fix
}

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

@app.route('/shutdown', methods=['GET'])
def shutdown():
    """Gracefully shutdown the Flask server."""
    pid = os.getpid()  # Get the process ID of the running server
    print(f"Shutting down server with PID {pid}...")
    os.kill(pid, signal.SIGINT)  # Send SIGINT to the current process
    return 'Server shutting down...'

def stop_flask_server():
    """Send a shutdown request after a delay."""
    time.sleep(10)  # Wait for 30 seconds before stopping
    print("Sending shutdown request to Flask server...")
    try:
        response = requests.get('http://127.0.0.1:8080/shutdown')  # Send request to shutdown endpoint
        print("Server shutdown response:", response.text)
    except requests.exceptions.ConnectionError:
        print("Server already shut down.")

def runApp():
    try:
        port = '8080'
        # Start Flask server
        app.run(host='0.0.0.0', port=int(port), debug=False, use_reloader=False)
    
    except KeyboardInterrupt:
        pass

    # Initiating shutdown after 30 seconds
    




