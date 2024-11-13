import threading
import time
from lib.ublox import runUblox
from lib.app import runApp

def run_flask():
    # Disabilita il reloader per evitare problemi di threading
    runApp()

def run_gps():
    print("Attendi 15 secondi...")
    time.sleep(15)
    runUblox()

if __name__ == "__main__":
    # Avvia runApp in un thread separato senza reloader
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Esegui runUblox dopo 15 secondi in un altro thread
    gps_thread = threading.Thread(target=run_gps)
    gps_thread.start()

    # Unisci i thread per assicurarsi che entrambi completino l'esecuzione
    flask_thread.join()
    gps_thread.join()
