# Sumo Logic Dashboards for Cloudflare
Sumo Logic Community Content built for Cloudflare DNS Logs and Cloudflare Zero Trust Access Audit Logs, Network Session Data, Audit Activity that is not published to the [App Catalog](https://help.sumologic.com/docs/integrations/).

#### Cloudflare DNS Logs Dashboard
![Cloudflare DNS Log Dashboard](Screenshots/Cloudflare_DNS.png)

#### Cloudflare Zero Trust Access, Network Session Data, and Audit Activity Log Dashboard
![Cloudflare Zero Trust Access and Network Session Dashboard](Screenshots/Cloudflare_Zero_Trust.png)


### To use the content:
- Download the JSON file.
- Find/replace all Source Categories within the JSON with your own Source Category (Ex: sourceCategory=yourSourceCategory).
- [Import](https://help.sumologic.com/docs/get-started/library/#import-content) the content to your desired folder location in Sumo Logic.
 
### Collection:
For instructions on how to collect logs for use with this content, please see [Sumo Logic Documentation](https://help.sumologic.com/docs/integrations/saas-cloud/cloudflare/#collecting-logs-for-cloudflare). 

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