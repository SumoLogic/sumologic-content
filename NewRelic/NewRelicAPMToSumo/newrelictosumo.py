# Version March 15, 2018
# Created by Dan Reichert at Sumo Logic

from newrelic_api import Applications
from datetime import datetime, timedelta

import sys
import json
import time
import requests

time_pattern='%Y-%m-%dT%H:%M:%S+00:00'


configfilename='newrelic.conf'
if len(sys.argv) > 1:
    configfilename=sys.argv[1]

configvars = {}
with open("newrelic.conf") as conffile:
    for line in conffile:
        key, val = line.partition("=")[::2]
        configvars[key.strip()] = str(val)

apps = Applications(api_key=configvars['NR_APIKEY'].rstrip())
SUMO_ENDPOINT=configvars['SUMO_ENDPOINT'].rstrip()

def Convert_Metricname_To_Carbon(metric_name):
    metric_name=metric_name.split("/")
    metric_name_formatted=""
    for x in range(0, len(metric_name)):
        if x == 0:
            metric_name_formatted="prefix=" + metric_name[x]
        if x == 1:
            metric_name_formatted=metric_name_formatted + " category=" + metric_name[x]
        if x == 2:
            metric_name_formatted=metric_name_formatted + " label=" + metric_name[x]
    return(metric_name_formatted)

def Main():
    metrics_upload=[]
    app_list=apps.list()['applications']
    t0=time.time()
    for app in app_list:
        app_name=app['name'].replace(" ", "_") # Replace spaces in the name with underscores
        metrics=apps.metric_names(app['id'])
        metrics_list=metrics['metrics']
        from_dt=datetime.now() - timedelta(minutes=1)
        metric_names=[]
        for metric in metrics_list:
            metric_names.append(metric['name'])
            
        metric_sets=apps.metric_data(app['id'], metric_names, from_dt=from_dt)['metric_data']['metrics']

        for metric_set in metric_sets:
            timeslice=metric_set['timeslices']
            metric_name=metric_set['name']
            epoch=int(time.mktime(time.strptime(timeslice[0]['to'], time_pattern)))

            for values in metric_set['timeslices']:
                for value in values['values']:
                    if isinstance(values['values'][value], int):
                        metric_formatted_carbon2='app=' + app_name + ' ' + Convert_Metricname_To_Carbon(metric_name.replace(" ", "_")) + ' units=' + value + '  ' + str(values['values'][value]) + ' ' + str(epoch) + '\n'
                        metrics_upload.append(metric_formatted_carbon2)
            
    fh = open('metrics_download', "w")
    fh.writelines(metrics_upload)
    fh.close()
    
    headers={'Content-Type':'application/vnd.sumologic.carbon2'}
    status=requests.post(SUMO_ENDPOINT, headers=headers, data=open('metrics_download', 'rb'))
  

    t1=time.time()
    print("Took %.2f ms" % (1000*(t1-t0)))

if __name__ == '__main__':
    Main()
