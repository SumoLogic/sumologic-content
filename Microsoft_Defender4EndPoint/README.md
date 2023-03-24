# Microsoft Defender for EndPoint

Sumo Logic Community Content built for Defender for EndPoint that is not published to the [App Catalog](https://help.sumologic.com/docs/integrations/).

## To use the content

- Download the JSON file(s) in the Dashboards & FERs directory
- Find/replace all Source Categories within the JSON with your own Source Category (Ex: sourceCategory=yourSourceCategory)
- [Import](https://help.sumologic.com/docs/get-started/library/#import-content) the content to your desired folder location in Sumo Logic. More information can be found at

### Collection

Log collection for Microsoft Defender for Endpoint can currently only be done via the use of Azure Event Hubs. For instructions on how to stream Defender for Endpoint logs to an Azure Event Hub, please see [Stream Defender Logs to Azure Event Hub](https://learn.microsoft.com/en-us/microsoft-365/security/defender-endpoint/raw-data-export-event-hub?view=o365-worldwide). Once the logs are streaming to an Azure Event Hub, you can use an Azure Event Hub source to get the logs into Sumo Logic. For instructions on setting up this source, please refer to [Sumo Azure Event Hub Source](https://help.sumologic.com/docs/send-data/hosted-collectors/cloud-to-cloud-integration-framework/azure-event-hubs-source/)

### Content Details

Microsoft Defender for Endpoint helps stop attacks, scales endpoint security resources, and evolves defenses. This dashboard specifically monitors ZAP (Zero-hour auto purge) and phishing-related events that Defender for Endpoint has identified and displays the pertinent details and trends for these events. For more details on ZAP events, please reference the [ZAP Documentation](https://learn.microsoft.com/en-us/microsoft-365/security/office-365-security/zero-hour-auto-purge?view=o365-worldwide).

Microsoft Defender for Endpoint logs a wide variety of events, and each event has a different log schema. Event names are captured in the "category" field of each log message, with most of the event details captured in the "properties" section of each log. For specific details on the log schema for each event that Defender for Endpoint logs, please reference the [Defender Schema Information](https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-schema-tables?view=o365-worldwide).

To make searching across these logs easier and more efficient, install [Field Extraction Rules](https://help.sumologic.com/docs/manage/field-extractions/) using the parsing logic contained in the "Defender4EndPoint_FERS.txt" file in the "Dashboards & FERS" directory. For more details on how to create field extraction rules, please reference [Creating a Field Extraction Rule](https://help.sumologic.com/docs/manage/field-extractions/create-field-extraction-rule/).

### To upload your own content

Please see [Sumo Logic Community Ecosystem Apps FAQs](https://help.sumologic.com/docs/integrations/community-ecosystem-apps/#faq).

### To add review/comment to content

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
