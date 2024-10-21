import os
import serial
import time

# Configura la connessione seriale al SIM808
ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)

def send_at_command(command, timeout=1):
    ser.write((command + '\r').encode())
    time.sleep(timeout)
    response = ser.read(ser.inWaiting()).decode()
    return response

# Imposta l'APN del tuo provider
apn = 'your_apn'
send_at_command(f'AT+SAPBR=3,1,"Contype","GPRS"')
send_at_command(f'AT+SAPBR=3,1,"APN","{apn}"')
send_at_command('AT+SAPBR=1,1')  # Avvia la connessione
response = send_at_command('AT+SAPBR=2,1')  # Verifica lo stato
print(response)

# Avvia il processo PPP
os.system('sudo pppd call gprs')
