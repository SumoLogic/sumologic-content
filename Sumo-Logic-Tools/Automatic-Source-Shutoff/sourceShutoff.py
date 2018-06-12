import sys
import json
import requests
import datetime

ACCESSID='INSERT_SUMO_ID'
ACCESSKEY='INSERT_SUMO_KEY'
DEPLOYMENT='us2'

url="https://api." + DEPLOYMENT + ".sumologic.com/api/v1/"
processing_rule={"filterType": "Exclude", "name": "Drop Logs Script", "regexp": ".*"}

results=sys.argv[1]
with open(results) as data_file:
    data=json.load(data_file)

for source in data['queryResults']:
    sourceData=requests.get(url + "collectors/" + source["Collectorid"] + "/sources/" + source["Sourceid"], auth=(ACCESSID, ACCESSKEY))

    newSourceData=sourceData.json()
    ETag=sourceData.headers['ETag']
    newSourceData['source']['filters'].append(processing_rule)

    headers={'Content-Type':'application/json', 'If-Match': ETag}
    updatedSource=requests.put(url + "collectors/" + source["Collectorid"] + "/sources/" + source["Sourceid"], auth=(ACCESSID, ACCESSKEY), json=newSourceData, headers=headers)
    now=datetime.datetime.now()
    if(updatedSource.status_code==200):
        print "{} action=ExcludeSource status=Success collector={} collectorId={} source={} sourceId={}".format(now, source["Collector"], source["Collectorid"], source["Source"], source["Sourceid"])
    else:
        print "{} action=ExcludeSource status=Fail collector={} collectorId={} source={} sourceId={}".format(now, source["Collector"], source["Collectorid"], source["Source"], source["Sourceid"])