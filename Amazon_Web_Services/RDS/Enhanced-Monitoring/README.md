# RDS Enhanced Monitoring

![RDS Enhanced Monitoring - Overview dashboard](https://raw.githubusercontent.com/SumoLogic/sumologic-content/master/Amazon_Web_Services/RDS/Enhanced-Monitoring/Screenshots/RDS-Enhanced-Monitoring-Overview.png)

AWS offers monitoring of RDS instances out of the box through CloudWatch Metrics. They also offer a more in-depth monitoring at the OS-level through the use of [Enhanced Monitoring](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Monitoring.OS.html). Enhanced Monitoring sends performance logs to CloudWatch Logs. While Sumo Logic can ingest these performance logs through the use of the standard CloudWatch Logs Lambda function, ingesting them as a timeseries metric will provide more real-time analysis at a fraction of the cost.

## Metric Collection

To ingest the Enhanced Monitoring logs, a modified version of the Lambda function was made to convert them into Carbon 2.0 metric format before sending to Sumo Logic.

Setup of the Lambda function follows the [standard setup as outlined in the Github repository](https://github.com/SumoLogic/sumologic-aws-lambda/tree/master/cloudwatchlogs) for it. Subscribe the function created from rds_enhanced_lambda.js to the CloudWatch Log group created for the Enhanced Monitoring logs (typically RDSOSMetrics).

## App Setup

The app includes 8 dashboards that can be modified for different visualizations and insights.

To install the app, replace all instances of $$RDS with "_sourceCategory=yourSourceCategory".

**Note: This current version does not support Microsoft SQL Server yet. See [AWS documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Monitoring.OS.html) for supported metrics for other engines.**