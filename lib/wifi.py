import subprocess

def get_wifi_connection_raspberry():
    try:
        # Run iwgetid command to get the SSID of the connected Wi-Fi network
        result = subprocess.run(["iwgetid", "-r"], capture_output=True, text=True)
        
        # Check if there's an output (SSID of the connected network)
        ssid = result.stdout.strip()
        if ssid:
            print(f"Connected to Wi-Fi network: '{ssid}'")
            return ssid
        else:
            print("No active Wi-Fi connection found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function
get_wifi_connection_raspberry()