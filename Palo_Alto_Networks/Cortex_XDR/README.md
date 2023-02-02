# Sumo Logic for Palo Alto Cortex XDR
Sumo Logic Community Content built for Palo Alto Cortex XDR that is not published to the [App Catalog](https://help.sumologic.com/docs/integrations/).

This folder contains a pre-built dashboard for Palo Alto Networks Cortex XDR Alerts/Events. It is recommended that you link this dashboard as a [contex action](https://help.sumologic.com/docs/cse/administration/create-cse-context-actions/) from CSE to filter by hostname/ip. Note - This dashboard assumes that only "Ingest Associated Events" is enabled for the [Palo Alto Cortex XDR Source](https://help.sumologic.com/docs/send-data/hosted-collectors/cloud-to-cloud-integration-framework/palo-alto-cortex-xdr-source/).

![screenshot](Screenshots/Screenshot%202023-02-02%20at%201.20.56%20PM.png)

### To use the content:
- Download the JSON file(s).
- Find/replace all Source Categories within the JSON with your own Source Category (Ex: sourceCategory=yourSourceCategory).
- [Import](https://help.sumologic.com/docs/get-started/library/#import-content) the content to your desired folder location in Sumo Logic.

### Collection:
For instructions on how to collect logs and metrics for use with content, please see [Sumo Logic Documentation](https://help.sumologic.com/docs/send-data/). See [Palo Alto Cortex XDR Source](https://help.sumologic.com/docs/send-data/hosted-collectors/cloud-to-cloud-integration-framework/palo-alto-cortex-xdr-source/) for easy setup.

### To upload your own content:
Please see [Sumo Logic Community Ecosystem Apps FAQs](https://help.sumologic.com/docs/integrations/community-ecosystem-apps/#faq).

### To add a review to content:
Please follow [How to add a review/rating to an app](https://help.sumologic.com/docs/integrations/community-ecosystem-apps/#how-do-i-add-a-reviewrating-to-an-app)