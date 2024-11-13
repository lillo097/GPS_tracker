import requests
from bs4 import BeautifulSoup
import time

def get_ip_from_html(url):
    try:
        response_text = ""
        ip_address = ""

        # Continua a richiedere il contenuto finchÃ© non si ottiene una risposta valida
        while not response_text or not ip_address:
            response = requests.get(url)
            response.raise_for_status()  # Verifica che la richiesta sia andata a buon fine

            response_text = response.text.strip()
            soup = BeautifulSoup(response_text, 'html.parser')

            # Verifica che il tag <body> sia presente
            if soup.body:
                ip_address = soup.body.get_text(strip=True)
                if ip_address:  # Verifica che ci sia un contenuto valido
                    print(f"Indirizzo IP recuperato: {ip_address}")
                    return ip_address
            elif response.text:
                ip_address = response.text
                return ip_address
            else:
                print("Il tag <body> non Ã¨ stato trovato. Riprovo...")

            # Attendi qualche secondo prima di riprovare per evitare sovraccarichi
            time.sleep(2)

    except Exception as e:
        print(f"Si Ã¨ verificato un errore: {e}")





