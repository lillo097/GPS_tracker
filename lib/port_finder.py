import serial.tools.list_ports

# Trova tutte le porte seriali
ports = serial.tools.list_ports.comports()

# Stampa l'elenco delle porte disponibili
for port in ports:
    print(f"Porta trovata: {port.device}")


# Port trovata: /dev/cu.URT0
# Porta trovata: /dev/cu.Bluetooth-Incoming-Port
# Porta trovata: /dev/cu.usbserial-1420