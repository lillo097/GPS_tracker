import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Impostazioni del server SMTP (ad esempio, per Gmail)
smtp_server = "smtp.gmail.com"
smtp_port = 587
email_account = "liviobasile97@gmail.com"  # Inserisci il tuo indirizzo email
email_password = "cdir pykb nhya zlor"  # Inserisci la tua password o una password per le app se usi Gmail

def send_email(subject, body):

    msg = MIMEMultipart()
    msg['From'] = email_account
    msg['To'] = "liviobasile97@gmail.com"
    msg['Subject'] = subject

    # Aggiungi il corpo del messaggio
    msg.attach(MIMEText(body, 'plain'))

    # Connessione al server SMTP
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Crittografia
        server.login(email_account, email_password)

        # Invia l'email
        server.sendmail(email_account, "liviobasile97@gmail.com", msg.as_string())
        print("Email inviata con successo!")

    except Exception as e:
        print(f"Errore durante l'invio dell'email: {e}")
    finally:
        server.quit()
