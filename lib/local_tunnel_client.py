import subprocess
import threading
import logging
from lib.email_sender import send_email


# Funzione per avviare LocalTunnel
def start_localtunnel(port, subdomain):
    try:
        # Avvia il processo di LocalTunnel con il sottodominio specificato
        lt_process = subprocess.Popen(
            ["lt", "--port", str(port), "--subdomain", subdomain],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Legge l'output del processo per trovare l'URL generato
        while True:
            output = lt_process.stdout.readline()
            if output == '' and lt_process.poll() is not None:
                break

            if "your url is" in output:
                localtunnel_link = output.split("is")[-1].strip()
                logging.info(f"\nLocalTunnel link: {localtunnel_link}\n")

                # Invia email con il link
                subject = "Your LocalTunnel Link"
                body = f"Ciao,\n\nEcco il tuo link al tunnel LocalTunnel: {localtunnel_link}\n\nSaluti"
                send_email(subject, body)

                print(f"LocalTunnel link: {localtunnel_link}")
                break

    except Exception as e:
        logging.error(f"Errore durante l'avvio di LocalTunnel: {e}")


# Funzione per avviare LocalTunnel in un thread
def runLocaltunnelClient():
    port = '8000'
    subdomain = 'haloooooooooooooo'
    print("Running LocalTunnel Client...")
    localtunnel_thread = threading.Thread(target=start_localtunnel, args=(port, subdomain))
    localtunnel_thread.daemon = True
    localtunnel_thread.start()