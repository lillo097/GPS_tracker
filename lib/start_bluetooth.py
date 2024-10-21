import serial
import time

# Set up serial communication (change port and baudrate as needed)
ser = serial.Serial('/dev/cu.usbserial-1420', 9600, timeout=1)  # Adjust 'COM3' for your serial port
time.sleep(2)  # Wait for the connection to stabilize

def send_at_command(command, delay=1):
    """Sends an AT command to the SIM808 and prints the response"""
    ser.write((command + '\r').encode())  # Send AT command
    time.sleep(delay)
    response = ser.read_all().decode()  # Read response
    print(response)
    return response

# Initialize Bluetooth by sending AT commands

# 1. Check if Bluetooth is supported
send_at_command('AT+BTHOST?')

# 2. Set Bluetooth to ON
send_at_command('AT+BTPOWER=1')

# 3. Make the SIM808 discoverable
send_at_command('AT+BTSCPAN=1')  # Make it discoverable and connectable

# 4. Query the Bluetooth state to ensure it's enabled
send_at_command('AT+BTPOWER?')

# 5. Optionally, list paired devices
send_at_command('AT+BTLIST')

# Close the serial connection when done
ser.close()
