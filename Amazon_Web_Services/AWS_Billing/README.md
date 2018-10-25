#Sumo Logic application for AWS/Billing Cloudwatch metrics

Contains Dashboards for AWS Billing Cloudwatch Metrics.

To use the content:
1. Collect [AWS Cloudwatch Metrics](https://help.sumologic.com/03Send-Data/Sources/02Sources-for-Hosted-Collectors/Amazon_Web_Services/Amazon_CloudWatch_Source_for_Metrics) from the AWS/Billing namespace. Note: Ensure you have enabled billing alerts in your AWS account to get these metrics.
2. Download the raw JSON file and search for (CTRL+F / CMD+F) "_sourceCategory=*" to replace with "_sourceCategory=yourSourceCategory"

[This dashboard provides high level insights into your AWS billing. The "Total AWS Charges" and "Total AWS Charges per minute" panels All of these metrics can be alerted off of as well.](https://raw.githubusercontent.com/SumoLogic/sumologic-content/master/Amazon_Web_Services/AWS_Billing/AWS_Billing_Dash.png)





See [Sumo Logic Documentation](https://help.sumologic.com/) for instructions on how to collect logs and metrics for use with content.

Guidelines PLEASE READ:

To contribute to subfolders or create new subfolders here, please follow the standards below:

1. All application, dashboard and search content in .json format. Please use descriptive naming such as:
   a. Company_TechnologyLine_ContentFunction. E.g. AWS_Kinesis_Errors.json or Sentinel_Vanguard_All.json

2. Relevant screenshot(s) in .png or equivalent format. Naming similar or equivalent to .json content it represents.

3. Create/update a README.md file (like this one) within the folder to track:
   a. Technology and product lines, authors, versions, etc.
   b. Link(s) to relevant 3rd party documentation to specify what types of data need to be collected for content to work.
