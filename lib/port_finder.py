import serial.tools.list_ports

# Trova tutte le porte seriali
ports = serial.tools.list_ports.comports()
list_of_ports = []
for port in ports:
    list_of_ports.append(port.device)
print(list_of_ports)
serial_port = list_of_ports[-1]

print(serial_port)

