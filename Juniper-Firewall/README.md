# Juniper Firewall

This is an app for the Juniper Firewall. It contains dashboard for an overview, accepted traffic, denied traffic, and threats per the Sumo Logic Integrated Threat Intelligence. 

Juniper logs are collected through syslog, and the Threat Intelligence relies on the [Threat Intelligence Quick Analysis Optimized](https://github.com/SumoLogic/sumologic-content/tree/master/Sumo-Logic-Tools/Threat_Intelligence_Optimized) scheduled view for IP addresses. 


## Setup

### Setup Field Extraction Rules

The Juniper app's queries heavily rely on Field Extraction Rules found in juniper-field-extraction-rules.txt. Setup the FERs prior to installing the app. Optionally, you can modify the dashboards to use query-time parsing instead of FERs.

### Setup Threat Intel Scheduled Views

The Juniper app has a threat dashboard for threats detected by Sumo Logic's integrated threat intelligence with Crowdstrike.

This dashboard relies upon the IP Scheduled View in the [Threat Intel Quick Analysis - Optimized](https://github.com/SumoLogic/sumologic-content/blob/master/Sumo-Logic-Tools/Threat_Intelligence_Optimized/scheduled_views.txt) app (Index Name: threat_intel_ip_address).

### Update Source Categories

Update source categories to the appropriate one(s):

Replace $$Juniper with "_sourceCategory=yourSourceCategory"

### Import App

Once imported, the app should automatically be setup to query against Juniper Firewall logs. 