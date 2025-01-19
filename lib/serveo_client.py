import subprocess
import threading
import logging
from lib.email_sender import *
import os
import time

# Funzione per avviare Serveo con o senza sottodominio specifico
def start_serveo(port, retries=10, retry_delay=5, custom_subdomain=True):
    for attempt in range(retries):
        try:
            subdomain_arg = (
                f"mysubdomain.serveo.net:80:localhost:{port}"
                if custom_subdomain
                else f"80:localhost:{port}"
            )

            logging.info(f"Attempt {attempt + 1} to start Serveo.")
            serveo_process = subprocess.Popen(
                ["/usr/bin/ssh", "-vvv", "-i", "/home/lillo97/.ssh/serveo_key", "-tt",
                 "-R", subdomain_arg, 
                 "serveo.net", "-o", "StrictHostKeyChecking=no"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            serveo_link = None

            while True:
                output = serveo_process.stdout.readline()
                if output.strip():
                    logging.info(f"Output: {output.strip()}")
                    if "Forwarding HTTP traffic" in output:
                        serveo_link = output.split("Forwarding HTTP traffic from")[-1].strip()
                        logging.info(f"Serveo link: {serveo_link}")

                        # Send email or other notification
                        subject = "Your Serveo Link"
                        body = f"Ciao,\n\nEcco il tuo link al tunnel Serveo: {serveo_link}\n\nSaluti"
                        send_email(subject, body)
                        return serveo_link
                elif serveo_process.poll() is not None:
                    logging.error("Serveo process ended unexpectedly.")
                    break
                
                time.sleep(0.5)

        except Exception as e:
            error_output = serveo_process.stderr.read()
            logging.error(f"Error during Serveo startup: {e}")
            logging.error(f"Serveo STDERR: {error_output}")

        logging.warning(f"Retrying in {retry_delay} seconds...")
        time.sleep(retry_delay)

    if custom_subdomain:
        logging.warning("Failed with custom subdomain, retrying with random subdomain.")
        return start_serveo(port, retries, retry_delay, custom_subdomain=False)
    else:
        logging.error("Failed to start Serveo after multiple attempts with random subdomain.")
        return None

def runServeoClient():
    print("Running Serveo Client...")
    port = '8080'
    serveo_thread = threading.Thread(target=start_serveo, args=(port,))
    serveo_thread.daemon = True
    serveo_thread.start()



