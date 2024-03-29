# Sumo Logic for Amazon CloudSearch
Sumo Logic Community Content built for Amazon CloudSearch not yet published to the [App Catalog](https://help.sumologic.com/docs/integrations/).

[Amazon CloudSearch](https://aws.amazon.com/cloudsearch/) is an AWS product that allows for rich search capabilities to your website or application. This Sumo Logic app is an overview dashboard that unifies AWS CloudTrail logs and AWS CloudWatch Metrics. It gives insights into indexed objects, search metrics, and resources that have been modified.

![Screenshot-Amazon-CloudSearch-ULM](Screenshot-Amazon-CloudSearch-ULM.png)

### To use the content:
- Download the JSON file(s).
- Find/replace all Source Categories within the JSON with your own Source Category (Ex: sourceCategory=yourSourceCategory).
- [Import](https://help.sumologic.com/docs/get-started/library/#import-content) the content to your desired folder location in Sumo Logic.

### Collection:
For instructions on how to collect logs and metrics for use with content, please see [Sumo Logic Documentation](https://help.sumologic.com/docs/send-data/). For the log portion of the app, you will need to ingest CloudTrail logs. Configure an [AWS CloudTrail Source](https://help.sumologic.com/Send-Data/Sources/02Sources-for-Hosted-Collectors/Amazon_Web_Services/AWS_CloudTrail_Source) to ingest the logs into Sumo Logic. For the metrics portion of the app, you will need to ingest [CloudWatch Metrics](https://help.sumologic.com/Metrics/Metrics-Sources/02Amazon-CloudWatch-Source-for-Metrics) with at least the *AWS/CloudSearch* namespace.

### To upload your own content:
Please see [Sumo Logic Community Ecosystem Apps FAQs](https://help.sumologic.com/docs/integrations/community-ecosystem-apps/#faq).

### To add review/comment to content:
Please provide a review/comment for this content by following the guidelines below:

- Select the **Comments** folder.
- Open the **Comments.json** file.
- Select Edit (pen icon).
- Add a new line below the current comments, and paste in your review/comment using the following schema:

        {
            "reviewer":"[githubid/name]",
            "ratings":{
                "overall":4,
                "use-case":5,
                "design":4,
                "technical":4
            },
            "review":"This app is very useful for knowing x, y, and z. It would be great if the dashboards were broken out by use case instead of being one big dashboard."
        }


- Select **Propose New Changes**.
- Submit **Pull Request**.

Code owners will review and merge your comments on the content to the repo.

Please see [How to add a review/comment to an app](https://help.sumologic.com/docs/integrations/community-ecosystem-apps/#how-do-i-add-a-reviewrating-to-an-app) for more information.