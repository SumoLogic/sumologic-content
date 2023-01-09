#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Fetches audit log data from the Mimecast API and saves to a folder for Sumo Logic data collection"""

import base64
import hashlib
import hmac
import json
import logging
import os
import pickle
import uuid
import time
import datetime
import sys
from os.path import dirname, abspath

import requests


def get_audit_logs(start, end):
    app_id = 'replace_with_access_id'
    app_key = 'replace_with_access_key'

    request_id = str(uuid.uuid4())
    hdr_date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S") + " UTC"
    uri = '/api/audit/get-audit-events'
    url = api_base_url + uri
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
        'meta': {
            'pagination': {
                'pageSize': 100
            }
        },
        'data': [
            {
                'startDateTime': start,
                'endDateTime': end
            }
        ]
    }

    if os.path.exists(os.path.join(dirname(dirname(abspath(__file__))), 'checkpoint', 'checkpoint_audit_next')):
        with open(os.path.join(os.path.join(dirname(dirname(abspath(__file__))), 'checkpoint',
                                            'checkpoint_audit_next')), 'r') as c:
            payload['meta']['pagination']['pageToken'] = c.read()

    try:
        logging.debug('Calling Mimecast: ' + url + ' Request ID: ' + request_id + ' Request Body: ' + str(payload))
        response = requests.post(url=url, data=str(payload), headers=headers, timeout=120)
        logging.debug('Response code: ' + str(response.status_code) + ' Headers: ' + str(response.headers))
        if response.status_code == 429:
            logging.warn('Mimecast API rate limit reached, sleeping for 30 seconds')
            time.sleep(30)
            logging.debug('Calling Mimecast: ' + url + ' Request ID: ' + request_id)
            response = requests.post(url=url, data=str(payload), headers=headers, timeout=120)
        elif response.status_code != 200:
            logging.error('Request to ' + url + ' with , request id: ' + request_id + ' returned with status code: '
                          + str(response.status_code) + ', response body: ' + response.text)
            return False
        else:
            try:
                response_body = json.loads(response.text)
                logging.debug('Setting log file name...')
                data_file_name = datetime.datetime.utcnow().strftime('%d%m%Y')
                data_file_name = 'audit_log_' + str(data_file_name) + '.log'
                with open(os.path.join(data_dir, 'audit', data_file_name), 'a') as al:
                    for event in response_body['data']:
                        al.write("date=" + event["eventTime"] + "|mcType=auditLog|user=" + event["user"] +
                                 "|auditType=\"" + event["auditType"] + "\"|eventInfo=\"" + event["eventInfo"] + "\n")

                if 'next' in response_body['meta']['pagination']:
                    logging.debug('Saving pagination checkpoint')
                    with open(os.path.join(os.path.join(dirname(dirname(abspath(__file__))), 'checkpoint',
                                                        'checkpoint_audit_next')), 'w') as ca:
                        ca.write(response_body['meta']['pagination']['next'])
                    return True
                else:
                    logging.debug('No more pages to collect. Saving end date as start date checkpoint for next run')
                    with open(os.path.join(os.path.join(dirname(dirname(abspath(__file__))), 'checkpoint',
                                                        'checkpoint_audit_start')), 'w') as csd:
                        csd.write(end)
                    if os.path.exists(os.path.join(dirname(dirname(abspath(__file__))), 'checkpoint',
                                                   'checkpoint_audit_next')):
                        logging.debug('Cleaning up page token')
                        os.remove(os.path.join(dirname(dirname(abspath(__file__))), 'checkpoint',
                                               'checkpoint_audit_next'))
                    return False
            except Exception, e:
                logging.exception('Unexpected error processing audit event data. Exception: ' + str(e))
                return False
    except Exception, e:
        logging.error('Unexpected error calling API. Exception: ' + str(e))
        return False


def get_iso_time(offset):
    date = datetime.datetime.utcnow()
    dt_offset = date - datetime.timedelta(minutes=offset)
    return_dt = dt_offset.strftime("%Y-%m-%dT%H:%M:%S") + "+0000"
    return return_dt


def remove_files(path):
    logging.info('Cleaning up files in: ' +  path)
    try:
        os.chdir(path)
        logging.debug('Directory changed successfully %s' % path)
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                curpath = os.path.join(dirpath, file)
                logging.debug('Checking ' + curpath)
                file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(curpath))
                logging.debug('Modified date: ' + str(file_modified))
                if datetime.datetime.now() - file_modified > datetime.timedelta(hours=168):
                    os.remove(curpath)
                    logging.debug('Removed ' + curpath)
                else:
                    logging.debug('Did not remove file: ' + curpath + '. File is not yet 7 days old')
    except Exception, e:
        logging.error('Error cleaning up files. Exception: ' + str(e))


# Program Start
with open(os.path.join(os.path.join(dirname(dirname(abspath(__file__))),
                                    'checkpoint', 'config.txt')), 'rb') as f:
    config = pickle.load(f)

log_dir = os.path.join(os.path.join(dirname(dirname(abspath(__file__))), 'log'))

log_name = 'audit_' + datetime.datetime.utcnow().strftime('%d%m%Y') + '.log'
logging.basicConfig(filename=os.path.join(log_dir, log_name), level=logging.INFO,
                    format='%(levelname)s|%(asctime)s|%(message)s')

account_code = config['account_code']
if len(account_code) < 0:
    logging.error('Log collection aborted. Account code not found, exiting.')
    sys.exit()

logging.info('***** Mimecast Data Collector for Sumo Logic v1.0 *****')
logging.info('Starting audit log collection for ' + account_code)

data_dir = config['data_dir']
if len(data_dir) < 0:
    logging.error('Data directory not set, exiting.')
    sys.exit()
logging.info('Using data directory: ' + data_dir)

access_key = config['access_key']
if len(access_key) < 0:
    logging.error('Access Key not set, exiting.')
    sys.exit()
secret_key = config['secret_key']
if len(secret_key) < 0:
    logging.error('Secret Key not set, exiting.')
    sys.exit()
api_base_url = config['api_base_url']
if len(api_base_url) < 0:
    logging.error('API base URL not set, exiting.')
    sys.exit()

if os.path.exists(os.path.join(dirname(dirname(abspath(__file__))), 'checkpoint', 'checkpoint_audit_start')):
    with open(os.path.join(dirname(dirname(abspath(__file__))), 'checkpoint', 'checkpoint_audit_start')) as csd:
        start = csd.read()
else:
    start = get_iso_time(60)

end = get_iso_time(0)

while get_audit_logs(start=start, end=end) is True:
    logging.info('Collecting Audit logs')

#Clean up data files
remove_files(os.path.join(dirname(dirname(abspath(__file__))), 'log'))
#Clean up log files
remove_files(os.path.join(data_dir, 'audit'))
logging.info('Audit log collection complete')
sys.exit()
