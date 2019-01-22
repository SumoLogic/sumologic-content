# Sumo Logic for Barracuda

![BarracudaNetworks-WAF-Overview.png](Barracuda_WAF/Screenshots/BarracudaNetworks-WAF-Overview.png)

Contains all Barracuda Networks technology and product lines for which Sumo Logic has content for.

See [Sumo Logic Documentation](https://help.sumologic.com/) for instructions on how to collect logs and metrics for use with content.

To use the content:
Download the raw JSON file(s) and search for (CTRL+F / CMD+F) `$$Barracuda_WAAF` to replace with `_sourceCategory=yourSourceCategory`

## Additional Dashboards

![BarracudaNetworks-WAF-Locations](Barracuda_WAF/Screenshots/BarracudaNetworks-WAF-Locations.png)

![BarracudaNetworks-WAF-Visitors](Barracuda_WAF/Screenshots/BarracudaNetworks-WAF-Visitors.png)

![BarracudaNetworks-WAF-WebServer_Ops](Barracuda_WAF/Screenshots/BarracudaNetworks-WAF-WebServer_Ops.png)

Guidelines PLEASE READ:

To contribute to subfolders or create new subfolders here, please follow the standards below:

1. All application, dashboard and search content in .json format. Please use descriptive naming such as:
   a. Company_TechnologyLine_ContentFunction. E.g. AWS_Kinesis_Errors.json or Sentinel_Vanguard_All.json

2. Relevant screenshot(s) in .png or equivalent format. Naming similar or equivalent to .json content it represents.

3. Create/update a README.md file (like this one) within the folder to track:
   a. Technology and product lines, authors, versions, etc.
   b. Link(s) to relevant 3rd party documentation to specify what types of data need to be collected for content to work.

For more information, see Barracuda documentation here:
[Barracuda logging](https://campus.barracuda.com/product/webapplicationfirewall/doc/4259935/how-to-configure-syslog-and-other-logs/)

2018/04/10 - Updated

  Added Barracuda Full Dashboard Application - author: Jason Hwa
