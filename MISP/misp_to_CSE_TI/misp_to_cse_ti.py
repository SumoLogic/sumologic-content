import os
import json
import requests
from requests.auth import HTTPBasicAuth


cip_deployment = input("Please enter your cip deployment ")
misp_url = input("Please enter your misp url  ")

def remap_attributes(attribute):
    """
    Remaps certain attributes to a specific payload
    """
    return {
        "active": "true",
        "description": attribute['Event']['info'],
        "value": attribute['value']
    }

def send_misp_request(misp_url, headers, data):
    response = requests.post(misp_url, headers=headers, json=data)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        raise ValueError(f'Request failed with status code {response.status_code}: {response.text}')


def add_indicators(payload):
    # environment variables
    cip_access_id = os.environ['cip_access_id']
    cip_access_key = os.environ['cip_access_key']
    
    if cip_deployment == "prod":
        threat_intel_url = f'https://api.sumologic.com/api/sec/v1/threat-intel-sources/{TI-ID}/items'
    elif cip_deployment != "prod":
        threat_intel_url = f'https://api.{cip_deployment}.sumologic.com/api/sec/v1/threat-intel-sources/{TI-ID}/items'

    print(threat_intel_url)
    # other variables

    response = requests.post(threat_intel_url,auth=HTTPBasicAuth(cip_access_id, cip_access_key), json=payload) 
    if response.status_code == 200:
        data = response.json()
        print("MISP Indicators added")
        print(json.dumps(data, indent=2))
    else:
        print('Error:', response.status_code)
    

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

# Print the first payload
indicators = []
for attribute in response['response']['Attribute']:
    indicators.append(remap_attributes(attribute))
payload = {"indicators": indicators}

# Paginate until there are no more results to grab
while response:
    # Increment the page number in the request data
    data['page'] = str(int(data['page']) + 1)

    # Make the next request and check for a response
    response = send_misp_request(misp_url, headers, data)

    if response:
        indicators = []
        for attribute in response['response']['Attribute']:
            indicators.append(remap_attributes(attribute))
        payload = {"indicators": indicators}
        add_indicators(payload)


