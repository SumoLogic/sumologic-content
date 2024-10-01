# Sumo Logic for AWS Health Events
Sumo Logic Community Content built for AWS Health Events that are not yet published to the [App Catalog](https://help.sumologic.com/docs/integrations/).

This content provides a way to forward AWS Health Events to a [Sumo Logic HTTP Source](https://help.sumologic.com/docs/send-data/hosted-collectors/http-source/logs-metrics/) using Amazon EventBridge. The integration from EventBridge leverages the [Sumo Logic Partner Destination](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-api-destination-partners.html#:~:text=HEC%20token%20ID.-,Sumo%20Logic,-API%20destination%20invocation). For more information on AWS Health Events forwarding, please see [Monitoring AWS Health events with Amazon EventBridge](https://docs.aws.amazon.com/health/latest/ug/cloudwatch-events-health.html).

### To use the content:
**For A Single Account:**
- Copy/download the two Cloudformation templates (1-aws-health-events-to-sumo-logic-iam-role.yaml and 2-aws-health-events-to-sumo-logic-event-rule.yaml).
- Run the IAM Role template in the AWS Account you want to collect from first, and copy the ARN output for the IAM Role. **Only create this Role once per AWS Account.**
- Run the Event Rule template and provide the [Sumo Logic HTTP Source URL](https://help.sumologic.com/docs/send-data/hosted-collectors/http-source/logs-metrics/) and the output IAM Role ARN from the first template. Run this template in any Region you want to collect health events from.

**For Multi Account/Region:**
- Copy/download the two Cloudformation templates (1-aws-health-events-to-sumo-logic-iam-role.yaml and 2-aws-health-events-to-sumo-logic-event-rule.yaml).
- Run the IAM Role template in each AWS Account you want to collect from first, and copy the ARN output for the IAM Role. **Only create this Role once per AWS Account.**
- Use Cloudformation StackSets to run the Event Rule template in multiple accounts/regions, and provide the [Sumo Logic HTTP Source URL](https://help.sumologic.com/docs/send-data/hosted-collectors/http-source/logs-metrics/) and the output IAM Role ARN from the first template.

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