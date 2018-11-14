Contains all Chef product lines for which Sumo Logic has content for.

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


# Log collection:
+ The dashboards in the content use either the Chef client logs, or via a [Chef Handler](https://github.com/duchatran/chef-handler-sumologic). You will need to integrate these as part of your flow (e.g setup a Sumo [local file source](https://help.sumologic.com/Send-Data/Sources/01Sources-for-Installed-Collectors/Local-File-Source) to collect the local client logs)

# Setup:
+ First search and replace all instances of `$$Chef` in the source file (Chef.json) with `_sourceCategory=yourSourceCategory`
+ Import Chef.json via the Sumo [console](https://help.sumologic.com/Search/Library/Export-and-Import-Content-in-the-Library)

2018/04/17:
	Add content and README file. 
