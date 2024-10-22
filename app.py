from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pyngrok import ngrok
import threading
import time
import psutil  # Importing psutil for system monitoring

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# GPS data dictionary with altitude and speed
gps_data = {
    'latitude': 0.0,
    'longitude': 0.0,
    'altitude': 0.0,  # Initialize to 0.0 or a predefined value
    'speed': 0.0  # Initialize to 0.0 or a predefined value
}

def start_ngrok():
    # Start Ngrok tunnel
    public_url = ngrok.connect(8080)
    print(f"Ngrok tunnel \"{public_url}\" is running...")

    # Keep the Ngrok service running
    while True:
        time.sleep(60)  # Sleep to keep the thread alive

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
