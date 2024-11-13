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

localtunnel_link = None  # Variable to store the Localtunnel link
email_sent = False  # Flag to ensure only one email is sent


def start_localtunnel(port, subdomain):
    try:
        # Avvia il processo di LocalTunnel con il sottodominio specificato
        lt_process = subprocess.Popen(
            ["lt", "--port", str(port), "--subdomain", subdomain],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        localtunnel_link = None  # Inizializza il link di LocalTunnel

        # Legge l'output del processo per trovare l'URL generato
        while True:
            output = lt_process.stdout.readline()  # Corretto: aggiunte le parentesi
            if output == '' and lt_process.poll() is not None:
                break  # Esce se non c'è più output e il processo è terminato

            # Cerca la riga che contiene l'URL generato
            if "your url is" in output:
                public_url = output.split("is")[-1].strip()

                # Controlla se il link è già stato generato
                if localtunnel_link != public_url:
                    localtunnel_link = public_url
                    logging.info(f"\nLocaltunnel link: {public_url}\n")

                    # Recupera l'IP dalla funzione get_ip_from_html
                    url = "https://loca.lt/mytunnelpassword"
                    ip = get_ip_from_html(url)
                    runBypass(public_url)
                    print("ip", ip)

                    # Componi e invia l'email con il link del tunnel e l'IP
                    subject = "Your Localtunnel Link"
                    body = f"Ciao,\n\nEcco il tuo link al tunnel Localtunnel: {public_url}\n\nIndirizzo IP: {ip}\n\nSaluti."
                    send_email(subject, body)

                    break  # Interrompe il ciclo dopo aver trovato il primo link

    except Exception as e:
        logging.error(f"Errore durante l'avvio di Localtunnel: {e}")


port = '8000'
# Start Localtunnel in a separate thread
localtunnel_thread = threading.Thread(target=start_localtunnel(port, 'halloooooohdhhddh'))
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


def runApp():
    try:
        app.run(host='0.0.0.0', port=int(port), debug=False, use_reloader=False)
    except KeyboardInterrupt:
        logging.info("Shutting down server.")



