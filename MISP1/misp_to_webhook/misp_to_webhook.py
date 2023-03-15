import requests
import json, os


misp_url = input("Please enter your misp url  ")
endpoint_url = input("Please enter your Sumo Logic https endpoint ")

def send_misp_request(url, headers, data):
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        raise ValueError(f'Request failed with status code {response.status_code}: {response.text}')

def send_logs_to_webhook(logs, endpoint_url, headers):
    for log in logs:
        response = requests.post(endpoint_url, json=log, headers=headers)
        if response.status_code != 200:
            raise ValueError(f'Failed to send JSON to endpoint. Status code: {response.status_code}')
        else:
            print('JSON sent to endpoint successfully')

# Set the URL and headers for the initial request
headers = {
    'Authorization': os.environ['misp_api_key'],
    'Accept': 'application/json',
    'Content-type': 'application/json'
}

# Set the request data for the initial request
data = {
    'returnFormat': 'json',
    'page': '1',
    'limit': '100',
    'order': 'Event.attribute_count desc, Event.date desc'
}

# Send the initial request and check for a response
response = send_misp_request(misp_url, headers, data)
if not response:
    print('Search request failed')
    exit()

# Send the initial logs to the webhook
logs = response['response']['Attribute']
send_logs_to_webhook(logs, endpoint_url, headers)

# Paginate until there are no more results to grab
while response:
    # Increment the page number in the request data
    data['page'] = str(int(data['page']) + 1)

    # Make the next request and check for a response
    response = send_misp_request(misp_url, headers, data)

    if response:
        # Send the logs to the webhook
        logs = response['response']['Attribute']
        send_logs_to_webhook(logs, endpoint_url, headers)

print('All results sent to webhook')
