# Incident Tools

## Whats included:
1. Integration YAML File
2. Action YAML Files (Refer to "Action Descriptions" section below for details)

## Disclaimer
The actions included in this integration have been published to App Central under [Incident Tools](https://help.sumologic.com/docs/platform-services/automation-service/app-central/integrations/incident-tools/). They remain here for reference purposes

## To use the content:
- Download the Integration and Action YAML files to your local device.
- Create a new CloudSOAR integration by logging into CloudSOAR > going to Settings (⚙)(top right) > Automation > Integrations > Plus(+) icon > and selecting the Integration YAML file.
- Add any Actions you downloaded to that Integration by selecting the Upload icon (hover over the newly added integration), and uploading the Action YAML file(s).
- For more information on uploading custom Integrations/Actions and how to test them, please see [Working with integrations](https://help.sumologic.com/docs/cloud-soar/cloud-soar-integration-framework/#working-with-integrations).

## Action Descriptions
NOTE: The actions included in this integration have been published to App Central under [Incident Tools](https://help.sumologic.com/docs/platform-services/automation-service/app-central/integrations/incident-tools/). They remain here for reference purposes


### Add External Alert to Incident
- Takes a JSON payload and attaches to a Cloud SOAR incident's "External Alert" section.

### Get External Alert
- Fetches the external alert(s) attached to an incident

  - _Note: You will need to specify yaml output mappings for each external alert you wish to fetch in order for this action to be usable within a playbook._

### Add Entity Metadata
- Searches for the specified entity object (IP, URL, etc.), locates the entity's ID first, and then adds a tag and/or description to this entity.

### Get War Room Timeline
- Grabs the Incident's audit timeline and returns it in JSON format. This is useful for posting to a CIP HTTP source (using 'Generic HTTP POST' action)

### Generic HTTP POST
- Make a generic POST request.
- Usage:
  - **API URL** - The HTTP Endpoint to make the request to.
  - **Request Body as JSON** - a _textarea_ field to build a JSON result using placeholders.
  - **Request Body (output.raw JSON)** - accepts the raw JSON result from the output of a previous action.

### Get Incident
- Fetches Incident data (all fields, related incident IDs, as well as external alert data) and returns it in JSON format. This is useful for posting to a CIP HTTP source (using 'Generic HTTP POST' action)

## To upload your own content:
Please see [Sumo Logic Community Ecosystem Apps FAQs](https://help.sumologic.com/docs/integrations/community-ecosystem-apps/#faq).

## To add review/comment to content:
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
