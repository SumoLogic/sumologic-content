# Sumo Logic Dashboard for Monitoring Automation Service Action and Playbooks
Sumo Logic Community Content built for Monitoring Action and Playbooks in Automation Service or Cloud SOAR that is not published to the [App Catalog](https://help.sumologic.com/docs/integrations/).

![Playbook Monitoring Dashboard](Screenshots/github_actions_screenshot.png)

### To use the content:
- Download the JSON file(s).
- [Import](https://help.sumologic.com/docs/get-started/library/#import-content) the content to your desired folder location in Sumo Logic.

### Collection:
This dashboard using Sumo Logic's built-in audit indexes (_index=sumologic_audit_events or _index=sumologic_system_events): [System Event Index](https://help.sumologic.com/docs/manage/security/audit-indexes/system-event-index/).

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

Author: Kalise Richmond
