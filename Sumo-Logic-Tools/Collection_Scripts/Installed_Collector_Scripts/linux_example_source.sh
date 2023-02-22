#! /bin/bash

#download collector from static URL, make sure to use correct URL
#link to urls: https://help.sumologic.com/03Send-Data/Installed-Collectors/05Reference-Information-for-Collector-Installation/02Download-a-Collector-from-a-Static-URL
curl "https://collectors.sumologic.com/rest/download/linux/64" --output SumoCollector.sh

#make executable
chmod +x SumoCollector.sh

#sources json - used to configure sources on the collector if you with
#this can also be done in the UI instead
#NEED TO EDIT TO YOUR USE CASE, this example has system auth logs for EC2 linux
#see this link for more info on local configuration file management: https://help.sumologic.com/03Send-Data/Sources/03Use-JSON-to-Configure-Sources/Local-Configuration-File-Management/Local-File-Configuration-Management-for-New-Collectors-and-Sources
cat > /tmp/sources.json << EOF
{
  "api.version":"v1",
  "sources":[{
    "name":"AuthLogs",
    "category":"test/collection",
    "automaticDateParsing":true,
    "multilineProcessingEnabled":true,
    "useAutolineMatching":true,
    "forceTimeZone":false,
    "filters":[],
    "cutoffRelativeTime":"-1h",
    "encoding":"UTF-8",
    "hostName":"test-host-name"
    "fields":{
      
    },
    "denylist":[],
    "pathExpression":"/var/log/auth.log*",
    "sourceType":"LocalFile"
  }]
}
EOF

#Run the script with the parameters that you want to configure (need Access Key and ID from Sumo, and sources).
#By default the Collector will be installed in either /opt/SumoCollector or /usr/local/SumoCollector.
#sources needs to be absolute filepath
sudo ./SumoCollector.sh -q -Vsumo.accessid=<ACCESS ID> -Vsumo.accesskey=<ACCESS KEY> -Vsources=/tmp/sources.json -Vcollector.name=Test Collector Name