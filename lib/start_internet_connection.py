import serial
import time
import json  # Importa la libreria json

# Configura la connessione seriale
ser = serial.Serial('/dev/cu.usbserial-1420', baudrate=9600, timeout=2)  # Assicurati che la porta sia corretta

def send_command(command, delay=1):
    ser.write((command + '\r\n').encode())
    time.sleep(delay)
    response = ser.read(ser.inWaiting()).decode()
    print(f"Command: {command}, Response: {response}")  # Stampa il comando e la risposta
    return response

def interpret_signal_quality(rssi):
    if rssi == 99:
        return "Segnale non disponibile"
    elif 0 <= rssi <= 9:
        return "Segnale debole"
    elif 10 <= rssi <= 14:
        return "Segnale moderato"
    elif 15 <= rssi <= 19:
        return "Buona qualità"
    elif 20 <= rssi <= 31:
        return "Ottima qualità"
    else:
        return "Valore RSSI non valido"

# Funzione per ottenere l'indirizzo IP
def get_ip():
    ip_response = send_command('AT+CIFSR')
    # Rimuovi eventuali spazi e il prefisso "CIFSR: "
    return ip_response.strip().replace('CIFSR: ', '')

# Funzione per salvare i dati in un file JSON
def save_to_json(data, json_file_path='signal_quality.json'):
    with open(json_file_path, 'a', encoding='utf-8') as json_file:  # Apri in modalità append
        json.dump(data, json_file)
        json_file.write('\n')  # Scrivi una nuova riga per ogni entry

# Inizializza il modulo
print(send_command('AT'))  # Verifica la connessione
print(send_command('AT+CPIN=7030'))  # Inserisci il tuo PIN
print(send_command('AT+CREG?'))  # Controlla la registrazione nella rete
print(send_command('AT+CGATT=1'))  # Attiva la registrazione nella rete

# Configura l'APN
print(send_command('AT+CSTT="internet.wind","",""'))  # Configura l'APN per WIND

# Attiva la connessione
print(send_command('AT+CIICR'))  # Attiva la connessione
print(get_ip())  # Ottieni l'indirizzo IP iniziale

# Ciclo per controllare la qualità del segnale ogni 2 secondi
try:
    while True:
        signal_quality = send_command('AT+CSQ')

        # Controlla se la risposta contiene i dati previsti
        if 'CSQ' in signal_quality:
            parts = signal_quality.split(":")[1].strip().split(",")
            rssi_value = int(parts[0])
            quality_description = interpret_signal_quality(rssi_value)

            # Ottieni l'indirizzo IP corrente
            current_ip = get_ip()

            print("Qualità del segnale:", quality_description)
            print("Indirizzo IP corrente:", current_ip)

            # Dati da salvare
            data = {
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                'rssi': rssi_value,
                'quality': quality_description,
                'ip_address': current_ip
            }

            # Salva i dati nel file JSON
            save_to_json(data)
        else:
            print("Risposta inaspettata dal comando AT+CSQ:", signal_quality)

        time.sleep(2)  # Attendi 2 secondi prima di ripetere

except KeyboardInterrupt:
    print("Interruzione da parte dell'utente. Chiusura della connessione seriale.")

finally:
    # Chiudi la connessione seriale alla fine
    ser.close()
