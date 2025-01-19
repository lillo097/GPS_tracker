import requests
import time
import subprocess


def save_html(url, filename):
    # Fetches the HTML content of a URL and saves it to a file
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an exception for HTTP errors
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"HTML content from {url} saved to {filename}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching {url}: {e}")
        return False


def run_command(command):
    # Executes the specified command in the terminal
    print(f"Executing command: {command}")
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")


def monitor_html(url, filename, command):
    while True:
        print(f"Checking {url}...")
        success = save_html(url, filename)

        if not success:
            run_command(command)

        # Wait for 15 minutes (900 seconds) before checking again
        print("Waiting 1h for next status check...")
       # print("°"*500)
        time.sleep(300)


def runHtmlService():
    # URL to fetch, file to save HTML, and command to execute on error
    url = "https://mysubdomain.serveo.net/"  # Replace with the URL you want to fetch
    filename = "output.html"  # The filename to save the HTML content
    command = "sudo systemctl restart gps_tracker"  # Replace with the command to run on error

    monitor_html(url, filename, command)

