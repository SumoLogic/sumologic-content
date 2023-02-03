# Sumo Logic for Lacework
Sumo Logic Community Content built for Lacework that is not published to the [App Catalog](https://help.sumologic.com/docs/integrations/).

This is a dashboard for analyzing, trending and investigating your Lacework Alerts. It will allow you to see alerts from your Lacework account, including compliance, agent, and account based alerts. You can also filer by alert severity in the dashboard to focus on what is important to you.

![Screenshot-Lacework-alerts-Overview](Screenshot/LaceWorkAlertsOverview.png)

### To use the content:
- Download the JSON file(s).
- Find/replace all Source Categories within the JSON with your own Source Category (Ex: sourceCategory=yourSourceCategory).
- [Import](https://help.sumologic.com/docs/get-started/library/#import-content) the content to your desired folder location in Sumo Logic.

### Collection:
For instructions on how to collect logs and metrics for use with content, please see [Sumo Logic Documentation](https://help.sumologic.com/docs/send-data/). If you aren't already sending your Lacework alerts to Sumo Logic, you can follow the simple steps below:

1. Create an https logs source in Sumo Logic. This can be done on a new or existing hosted collector in your account. Follow [this document](https://github.com/SumoLogic/sumologic-content/issues) to create the https logs source. Note the endpoint that is created, this will be used in step 2. Ensure a value is input for _sourceCategory.

2. Now you can create a custom Lacework webhook alert channel that is pointed toward the Sumo Logic https logs endpoint created in step 1. Follow [this Lacework document](https://support.lacework.com/hc/en-us/articles/360034367393-Webhook) to create the webhook alert channel. The value for the "Webhook URL", will be the endpoint you created in step 1.

### To upload your own content:
Please see [Sumo Logic Community Ecosystem Apps FAQs](https://help.sumologic.com/docs/integrations/community-ecosystem-apps/#faq).

### To add a review to content:
Please provide a comment for this content by following the guidelines below:

- Select the **Comments** folder.
- Open the **Comments.json** file.
- Select Edit (pen icon).
- Add a new line below the current comments, and paste in your ratings/comments using the following schema:

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

Code owners will review and merge your rating of the content to the repo.

Please see [How to add a review/rating to an app](https://help.sumologic.com/docs/integrations/community-ecosystem-apps/#how-do-i-add-a-reviewrating-to-an-app) for more information.