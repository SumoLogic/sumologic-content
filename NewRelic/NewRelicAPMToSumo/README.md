# New Relic APM to Sumo Logic HTTP

## NOTE: This script is still in testing and beta! 

This is a script to integrate with New Relic's APM product that will ingest the APM into Sumo Logic using Carbon 2.0 metrics. The purpose of this is to allow you to have a single pane of glass to monitor not only your system logs and host metrics natively in Sumo Logic dashboards and alerts, but also ingest correlate your New Relic APM data to this data.

## How It Works:
- The script relies on the [New Relic API SDK](https://pypi.python.org/pypi/newrelic-api).
- Converting it to Lambda will also require the Python Requests dependency, which is typically standard but it is not a standard Lambda library. This will need to be packaged to convert it to a Lambda function.
- There is a .conf file that is currently used for 2 variables: NR_APIKEY and SUMO_ENDPOINT.
  - NR_APIKEY is the API key generated in New Relic APM
  - SUMO_ENDPOINT is an HTTP collector.
- The script is a [Sumo Logic Script Source](https://help.sumologic.com/Send-Data/Sources/01Sources-for-Installed-Collectors/Script-Source); however, a cronjob should work just as well.
- Script Sources do not currently support metrics, so this is why an [HTTP Source](https://help.sumologic.com/Send-Data/Sources/02Sources-for-Hosted-Collectors/HTTP-Source) is needed.
- Currently the script just provides the time it took to execute in the command line output; however, there’s potentially more data that can be harvested from the New Relic API to send over in the script.

## Script Flow/Logic
1. Gets a list of the available New Relic apps for the API key
2. Iterates through each app:
   1. Get the metrics available for each app
   2. Format a list of those metric names
   3. Get all the available metric data from the metric list.
   4. Format the metric in [Carbon 2.0](https://help.sumologic.com/Send-Data/Sources/02Sources-for-Hosted-Collectors/HTTP-Source/Upload-Data-to-an-HTTP-Source#Sending_Metric_Data) using [New Relic’s naming conventions](https://docs.newrelic.com/docs/plugins/plugin-developer-resources/developer-reference/metric-naming-reference).
   5. Add the results to a list (metrics_upload)
3. Write the result list (metrics_upload) to a temporary file. (ToDo: replace using the temporary file with a newline delimited string.)
4. Post the temporary file with the metrics to a [Sumo Logic HTTP endpoint](https://help.sumologic.com/Send-Data/Sources/02Sources-for-Hosted-Collectors/HTTP-Source/Upload-Data-to-an-HTTP-Source#Sending_Metric_Data).
5. Print out the time it took to download the metrics so the Sumo Logic Script Source will ingest it.

## Setup
1. Install a [Sumo Logic Installed Collector](https://help.sumologic.com/Send-Data/Installed-Collectors) on a system where the script will reside. 
2. Install newrelic_api SDK. 
   - `sudo pip install newrelic_api`
3. Copy the newrelictosumo.py and newrelic.conf to their own folder.
4. Create a Sumo Logic [Hosted Collector](https://help.sumologic.com/Send-Data/Hosted-Collectors/Configure-a-Hosted-Collector) with a [HTTP Logs and Metrics Source](https://help.sumologic.com/Send-Data/Sources/02Sources-for-Hosted-Collectors/HTTP-Source).
5. Create a [New Relic API key](https://docs.newrelic.com/docs/apis/rest-api-v2/getting-started/api-keys)
6. Edit newrelic.conf variables to the New Relic API key and Sumo Logic HTTP endpoint.
7. Test the script:
   - `python newrelictosumo.py`
   - You should a message like “Took 5.5 ms” once completed. The New Relic APM metrics should also be visible in Sumo Logic in a metrics query for the configured source.
8. Create a [Script Source](https://help.sumologic.com/Send-Data/Sources/01Sources-for-Installed-Collectors/Script-Source) on the installed collector.
9. Configure the Script Source with the following parameters:
   - **Frequency:** 1 minute
   - **Command:**  /bin/sh
   - **Script:** `Type the script to exectue.`
     - `python newrelictosumo.py`
   - **Working Directory:** /absolute/path/to/NewRelicScriptFolder (e.g., /home/ubuntu/NewRelic)
10. Once saved, the script will run every minute. It will generate log messages for the runtime of the script, and it will send 1 minute resolution metrics to the hosted HTTP Logs and Metrics Source.