## Usage:

> **NOTE:** you **MUST** find and replace `$$HaProxy` in the content json (currently `$$HAProxy`) with a suitable string to match your HA Proxy logs ie. ("_sourceCategory=yourSourceCategory").


Contains all HA Proxy technology and product lines for which Sumo Logic has content for.

See [HA Proxy Documentation](https://www.haproxy.com/blog/haproxy-log-customization/) for standard HA Proxy the logging format and fields that this content was developed for.

See [Sumo Logic Documentation](https://help.sumologic.com/) for instructions on how to collect logs and metrics for use with content.

Guidelines PLEASE READ:

To contribute to subfolders or create new subfolders here, please follow the standards below:

1. All application, dashboard and search content in .json format. Please use descriptive naming such as:
   a. Company_TechnologyLine_ContentFunction. E.g. AWS_Kinesis_Errors.json or Sentinel_Vanguard_All.json

2. Relevant screenshot(s) in .png or equivalent format. Naming similar or equivalent to .json content it represents.
   a. More than 1 screenshot? Please create a "Screenshots" folder.

3. Create/update a README.md file (like this one) within the folder to track:
   a. Technology and product lines, authors, versions, etc.
   b. Link(s) to relevant 3rd party documentation to specify what types of data need to be collected for content to work.
