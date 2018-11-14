# Sophos UTM

![Sophos UTM - Overview](https://raw.githubusercontent.com/SumoLogic/sumologic-content/master/Sophos/UTM/Screenshots/Screenshot-Sophos-UTM-Overview.png)


This is an app for Sophos UTM. It contains dashboards for an overview, blocked traffic, dropped packets, accepted traffic,  and threats per the Sumo Logic Integrated Threat Intelligence. 

Sophos UTM logs are collected through syslog, and the Threat Intelligence relies on the [Threat Intelligence Quick Analysis Optimized](https://github.com/SumoLogic/sumologic-content/tree/master/Sumo-Logic-Tools/Threat_Intelligence_Optimized) scheduled views. 


## Setup

### Setup Field Extraction Rules

The Sophos UTM app's queries heavily rely on Field Extraction Rules found in sophos-utm-field-extraction-rules.txt. Setup the FERs prior to installing the app. Optionally, you can modify the dashboards to use query-time parsing instead of FERs.

### Setup Threat Intel Scheduled Views

The Sophos UTM app has a threat dashboard for threats detected by Sumo Logic's integrated threat intelligence with Crowdstrike.

This dashboard relies upon the Scheduled Views in the [Threat Intel Quick Analysis - Optimized](https://github.com/SumoLogic/sumologic-content/blob/master/Sumo-Logic-Tools/Threat_Intelligence_Optimized/scheduled-views.txt) app. Use the standard index names specified in the text document.

### Update Source Categories

Update source categories to the appropriate one(s):

Update `*$$Sophos*` to `_sourceCategory=yourSourceCategory`

### Import App

Import the Sophos-UTM.json into Sumo Logic. Once imported, the app should automatically be setup to query against Sophos UTM logs.

### Additional Dashboards

![Screenshot-Sophos-UTM-Blocked-Traffic](Screenshots/Screenshot-Sophos-UTM-Blocked-Traffic.png)

![Screenshots/Screenshot-Sophos-UTM-Dropped-Packets](Screenshots/Screenshot-Sophos-UTM-Dropped-Packets.png)

![Screenshot-Sophos-UTM-Traffic](Screenshots/Screenshot-Sophos-UTM-Traffic.png)

![Screenshot-Sophos-UTM-Threat-Intelligence](Screenshots/Screenshot-Sophos-UTM-Threat-Intelligence.png)
