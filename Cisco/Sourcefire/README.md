# Sumo Logic for Cisco Sourcefire
Sumo Logic Community Content built for Cisco Sourcefire not yet published to the [App Catalog](https://help.sumologic.com/docs/integrations/).

For instructions on how to collect logs and metrics for use with content, please see [Sumo Logic Documentation](https://help.sumologic.com/docs/send-data/). For the log portion of the app, you will need to configure your device to send the logs to a Sumo Logic [syslog source](https://help.sumologic.com/03Send-Data/Sources/01Sources-for-Installed-Collectors/Syslog-Source). Setup a Scheduled View for the `threat_intel_ip_address` view found in the [Threat Intel Optimized app](https://github.com/SumoLogic/sumologic-content/blob/master/Sumo-Logic-Tools/Threat_Intelligence_Optimized/scheduled-views.txt).

This Sumo Logic app is a collection of 3 dashboards that utilizes Sourcefire logs. It gives insights into allowed and blocked traffic. Portions of the app relies on a scheduled view for the integrated Threat Intelligence.

![Cisco-Sourcefire-Overview](Cisco-Sourcefire-Overview.png)

### To use the content:
- Download the JSON file(s).
- Find/replace all Source Categories within the JSON with your own Source Category (Ex: sourceCategory=yourSourceCategory).
- Import the content to your desired folder location in Sumo Logic.

### To upload your own content:
Please see [Sumo Logic Community Ecosystem Apps FAQs](https://help.sumologic.com/docs/integrations/community-ecosystem-apps/#faq).