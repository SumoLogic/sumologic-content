import os
import json
import boto3
import requests
import dateutil.parser
from datetime import datetime, timedelta, timezone
import time

# add timestamp parse rule to source: yyyyMMddHHmmss.SSS

globs = {
	"access_token": "",
	"sumo_collector_url": "",
	"client_id": "",
	"refresh_token": "",
	"refresh_url": "https://test.salesforce.com/services/oauth2/token",
	"ssm": None
}
#update refresh url for each instance

def getAuthHeader():
	access_token = globs["access_token"]
	return {'Authorization': f"Bearer {access_token}"}

def httpGet(url):
	access_token = globs["access_token"]
	response = requests.get(url, headers=getAuthHeader())

	if (response.status_code >= 400):
		print("token expired; getting a new one")
		refresh_response = requests.post(
			globs["refresh_url"], 
			data={"grant_type": "refresh_token", "refresh_token": globs["refresh_token"], "client_id": globs["client_id"]},
			headers={"Content-Type": "application/x-www-form-urlencoded"})
		globs["access_token"] = refresh_response.json()['access_token']
		globs["ssm"].put_parameter(
			Name = os.environ.get('accessToken'),
	        Type = 'String',
	        Overwrite = True,
	        Value = globs["access_token"]
	        )

	return requests.get(url, headers=getAuthHeader())

def uploadLogsToSumo(log_ids):
	for log_id in log_ids:
		url = f"https://cs17.salesforce.com/services/data/v32.0/sobjects/EventLogFile/{log_id}/LogFile"
		response = httpGet(url)

		lines = list(map(lambda splitLine: list(map(lambda s: s[1:-1], splitLine)), list(map(lambda ln: ln.split(','), response.text.splitlines()))))
		column_names = lines[0]
		payload = ""
		for line in lines[1:]:
			payload += json.dumps(dict(zip(column_names, line))) + "\n"
	
		requests.post(globs["sumo_collector_url"], data=payload)
		print(f"uploaded id {log_id}")


def getSfdcLogsForEventType(event_type, date):

	print(f"fetching logs created after: {date} PST")
	url = f"https://cs17.salesforce.com/services/data/v32.0/query?q=SELECT+Id+,+EventType+,+LogFile+,+CreatedDate+,+LogFileLength+FROM+EventLogFile+WHERE+CreatedDate+>+{date}+AND+EventType+=+'{event_type}'" 
	response = httpGet(url)
	print(f"successfully fetched {event_type} logs")
	ids = list(map(lambda record: record['Id'], response.json()['records']))

	return ids

def lambda_handler(event, context):
	start_time = (datetime.now(timezone.utc) - timedelta(hours=8)).strftime('%Y-%m-%d' + 'T' + '%H:%M:%S') + 'Z'
	print(f"start time is {start_time} PST")
	event_types = ["API", "LOGIN"]

	try:
		env_sumoCollectorUrl = os.environ.get('sumoCollectorUrl')
		env_latestTimestamp = os.environ.get('latestTimestamp')
		env_clientUrl = os.environ.get('clientId')
		env_refreshToken = os.environ.get('refreshToken')
		env_accessToken = os.environ.get('accessToken')
	except Exception as e:
		return {'Result': "Can't get environment variables", 'Error': e}
	try:
		ssm = boto3.client('ssm')
		globs["ssm"] = ssm
		globs["sumo_collector_url"] = ssm.get_parameter(Name=env_sumoCollectorUrl, WithDecryption=True)['Parameter']['Value']
		latest_timestamp = ssm.get_parameter(Name=env_latestTimestamp, WithDecryption=True)['Parameter']['Value']
		globs["client_id"] = ssm.get_parameter(Name=env_clientUrl, WithDecryption=True)['Parameter']['Value']
		globs["refresh_token"] = ssm.get_parameter(Name=env_refreshToken, WithDecryption=True)['Parameter']['Value']
		globs["access_token"] = ssm.get_parameter(Name=env_accessToken, WithDecryption=True)['Parameter']['Value']
	except Exception as e:
		return {'Result': "Can't get configuration items from AWS Parameter Store", 'Error': e}

	for event_type in event_types:
		ids = getSfdcLogsForEventType(event_type, latest_timestamp)
		print(f"{len(ids)} log files to process")

		uploadLogsToSumo(ids)
	
	ssm.put_parameter(
		Name = env_latestTimestamp,
        Type = 'String',
        Overwrite = True,
        Value = start_time
        )

	print(f"upload completed for logs created after {latest_timestamp} PST")
