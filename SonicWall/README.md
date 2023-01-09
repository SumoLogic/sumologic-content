# Sumo Logic for SonicWall
Sumo Logic Community Content built for SonicWall that is not published to the [App Catalog](https://help.sumologic.com/docs/integrations/).

![sonicwall_overview](Screenshots/sonicwall_overview.png)

This is a dashboard and parser for SonicWall appliances. The dashboard partially utilizes the parsers as well as the [Optimized Threat Intelligence scheduled view for IP addresses](https://github.com/SumoLogic/sumologic-content/blob/master/Sumo-Logic-Tools/Threat_Intelligence_Optimized/scheduled-views.txt).

### To use the content:
- Download the JSON file(s).
- Find/replace all Source Categories within the JSON with your own Source Category (Ex: sourceCategory=yourSourceCategory).
- [Import](https://help.sumologic.com/docs/get-started/library/#import-content) the content to your desired folder location in Sumo Logic. More information can be found at [Collect Logs for SentinelOne](https://help.sumologic.com/docs/send-data/collect-from-other-data-sources/collect-logs-sentinelone/).

### Collection:
For instructions on how to collect logs and metrics for use with content, please see [Sumo Logic Documentation](https://help.sumologic.com/docs/send-data/).

The SonicWall dashboard has a threat section for threats detected by the Integrated Threat Intelligence on IP addresses. This panel relies upon the Scheduled Views in the [Threat Intel Quick Analysis - Optimized](https://github.com/SumoLogic/sumologic-content/tree/master/Sumo-Logic-Tools/Threat_Intelligence_Optimized) app.

### To upload your own content:
Please see [Sumo Logic Community Ecosystem Apps FAQs](https://help.sumologic.com/docs/integrations/community-ecosystem-apps/#faq).