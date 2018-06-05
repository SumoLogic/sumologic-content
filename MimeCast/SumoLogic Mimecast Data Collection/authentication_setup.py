#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Login utility for Mimecast log collection """
import base64
import getpass
import hashlib
import hmac
import json
import pickle
import os
import uuid
import datetime
import sys
from os.path import dirname, abspath

import requests

app_id = 'replace_with_app_id'
app_key = 'replace_with_app_key'

print '************************************************************************'
print '****** Sumo Logic Mimecast setup utility v1.0 ******'
print '************************************************************************'

config = {}
print 'Please enter the full path to the folder / directory where Mimecast data will be stored. ' \
      'You can use an existing path or create a new path here.'

data_dir = raw_input('Data Directory: ')
config['data_dir'] = data_dir
# data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')

print str(data_dir)

if os.path.exists(data_dir):
    print 'Data directory exists'
else:
    try:
        os.makedirs(data_dir)
        print 'Data directory created successfully'
        os.makedirs(os.path.join(data_dir, 'audit'))
        print 'Audit data directory created successfully'
        os.makedirs(os.path.join(data_dir, 'mta'))
        print 'MTA data directory created successfully'
        os.makedirs(os.path.join(data_dir, 'tmp'))
        print 'Tmp data directory created successfully'
    except Exception, e:
        print 'Unexpected error creating log directory: ' + str(e)

if os.path.exists(os.path.join(os.path.join(dirname(dirname(abspath(__file__)))), 'checkpoint')):
    print 'Checkpoint directory exists'
else:
    try:
        os.makedirs(os.path.join(os.path.join(dirname(dirname(abspath(__file__)))), 'checkpoint'))
        print 'Checkpoint directory created successfully'
    except Exception, e:
        print 'Unexpected error creating log directory: ' + str(e)


if os.path.exists(os.path.join(os.path.join(dirname(dirname(abspath(__file__)))), 'log')):
    print 'Log directory exists'
else:
    try:
        os.makedirs(os.path.join(os.path.join(dirname(dirname(abspath(__file__)))), 'log'))
        print 'Log directory created successfully'
    except Exception, e:
        print 'Unexpected error creating log directory: ' + str(e)

print 'Please log in using the email address and Mimecast password of a Mimecast administrator ' \
      'account to continue:'

email_address = raw_input('Email Address:')
password = getpass.getpass(prompt='Password:')

print 'Discovering API base url for ' + email_address

def discover_base_url():
    try:
        base_url = "https://api.mimecast.com"
        uri = "/api/login/discover-authentication"
        url = base_url + uri

        request_id = str(uuid.uuid4())
        hdr_date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S") + " UTC"

        headers = {
            'x-mc-app-id': app_id,
            'x-mc-date': hdr_date,
            'x-mc-req-id': request_id,
            'Content-Type': 'application/json'
        }

        payload = {
            "data": [
                {
                    "emailAddress": email_address
                }
            ]
        }

        r = requests.post(url=url, headers=headers, data=str(payload))

        api_base_url = json.loads(r.text)
        return api_base_url['data'][0]['region']['api']
    except Exception, e:
        print 'Unexpected error discovering base url, exception: ' + str(e)
        sys.exit()

api_base_url = discover_base_url()
print 'API Base URL discovered: ' + api_base_url
config['api_base_url'] = api_base_url

print 'Requesting access key and secret key values...'

def log_in():
    try:
        uri = "/api/login/login"
        url = api_base_url + uri
        request_id = str(uuid.uuid4())
        hdr_date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S") + " UTC"

        headers = {
            'Authorization': 'Basic-Cloud ' + base64.b64encode(email_address + ':' + password),
            'x-mc-app-id': app_id,
            'x-mc-date': hdr_date,
            'x-mc-req-id': request_id,
            'Content-Type': 'application/json'
        }

        payload = {
            "data": [
                {
                    "userName": email_address
                }
            ]
        }

        r = requests.post(url=url, headers=headers, data=str(payload))

        if r.status_code != 200:
            print 'Login Failed. Status Code: ' + str(r.status_code)
            print 'Response body: ' + r.text
            sys.exit()
        else:
            return r.text
    except Exception, e:
        print 'Unexpecting error processing log in, exception: ' + str(e)
        sys.exit()

keys = json.loads(log_in())
access_key = keys['data'][0]['accessKey']
secret_key = keys['data'][0]['secretKey']
config['access_key']= access_key
config['secret_key'] = secret_key

print 'Log in successful. Retrieving account code and saving to configuration...'

def get_account():
    uri = '/api/account/get-account'
    url = api_base_url + uri
    request_id = str(uuid.uuid4())
    hdr_date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S") + " UTC"

    hmac_sha1 = hmac.new(secret_key.decode("base64"), ':'.join([hdr_date, request_id, uri, app_key]),
                         digestmod=hashlib.sha1).digest()

    sig = base64.encodestring(hmac_sha1).rstrip()

    headers = {
        'Authorization': 'MC ' + access_key + ':' + sig,
        'x-mc-app-id': app_id,
        'x-mc-date': hdr_date,
        'x-mc-req-id': request_id,
        'Content-Type': 'application/json'
    }

    payload = {
        'data': [
        ]
    }
    try:
        r = requests.post(url=url, headers=headers, data=str(payload))
    except Exception, e:
        print 'Unexpected error getting account code for ' + email_address + '. Exception: ' + str(e)
        sys.exit(0)

    return json.loads(r.text)['data'][0]['accountCode']

config['account_code'] = get_account()

try:
    with open(os.path.join(os.path.join(dirname(dirname(abspath(__file__)))), 'checkpoint', 'config.txt'), 'wb') as f:
        pickle.dump(config, f)
except Exception, e:
    print 'Unexpected error writing config, exception: ' + str(e)
    sys.exit()

print 'Configuration saved successfully.'
