# ServiceNow CloudSOAR Integration for Sumo Logic
Sumo Logic Custom CloudSOAR Integration for ServiceNow, provided by the community. A similar Integration is already provided out-of-the-box in the SOAR App Central, however this particular integration includes an additional daemon that allows you to pull from **any** ServiceNow table, as opposed to just the Incident daemon provided OOTB.

### Whats included:
1. Integration YAML File: Integration configurations and test code (different from OOTB Integration)
2. Action YAML File(s):
    - Create Ticket (Notification) - Inserts one record in the specified table
    - Update Ticket (Notification) - Updates the specified record with the name-value pairs included in the request body
    - Close Ticket (Containment) - Closes a ticket specified by the System ID
    - Get Ticket Details (Enrichment) - Retrieve a record from a table
    - Search Tickets (Enrichment) - Retrieve a record from a table
    - ServiceNow Incidents Daemon (Daemon) - Automatically retrieves new tickets
    - ServiceNow Table Daemon (Daemon) - Automatically retrieves new records from specified table name

### To use the content:
- Download the Integatration and Action YAML files to your local device.
- Create a new CloudSOAR integration by logging into CloudSOAR > going to Settings cogwheel (top right) > Automation > Integrations > Plus(+) icon > and selecting the Integration YAML file.
- Add any Actions you downloaded to that Integration by selecting the Upload icon (hover over the newly added integration), and uploading the Action YAML file(s).
- For more information on uploading custom Integrations/Actions and how to test them, please see [Working with integrations](https://help-opensource.sumologic.com/docs/cloud-soar/cloud-soar-integration-framework/#working-with-integrations).

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