import subprocess
import time

def run_app_py():
    """Esegue il comando per avviare app.py in background"""
    print("Esecuzione di app.py in background...")
    # Avvia app.py in background
    subprocess.Popen(["python", "app.py"])

def run_ublox_py():
    """Esegue il comando per avviare ublox.py"""
    print("Esecuzione di ublox.py...")
    subprocess.run(["python", "lib/ublox.py"])

if __name__ == "__main__":
    # Esegui app.py in background
    run_app_py()

    # Aspetta 15 secondi
    print("Attendi 15 secondi...")
    time.sleep(15)

    # Esegui ublox.py
    run_ublox_py()
