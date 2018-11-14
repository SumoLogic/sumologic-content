# Sumo Logic for Cisco Meraki

![Cisco_Meraki](Meraki/Screenshots/Cisco_Meraki.png)

Contains all Cisco Meraki technology and product lines for which Sumo Logic has content for.

See [Sumo Logic Documentation](https://help.sumologic.com/) for instructions on how to collect logs and metrics for use with content.

To use this application replace `$$Meraki` with `_sourceCategory=yourSourceCategory` Cisco Meraki in the Cisco_Meraki.json file.

Guidelines PLEASE READ:

To contribute to subfolders or create new subfolders here, please follow the standards below:

1. All application, dashboard and search content in .json format. Please use descriptive naming such as:
   a. Company_TechnologyLine_ContentFunction. E.g. AWS_Kinesis_Errors.json or Sentinel_Vanguard_All.json

2. Relevant screenshot(s) in .png or equivalent format. Naming similar or equivalent to .json content it represents.
   a. More than 1 screenshot? Please create a "Screenshots" folder.

3. Create/update a README.md file (like this one) within the folder to track:
   a. Technology and product lines, authors, versions, etc.
   b. Link(s) to relevant 3rd party documentation to specify what types of data need to be collected for content to work.

2017/12/04 - Updated:

  Meraki - Collect:
  -Cisco Meraki Logs
  For more information, see Cisco's documentation here:
  [Cisco Logging](https://documentation.meraki.com/zGeneral_Administration/Monitoring_and_Reporting/Syslog_Event_Types_and_Log_Samples)
