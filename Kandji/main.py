import requests
import json
import time
import os


# Access environment variables
SUBDOMAIN = os.environ.get('SUBDOMAIN')
SIEM_HTTPS_ENDPOINT = os.environ.get('SIEM_HTTPS_ENDPOINT')
TOKEN = os.environ.get('TOKEN')

# Check if environment variables are set
if not (SUBDOMAIN and SIEM_HTTPS_ENDPOINT and TOKEN):
    print("Error: Missing environment variables. Ensure SUBDOMAIN, SIEM_HTTPS_ENDPOINT, and TOKEN are set.")
    exit()

# Constants
API_BASE_URL = f"https://{SUBDOMAIN}.api.kandji.io/api/v1"
RETRY_INTERVAL = 10  # Time in seconds to wait before retrying a failed request
LIMIT = 300  # Maximum number of results per request

def make_request(url, headers, retries=1):
    for _ in range(retries + 1):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError:
                print(f"Error: Response from {url} is not valid JSON. Retrying...")
                time.sleep(RETRY_INTERVAL)
        elif response.status_code == 401:
            print(f"Error: Token does NOT have permissions")
        else:
            print(f"Error {response.status_code} when accessing {url}. Retrying...")
            time.sleep(RETRY_INTERVAL)
    print(f"Failed to fetch data from {url} after {retries + 1} attempts.")
    return None

def send_to_siem(data, category):
    headers = {
        "Content-Type": "application/json",
        "X-Sumo-Category": f"kandji/{category}"
    }
    response = requests.post(SIEM_HTTPS_ENDPOINT, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print(f"Data of category {category} successfully sent to SIEM.")
    else:
        print(f"Failed to send data of category {category} to SIEM. Error: {response.status_code}")

def fetch_all_devices(headers):
    offset = 0
    all_devices = []
    
    while True:
        devices_data = make_request(f"{API_BASE_URL}/devices?limit={LIMIT}&offset={offset}", headers)
        if not devices_data:
            break

        all_devices.extend(devices_data)
        if len(devices_data) < LIMIT:
            break  # If fewer than LIMIT devices are returned, it means we've fetched all devices
        offset += LIMIT

    return all_devices

def main():
    
    headers = {"Authorization": f"Bearer {TOKEN}"}

    # 1. Fetch all devices with pagination
    all_devices = fetch_all_devices(headers)
    device_ids = [device["device_id"] for device in all_devices]

    # 2. Fetch threat details
    threat_data = make_request(f"{API_BASE_URL}/threat-details", headers)
    if threat_data:
        send_to_siem(threat_data, "threat_data")

    # 3. Fetch lost device mode for each device id
    for device_id in device_ids:
        lost_device_data = make_request(f"{API_BASE_URL}/devices/{device_id}/details/lostmode", headers)
        if lost_device_data:
            send_to_siem(lost_device_data, "lost_device_data")
    
    # 4. Device commands 

    for device_id in device_ids:
        device_commands = make_request(f"{API_BASE_URL}/devices/{device_id}/commands", headers)
        if device_commands: 
            send_to_siem(device_commands, "device_commands")

    # 5. Device Apps
    for device_id in device_ids:
        device_apps = make_request(f"{API_BASE_URL}/devices/{device_id}/apps", headers)
        if device_apps: 
            send_to_siem(device_apps, "device_apps")
    
    # 6. Device Details (inventory for CSE)
    for device_id in device_ids:
        device_details = make_request(f"{API_BASE_URL}/devices/{device_id}/details", headers)
        if device_details: 
            send_to_siem(device_details, "device_apps")

if __name__ == "__main__":
    main()
