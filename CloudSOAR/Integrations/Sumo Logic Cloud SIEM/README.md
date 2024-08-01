# Sumo Logic Cloud SIEM

## Whats included:
Additional Action YAML Files that can be used with the OOTB Sumo Logic Cloud SIEM Integration (Refer to "Action Descriptions" section below for details).

**Note:** In order to use this action, the OOTB Sumo Logic Cloud SIEM integration must be duplicated, and the name of the integration must also match the integration name specified at the top of the Action file.

## Disclaimer
This integration is in active development. Actions, or the parameters defined therin may change in subsequent releases.

## To use the content:
- Download the Integration and Action YAML files to your local device.
- Create a new Cloud SOAR integration by logging into CloudSOAR > going to Settings (⚙)(top right) > Automation > Integrations > Plus(+) icon > and selecting the Integration YAML file.
- Add any Actions you downloaded to that Integration by selecting the Upload icon (hover over the newly added integration), and uploading the Action YAML file(s).
- For more information on uploading custom Integrations/Actions and how to test them, please see [Working with integrations](https://help-opensource.sumologic.com/docs/cloud-soar/cloud-soar-integration-framework/#working-with-integrations).

## Action Descriptions 
### Add Indicator to Threat Intel Source
- Accepts a single IP, or comma-separated list of IPs and searches for IOCs using Sumo Logic's [threatip()](https://help-opensource.sumologic.com/docs/search/search-query-language/search-operators/threatip/) operator. 
### Create Threat Intel Source
- Creates a [Threat Intel Source](https://help.sumologic.com/docs/cse/rules/about-cse-rules/#threat-intelligence) in Cloud SIEM.
### Get Threat Intel Indicator
- Fetches an threat intel indicator by ID [API Reference](https://api.sumologic.com/docs/sec/#operation/GetThreatIntelIndicator)
### List Threat Intel Indicators
- Lists threat intel indicators with filter options [API Reference](https://api.sumologic.com/docs/sec/#operation/GetThreatIntelIndicators)
### List Threat Intel Sources
- Lists threat intel sources in Cloud SIEM [API Reference](https://api.sumologic.com/docs/sec/#operation/GetThreatIntelligenceSources)
### Remove Indicator from Threat Intel Source
- Removes a threat intel indicator from Cloud SIEM [API Reference](https://api.sumologic.com/docs/sec/#operation/DeleteThreatIntelIndicator)
### Update Indicator to Threat Intel Source
- Updates a threat intel indicator in Cloud SIEM [API Reference](https://api.sumologic.com/docs/sec/#operation/UpdateThreatIntelIndicator)

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
