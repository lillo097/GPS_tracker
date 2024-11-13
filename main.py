import threading
import time
from lib.ublox import runUblox
from lib.app import runApp

def run_flask():
    # Disabilita il reloader per evitare problemi di threading
    
    #time.sleep(60)
    runApp()

def run_gps():
    
    #time.sleep(30)
    runUblox()

if __name__ == "__main__":
    # Avvia runApp in un thread separato senza reloader
    print("Attendi 60 secondi per avviare correttamente il WI-FI")
    time.sleep(30)
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Esegui runUblox dopo 15 secondi in un altro thread
    print("Attendi 30 secondi sto avviando il GPS")
    time.sleep(30)
    gps_thread = threading.Thread(target=run_gps)
    gps_thread.start()

    # Unisci i thread per assicurarsi che entrambi completino l'esecuzione
    flask_thread.join()
    gps_thread.join()
