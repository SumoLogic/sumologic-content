Contains all MimeCast product lines for which Sumo Logic has content for.

See [Sumo Logic Documentation](https://help.sumologic.com/) for instructions on how to collect logs and metrics for use with content.
**In addition, for MimeCast log collection, please refer to Sumo Logic Data Collection for MimeCast.docx in this repo**

To use the content:

1. Collect MimeCast MTA and Audit logs with scripts located in the SumoLogic Mimecast Data Collection folder.
2. Download the raw JSON file(s) and search for (CTRL+F / CMD+F) "<REPLACEME>" to replace with your appropriate _sourceCategory.

Guidelines PLEASE READ:

To contribute to subfolders or create new subfolders here, please follow the standards below:

1. All application, dashboard and search content in .json format. Please use descriptive naming such as:
   a. Company_TechnologyLine_ContentFunction. E.g. AWS_Kinesis_Errors.json or Sentinel_Vanguard_All.json

2. Relevant screenshot(s) in .png or equivalent format. Naming similar or equivalent to .json content it represents.

3. Create/update a README.md file (like this one) within the folder to track:
   a. Technology and product lines, authors, versions, etc.
   b. Link(s) to relevant 3rd party documentation to specify what types of data need to be collected for content to work.

For more information, see MimeCast documentation here:
[MimeCast logs](https://www.mimecast.com/developer/documentation/get-siem-logs/)

2018/06/05 - Updated

  Added MimeCast Searches, Dashboards, Python Collection Script, Collection Instructions, Screenshots - author: Jason Hwa
