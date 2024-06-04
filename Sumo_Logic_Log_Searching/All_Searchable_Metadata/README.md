# Sumo Logic All Searchable Metadata
Sumo Logic Dashboards for Searching existing log data in your account.

This consists of 3 dashboards (leveraging built-in metadata):
- All Searchable Log Metadata - does not consider your log access permissions
- Searchable Log Metadata Available To Me - does consider your log access permissions, but only searches data in Continuous tier
- All Searchable Metrics Metadata

![all_searchable_logs](screenshots/all_searchable_logs.png)
![all_searchable_metrics](screenshots/all_searchable_metrics.png)
![all_continuous](screenshots/all_continuous.png)

### To use the content:
- Make sure you have the Data Volume Index enabled.
- Download the JSON file(s).
- [Import](https://help.sumologic.com/docs/get-started/library/#import-content) the content to your desired folder location in Sumo Logic.

### Collection:
For instructions on how to collect logs, metrics, or traces for use with content, please see [Sumo Logic Documentation](https://help.sumologic.com/docs/send-data/).

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