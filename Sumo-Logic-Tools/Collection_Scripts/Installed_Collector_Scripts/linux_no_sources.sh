#! /bin/bash

#download collector from static URL, make sure to use correct URL
#link to urls: https://help.sumologic.com/03Send-Data/Installed-Collectors/05Reference-Information-for-Collector-Installation/02Download-a-Collector-from-a-Static-URL
curl "https://collectors.sumologic.com/rest/download/linux/64" --output SumoCollector.sh


#make executable
chmod +x SumoCollector.sh


#Run the script with the parameters that you want to configure (need Access Key and ID from Sumo, and sources).
#By default the Collector will be installed in either /opt/SumoCollector or /usr/local/SumoCollector.
sudo ./SumoCollector.sh -q -Vsumo.accessid=<ACCESS ID> -Vsumo.accesskey=<ACCESS KEY> -Vcollector.name=Test Collector Name