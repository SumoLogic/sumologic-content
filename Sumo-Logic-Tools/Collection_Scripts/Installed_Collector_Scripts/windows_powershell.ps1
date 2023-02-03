#####
# Pre-reqs:
# Generate your install token in Sumo Logic: https://help.sumologic.com/docs/manage/security/installation-tokens/
# Specify the correct collector download URL: https://help.sumologic.com/docs/send-data/installed-collectors/collector-installation-reference/download-collector-from-static-url/
# Create a sources.json file config: https://help.sumologic.com/docs/send-data/use-json-configure-sources/
# Determine the varfile parameters you'd like to use: https://help.sumologic.com/docs/send-data/installed-collectors/collector-installation-reference/user-properties/#userproperties-parameters
#####
# Make the Sumo folder
mkdir C:\sumo
# Download the collector from url (make sure to provide correct URL for deployment)
Invoke-WebRequest 'https://collectors.sumologic.com/rest/download/win64' -outfile 'C:\sumo\SumoCollector.exe'
# Download the sources.json from a repo (Invoke-WebRequest) or bake it into script
# simple write to file for this example (windows events source)
New-Item C:\sumo\sources.json
$contentSources = @"
{
  "api.version":"v1",
  "sources":[{
    "name":"Windows Logs",
    "category":"<ENTER IN A SOURCE CATEGORY>",
    "automaticDateParsing":true,
    "multilineProcessingEnabled":false,
    "useAutolineMatching":false,
    "forceTimeZone":false,
    "filters":[],
    "cutoffRealtiveTime":"-3d",
    "encoding":"UTF-8",
    "eventFormat":1,
    "logNames":["Security","Application","System"],
    "renderMessages":true,
    "sidStyle":2,
    "sourceType":"LocalWindowsEventLog"
  }]
}
"@
Set-Content C:\sumo\sources.json $contentSources
# create varfile with collector parameters (could also pull this from repository with Invoke-WebRequest)
New-Item C:\sumo\sumo_params.txt
$contentParams = @"
sumo.token_and_url=<ENTER INSTALLATION TOKEN>
syncSources=C:\\sumo\\sources.json
collector.name=<ENTER COLLECTOR NAME>
"@
Set-Content C:\sumo\sumo_params.txt $contentParams
# Run the collector with reference to varfile with parameters of choosing
Start-Process C:\sumo\SumoCollector.exe -Wait -ArgumentList "-q","-console","-varfile `"C:\sumo\sumo_params.txt`""