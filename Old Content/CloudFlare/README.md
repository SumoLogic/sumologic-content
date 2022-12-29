# Sumo Logic for CloudFlare

![CloudFlare%20-%20Overview](Screenshots/CloudFlare%20-%20Overview.png)

Contains all CloudFlare technology and product lines for which Sumo Logic has content for.

See [Sumo Logic Documentation](https://help.sumologic.com/) for instructions on how to collect logs and metrics for use with content.

To use this application, replace `$$CloudFlare` with your `_sourceCategory=yourSourceCategory` in the CloudFlare_Logs.json file.

For more information, see CloudFlare's documentation here:
Shipping CloudFlare Logs to Sumo Logic: https://hackernoon.com/how-to-ship-cloudflare-logs-to-sumo-logic-with-lambda-a119e5379f02

## Additional Dashboards

![CloudFlare%20-%20Visitor%20Access%20Types](Screenshots/CloudFlare%20-%20Visitor%20Access%20Types.png)

![CloudFlare%20-%20Visitor%20Locations](Screenshots/CloudFlare%20-%20Visitor%20Locations.png)

![CloudFlare%20-%20Visitor%20Traffic%20Insights.png](Screenshots/CloudFlare%20-%20Visitor%20Traffic%20Insights.png)

![CloudFlare%20-%20Web%20Server%20Operations](Screenshots/CloudFlare%20-%20Web%20Server%20Operations.png)

Guidelines PLEASE READ:

To contribute to subfolders or create new subfolders here, please follow the standards below:

1. All application, dashboard and search content in .json format. Please use descriptive naming such as:
   a. Company_TechnologyLine_ContentFunction. E.g. AWS_Kinesis_Errors.json or Sentinel_Vanguard_All.json

2. Relevant screenshot(s) in .png or equivalent format. Naming similar or equivalent to .json content it represents.
   a. More than 1 screenshot? Please create a "Screenshots" folder.

3. Create/update a README.md file within the subfolder to track:
   a. Authors, versions, dates
   b. Link(s) to relevant 3rd party documentation to specify what types of data need to be collected for content to work.

2018/01/05 - Updated:

  Added CloudFlare content Dashboards (set of 5) - Jason Hwa
