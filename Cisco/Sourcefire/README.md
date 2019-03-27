# Cisco Sourcefire

![Cisco-Sourcefire-Overview](Cisco-Sourcefire-Overview.png)


This Sumo Logic app is a collection of 3 dashboards that utilizes Sourcefire logs. It gives insights into allowed and blocked traffic. Portions of the app relies on a scheduled view for the integrated Threat Intelligence.

## Log Collection

For the log portion of the app, you will need to configure your device to send the logs to a Sumo Logic [syslog source](https://help.sumologic.com/03Send-Data/Sources/01Sources-for-Installed-Collectors/Syslog-Source).

## Sumo Logic Threat Intelligence

Setup a Scheduled View for the `threat_intel_ip_address` view found in the [Threat Intel Optimized app](https://github.com/SumoLogic/sumologic-content/blob/master/Sumo-Logic-Tools/Threat_Intelligence_Optimized/scheduled-views.txt).

## Setup and Installation

Using the Cisco-Sourcefire.json, perform a find-and-replace for `_sourceCategory=$$CiscoSourcefire` with your appropriate scope for Cisco Sourcefire logs.

Import the modified JSON into your Sumo Logic library.