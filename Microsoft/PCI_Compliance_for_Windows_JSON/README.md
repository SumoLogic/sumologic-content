# PCI Compliance for Windows JSON

This is an updated version of the [PCI Compliance for Windows app](https://help.sumologic.com/07Sumo-Logic-Apps/04Microsoft-and-Azure/PCI_Compliance_for_Windows/PCI-Compliance-for-Windows-App-Dashboards). It is updated to work with Windows Event Logs in the JSON formatted syntax. It is also utilizing the new Sumo Logic dashboard framework. 

## Setup

### Setup Collection

This app only requires a [standard Windows Event source(s)](https://help.sumologic.com/03Send-Data/Sources/01Sources-for-Installed-Collectors/Local-Windows-Event-Log-Source) configured for the JSON-formatted event logs by selected **Collect using JSON format** in the _Event Format_ section. 

### Modify Dashboard JSON

Prior to importing the app, find and replace all instances of _\_sourceCategory=windows/events_ with your appropriate metadata for your Windows Event logs.


### Import App

Import your modified version of the JSON file into Sumo Logic.
