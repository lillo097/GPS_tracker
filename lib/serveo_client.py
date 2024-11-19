import subprocess
import threading
import logging
from lib.email_sender import *


# Funzione per avviare Serveo senza specificare il sottodominio
def start_serveo(port):
    try:
        # Avvia il tunnel Serveo sulla porta specificata senza sottodominio
        serveo_process = subprocess.Popen(
            ["/usr/bin/ssh", "-i", "~/.ssh/serveo_key", "-tt", "-R", f"mysubdomain.serveo.net:80:localhost:{port}", "serveo.net", "-o", "StrictHostKeyChecking=no"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        serveo_link = None  # Inizializza il link di Serveo

        # Leggi l'output del processo per trovare l'URL generato
        while True:
            output = serveo_process.stdout.readline()
            if output == '' and serveo_process.poll() is not None:
                break  # Exit if there's no more output and the process is done

            if "Forwarding HTTP traffic" in output:
                serveo_link = output.split("Forwarding HTTP traffic from")[-1].strip()
                logging.info(f"\nServeo link: {serveo_link}\n")

                # Send email or perform additional actions
                subject = "Your Serveo Link"
                body = f"Ciao,\n\nEcco il tuo link al tunnel Serveo: {serveo_link}\n\nSaluti"
                send_email(subject, body)

                print(f"Serveo link: {serveo_link}")
                break  # Stop after finding the first link

    except Exception as e:
        logging.error(f"Errore durante l'avvio di Serveo: {e}")


def runServeoClient():
        print("Running Serveo Client...")
        port = '8000'
        serveo_thread = threading.Thread(target=start_serveo, args=(port,))
        serveo_thread.daemon = True
        serveo_thread.start()




