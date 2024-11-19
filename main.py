import threading
import time
from lib.ublox import runUblox
from lib.app import runApp
from lib.serveo_client import runServeoClient
from lib.local_tunnel_client import runLocaltunnelClient
import socket

def wait_for_internet(host="8.8.8.8", port=53, timeout=3):
    while True:
        try:
            socket.create_connection((host, port), timeout=timeout)
            print("Internet is available.")
            break
        except OSError:
            print("Waiting for internet...")
            time.sleep(5)

if __name__ == "__main__":
    print("Waiting for Wi-Fi to initialize...")
    wait_for_internet()

    print('Running Flask client...')
    flask_thread = threading.Thread(target=runApp)
    flask_thread.start()
    time.sleep(10)

    print("Running Serveo client...")
    serveo_thread = threading.Thread(target=runServeoClient)
    serveo_thread.start()
    time.sleep(30)
    
    #print("Running Local Tunnel client...")
    #lt_thread = threading.Thread(target=runLocaltunnelClient)
    #lt_thread.start()
    #time.sleep(30)
    

    print("Starting GPS module...")
    gps_thread = threading.Thread(target=runUblox)
    gps_thread.start()
    time.sleep(10)

    flask_thread.join()
    serveo_thread.join()
    gps_thread.join()
