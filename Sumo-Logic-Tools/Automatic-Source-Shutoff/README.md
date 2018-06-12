# Automatic Source Shutoff Script

This is a Python script that will automatically add a [processing rule](https://help.sumologic.com/Manage/Collection/Processing-Rules) to a source on a collector to exclude all logs.

This script should be used in conjunction with a Sumo Logic [Script Action](https://help.sumologic.com/Send-Data/Sources/01Sources-for-Installed-Collectors/Script-Action) to trigger when a certain threshold is met. For example, if a source hits an ingestion amount in a certain amount of time or there is a large [outlier](https://help.sumologic.com/Search/Search-Query-Language/Search-Operators/outlier) spike on ingestion for a source, then it will exclude any logs going forward.

*Note: This script currently will only create the exclusion of logs. It will not automatically "turn on" a source. You must manually remove the processing rule created.*

The script will add a processing rule to the source on the specified collector called "Drop Logs Script". It adds an exclude rule for _all_ logs (regex pattern: .\*).

When a source is excluded, it will create a log entry under the source of the name of the Script Action specifying the time, Source, and Collector.

## Setup and Configuration

1. Setup an Installed Collector on a system with Python configured.

2. Create a Sumo Access ID and Access Key set.

3. Modify _sourceShutoff.py_, and replace ACCESSID, ACCESSKEY, and [DEPLOYMENT](https://help.sumologic.com/APIs/General-API-Information/Sumo-Logic-Endpoints-and-Firewall-Security) with your appropriate values. Fill in your appropriate Environment for DEPLOYMENT.

4. Place sourceShutoff.py in a folder on the system.

5. Setup a Script Action on the Installed Collector. Specify a name and description (optional). For command, specify _/usr/bin/python_. For script, specify the _absolute path_ to the script. For example, _/home/ubuntu/scripts/sourceShutoff.py_. For Working Directory, specify the folder the script is located in. Save the Script Action.

6. Setup the Scheduled View from _data-volume-scheduled-view.txt_. 

7. Write a query with the different threshold(s) to shutoff your collector. An example is found in _example-shutoff-query.txt_. This example will trigger the Script Action if a source on a collector has ingested over 50 megabytes in a 5 minute window. 

8. Schedule the query, specify Script Action, and select the one you created. 