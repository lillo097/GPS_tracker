import time
from datetime import datetime

def monitor_time(file_path="time_log.txt"):
    """
    Monitora il tempo corrente e lo scrive in un file ogni minuto.
    """
    try:
        while True:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Scrive il tempo nel file
            with open(file_path, 'w') as file:
                file.write(current_time)
            
            time.sleep(60)  # Attende un minuto prima di aggiornare
    except Exception as e:
        print(f"Errore nel servizio di monitoraggio del tempo: {e}")
