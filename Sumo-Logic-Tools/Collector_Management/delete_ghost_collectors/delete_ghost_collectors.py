#!/usr/bin/python
import json
import requests
import getpass
from datetime import datetime
import sys
import traceback

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
    
    print ("API_URL = " + API_URL)
    try:      
      #get the epoch time for deletion based on "now" - hours offline.
      epoch_time = datetime.utcfromtimestamp(0)
      now_utc = datetime.utcnow()
      time = (now_utc - epoch_time).total_seconds() * 1000
      # print ("time = ", time)
    except Exception:
      print("Something went wrong -> could not get epoch time...")
      traceback.print_exc()
      sys.exit(1)  
    #OFFLINE in milliseconds 
    o_millis = int(OFFLINE) * 60 * 60 * 1000
    delete_time = time - int(o_millis)
    s = int(delete_time) / 1000
    print ("s = " + str(s))
    v_date = datetime.fromtimestamp(s).strftime("%m/%d/%Y, %H:%M:%S")
    print("Checking for Collectors offline since: " + str(v_date))
    # Get our list of Collectors from Sumo Logic.
    collectorlist = requests.get(API_URL, auth=(ACCESSID, ACCESSKEY), verify=False)
    collectors = collectorlist.json()
    # Locate the offline collectors and delete them if the lastSeenAlive time is over given hours
    for collector in collectors['collectors']:
      if collector['alive'] is False and collector['lastSeenAlive'] <= delete_time:
        id=str(collector['id'])
        a = int(collector['lastSeenAlive']) / 1000.0
        af = datetime.fromtimestamp(a).strftime('%Y-%m-%d %H:%M:%S')
        termOut = "Offline Collector: '" + collector['name'] + "' Last seen alive on: " + af
        if (AUDIT == "n"):
          requests.delete(API_URL+"/"+id, auth=(ACCESSID, ACCESSKEY), verify=False)
          termOut += " --- DELETED"
        print(termOut)
  except Exception:
    print("Something went wrong -> could not delete ghost collectors...")
    traceback.print_exc()
    sys.exit(1)
if __name__ == "__main__":
    sys.exit(main())
