import os
import json
import requests
from requests.auth import HTTPBasicAuth
from configparser import ConfigParser
from datetime import datetime, timedelta, timezone
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables
config = ConfigParser()
config.read('./env.ini')

cip_access_id = config.get('DEFAULT', 'cip_access_id', fallback='xxx')
cip_access_key = config.get('DEFAULT', 'cip_access_key', fallback='xxxxx')
cip_ti_sourcename = config.get('DEFAULT', 'cip_ti_sourcename', fallback='test_misp')
cip_ti_url = config.get('DEFAULT', 'cip_ti_url', fallback='xxxxx')

misp_url = config.get('DEFAULT', 'misp_url', fallback='https://api.au.sumologic.com')
misp_api_key = config.get('DEFAULT', 'misp_api_key', fallback='xxxxx')
cip_ti_indicator_retention = config.get('DEFAULT', 'cip_ti_indicator_retention', fallback='30')
misp_tag = config.get('DEFAULT', 'misp_tag', fallback='OSINT')
misp_tag_array = [item.strip() for item in misp_tag.split(',') if item]
mist_last = config.get('DEFAULT', 'mist_last', fallback='24h')


def remap_attributes(attribute):
    """
    Remaps certain attributes to a specific payload
    """

    # Get current UTC time in the desired format
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')
    future_time = datetime.now(timezone.utc) + timedelta(days=int(cip_ti_indicator_retention))
    future_time_formatted = future_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')

    # maping Type
    msip_type=attribute['type']
    if msip_type in ("domain","hostname"):
        cip_ti_type = "domain-name"
    elif "email" in msip_type:
        cip_ti_type = "email-addr"
    elif msip_type in ("filename", "pdb"):
        cip_ti_type = "file"
    elif msip_type in ("first-name", "full-name", "last-name"):
        cip_ti_type = "user-account"
    elif msip_type in ("ip-dst", "ip-src"):
        cip_ti_type = "ipv4-addr"
    elif msip_type in ("link","uri","url"):
        cip_ti_type = "url"
    elif msip_type in ("md5","vhash","filehash") or  msip_type.startswith("sha"):
        cip_ti_type = "file:hashes"
    elif msip_type in ("mac-address", "mac-eui-64"):
        cip_ti_type = "mac-addr"
    else:
        cip_ti_type = "none"

    indicator = {
        "id": attribute['uuid'],
        "indicator": attribute['value'],
        "type": cip_ti_type,
        "source": cip_ti_sourcename,
        "validFrom": current_time,
        "validUntil": future_time_formatted,
        "confidence": 50,
        "threatType": "anomalous-activity" 
    }

    # print("pring payload")
    # print(json.dumps(indicator))

    return indicator

def send_misp_request(misp_url, headers, data):
    response = requests.post(misp_url, headers=headers, json=data, verify=False)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        raise ValueError(f'Request failed with status code {response.status_code}: {response.text}')


def add_indicators_to_cip_ti(payload):

    response = requests.post(cip_ti_url,auth=HTTPBasicAuth(cip_access_id, cip_access_key), json=payload) 
    if 200 <= response.status_code < 300:
        # data = response.json()
        print("MISP Indicators added")
        # print(json.dumps(data, indent=2))
    else:
        print('Error:', response.status_code)
        print("body: ",response.text)
        print(json.dumps(dict(response.headers), indent=2))
        print("payload:",json.dumps(payload))
    

# Set the URL and headers for the initial request
headers = {
    'Authorization': misp_api_key,
    'Accept': 'application/json',
    'Content-type': 'application/json'
}

# Set the request data for the initial request
data = {
    'returnFormat': 'json',
    'page': '0',
    'limit': '100',
    "tags": misp_tag_array,
    "to_ids":"1",
    "publish_timestamp": mist_last
}


# Paginate until there are no more results to grab
response = {
    "response": {
        "Attribute": [
            {
                "none": "none"
            }
        ]
    }
}
loop_times = 0
while response['response']['Attribute']:
    # Increment the page number in the request data
    data['page'] = str(int(data['page']) + 1)

    
    loop_times = loop_times + 1
    print ("In Loop: ", loop_times,"times")
    # if loop_times == 3:
    #     break

    # Make the next request and check for a response
    response = send_misp_request(misp_url, headers, data)
    if response['response']['Attribute']:
        indicators = []
        for attribute in response['response']['Attribute']:
            payload_temp = remap_attributes(attribute)
            if payload_temp['type'] == "none":
                print("Type Not in CIP - attribute: ",json.dumps(attribute))
            else:    
                indicators.append(payload_temp)
        payload = {"indicators": indicators}
        add_indicators_to_cip_ti(payload)
    else: 
        print("No more indicators")
        
print("End")