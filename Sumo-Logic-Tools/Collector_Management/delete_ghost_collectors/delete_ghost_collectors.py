#!/usr/bin/python
import json
import requests
import getpass
import datetime
import sys
#API_URL = "https://api.sumologic.com/api/v1/collectors"
#API_URL = "https://api.us2.sumologic.com/api/v1/collectors"
#API_URL = "https://api.eu.sumologic.com/api/v1/collectors"
#API_URL = "https://api.au.sumologic.com/api/v1/collectors"
if sys.version_info[0] >= 3:
  get_input = input
  DEPLOYMENT = input("Deployment: ")
  ACCESSID = input("AccessID: ")
  ACCESSKEY = getpass.getpass()
  OFFLINE = input("Hours Offline: ")
  AUDIT = input("Audit Mode: (y/n)")
else:
  get_input = raw_input
  DEPLOYMENT = raw_input("Deployment: ")
  ACCESSID = raw_input("AccessID: ")
  ACCESSKEY = getpass.getpass()
  OFFLINE = raw_input("Hours Offline: ")
  AUDIT = raw_input("Audit Mode: (y/n)")

if (AUDIT != "y") and (AUDIT != "n"):
  AUDIT = "y"

def main():
  try:
    #set API endpoint
    if DEPLOYMENT in ("us1", "us2", "au", "eu", "de", "ca", "jp"):
      if DEPLOYMENT == "us1":
        API_URL = "https://api.sumologic.com/api/v1/collectors"    
      else:
        API_URL = "https://api." + DEPLOYMENT + ".sumologic.com/api/v1/collectors"
    else:
      print("Invalid Deployment - " + DEPLOYMENT)
      sys.exit(1)

    #get the epoch time for deletion based on "now" - hours offline.
    time = int(datetime.datetime.now().strftime("%s")) * 1000
    o_millis = int(OFFLINE) * 60 * 60 * 1000
    delete_time = time - int(o_millis)
    s = int(delete_time) / 1000.0
    v_date = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S')
    print("Checking for Collectors offline since: " + str(v_date))
    # Get our list of Collectors from Sumo Logic.
    collectorlist = requests.get(API_URL, auth=(ACCESSID, ACCESSKEY), verify=False)
    collectors = collectorlist.json()
    # Locate the offline collectors and delete them if the lastSeenAlive time is over given hours
    for collector in collectors['collectors']:
      if collector['alive'] is False and collector['lastSeenAlive'] <= delete_time:
        id=str(collector['id'])
        a = int(collector['lastSeenAlive']) / 1000.0
        af = datetime.datetime.fromtimestamp(a).strftime('%Y-%m-%d %H:%M:%S')
        termOut = "Offline Collector: '" + collector['name'] + "' Last seen alive on: " + af
        if (AUDIT == "n"):
          requests.delete(API_URL+"/"+id, auth=(ACCESSID, ACCESSKEY), verify=False)
          termOut += " --- DELETED"
        print(termOut)
  except:
    print("Something went wrong -> could not delete ghost collectors...")
    sys.exit(1)
if __name__ == "__main__":
    sys.exit(main())