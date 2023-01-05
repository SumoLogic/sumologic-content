# Sumo Logic for Amazon CloudSearch
Sumo Logic Community Content built for Amazon CloudSearch not yet published to the [App Catalog](https://help.sumologic.com/docs/integrations/).

[Amazon CloudSearch](https://aws.amazon.com/cloudsearch/) is an AWS product that allows for rich search capabilities to your website or application. This Sumo Logic app is an overview dashboard that unifies AWS CloudTrail logs and AWS CloudWatch Metrics. It gives insights into indexed objects, search metrics, and resources that have been modified.

For instructions on how to collect logs and metrics for use with content, please see [Sumo Logic Documentation](https://help.sumologic.com/docs/send-data/). For the log portion of the app, you will need to ingest CloudTrail logs. Configure an [AWS CloudTrail Source](https://help.sumologic.com/Send-Data/Sources/02Sources-for-Hosted-Collectors/Amazon_Web_Services/AWS_CloudTrail_Source) to ingest the logs into Sumo Logic. For the metrics portion of the app, you will need to ingest [CloudWatch Metrics](https://help.sumologic.com/Metrics/Metrics-Sources/02Amazon-CloudWatch-Source-for-Metrics) with at least the *AWS/CloudSearch* namespace.

![Screenshot-Amazon-CloudSearch-ULM](Screenshot-Amazon-CloudSearch-ULM.png)

### To use the content:
- Download the JSON file(s).
- Find/replace all Source Categories within the JSON with your own Source Category (Ex: sourceCategory=yourSourceCategory).
- [Import](https://help.sumologic.com/docs/get-started/library/#import-content) the content to your desired folder location in Sumo Logic.

### To upload your own content:
Please see [Sumo Logic Community Ecosystem Apps FAQs](https://help.sumologic.com/docs/integrations/community-ecosystem-apps/#faq).