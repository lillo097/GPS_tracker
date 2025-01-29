import threading
import time
from lib.ublox import runUblox
from lib.app import runApp
from lib.serveo_client import runServeoClient
from lib.local_tunnel_client import runLocaltunnelClient
from lib.stop_services import runHtmlService
from lib.ngrok_service import runNgrokService
from lib.debugging_service import monitor_time
from lib.multimeter import run_multimeter
from lib.telebot_service import run_bot
import socket
import signal
import os
os.environ["VIRTUAL_ENV"] = "/home/lillo97/GPS_tracker/venv"

def wait_for_internet(host="8.8.8.8", port=53, timeout=3, max_wait=120):
    start_time = time.time()
    while True:
        try:
            socket.create_connection((host, port), timeout=timeout)
            print("Internet is available.")
            break
        except OSError:
            elapsed_time = time.time() - start_time
            print(f"Waiting for internet... {int(elapsed_time)}s elapsed")
            if elapsed_time > max_wait:
                print("Internet not available within the timeout. Rebooting...")
                os.system("sudo reboot")
                break
            time.sleep(5)

def shutdown_handler(sig, frame):
    os._exit(0)

if __name__ == "__main__":
    
    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)
    
    
    print("Waiting for Wi-Fi to initialize...")
    wait_for_internet()

    print('Running Flask client...')
    flask_thread = threading.Thread(target=runApp)
    flask_thread.start()
    time.sleep(15)

    #print("Running Serveo client...")
    #serveo_thread = threading.Thread(target=runServeoClient)
    #serveo_thread.start()
    #time.sleep(60)
    
    print("Running Ngrok client...")
    ngrok_service_thread = threading.Thread(target=runNgrokService)
    ngrok_service_thread.start()
    time.sleep(30)
    
    #print("Running Local Tunnel client...")
    #lt_thread = threading.Thread(target=runLocaltunnelClient)
    #lt_thread.start()
    #time.sleep(30)
    
    print("Starting GPS module...")
    gps_thread = threading.Thread(target=runUblox)
    gps_thread.start()
    time.sleep(10)
    
    print("Starting debugging service...")
    debug_thread = threading.Thread(target=monitor_time, args=("time_log.txt",))
    debug_thread.daemon = True  # Imposta il thread come demone
    debug_thread.start()
    
#    print('Starting Telegram bot service...')
 #   bot_thread = threading.Thread(target=run_bot)
  #  bot_thread.start()

#    print("Starting Multimeter service...")
 #   multimeter_thread = threading.Thread(target=run_multimeter)
  #  multimeter_thread.start()
    
    #print("Running service status check module...")
    #stop_services_thread = threading.Thread(target=runHtmlService)
    #stop_services_thread.start()
    
    flask_thread.join()
    #serveo_thread.join()
    ngrok_service_thread.join()
    gps_thread.join()
    #start_services_thread.join()
    debug_thread.join()
   # bot_thread.join()
   # multimeter_thread.join()
    
    
