Contains all Proofpoint and product lines for which Sumo Logic has content for.

See [Sumo Logic Documentation](https://help.sumologic.com/) for instructions on how to collect logs and metrics for use with content.

For more information, see Proofpoint's Youtube here:
[Proofpoint Logging](https://www.youtube.com/watch?v=qPOgaXB6xBw)


To use the dashboards, replace $$Proofpoint with "_sourceCategory=yourSourceCategory".


Guidelines PLEASE READ:

To contribute to subfolders or create new subfolders here, please follow the standards below:

1. All application, dashboard and search content in .json format. Please use descriptive naming such as:
   a. Company_TechnologyLine_ContentFunction. E.g. AWS_Kinesis_Errors.json or Sentinel_Vanguard_All.json

2. Relevant screenshot(s) in .png or equivalent format. Naming similar or equivalent to .json content it represents.
   a. More than 1 screenshot? Please create a "Screenshots" folder.

3. Create/update a README.md file (like this one) within the folder to track:
   a. Technology and product lines, authors, versions, etc.
   b. Link(s) to relevant 3rd party documentation to specify what types of data need to be collected for content to work.

2018/04/24 - Updated:

  Generic Product - Collect
  - Proofpoint Logs
  For more information, see Proofpoint's documentation here:
  [Proofpoint Logging](https://youtu.be/qPOgaXB6xBw?t=2m6s)
  - This syslog forwarding do requires syslog over TLS so setting up a syslog-ng or rsyslog to accepted encrypted syslog is required.

  There is also an SIEM API method that can be customized to extract data from Proofpoint into Sumo Logic, but that is not in scope for this App (https://help.proofpoint.com/Threat_Insight_Dashboard/API_Documentation/SIEM_API).