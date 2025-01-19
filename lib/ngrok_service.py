import logging
from pyngrok import ngrok
from lib.email_sender import *

def runNgrokService():
    # Set up logging
    #logging.basicConfig(level=logging.INFO)
    
    # Open a tunnel to port 8080
    public_url = ngrok.connect(8080)
    #print(f"Ngrok tunnel link: {public_url}")
    subject = "Your Ngrok Link"
    body = f"Ciao,\n\nEcco il tuo link al tunnel Ngrok: {public_url}\n\nSaluti"
    send_email(subject, body)
    