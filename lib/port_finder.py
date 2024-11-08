import serial.tools.list_ports

# Trova tutte le porte seriali
ports = serial.tools.list_ports.comports()

# Stampa l'elenco delle porte disponibili
for port in ports:
    print(f"Porta trovata: {port.device}")

