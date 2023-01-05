# Sumo Logic for Chef
Sumo Logic Community Content built for Chef not yet published to the [App Catalog](https://help.sumologic.com/docs/integrations/).

For instructions on how to collect logs and metrics for use with content, please see [Sumo Logic Documentation](https://help.sumologic.com/docs/send-data/). These dashboards use either the Chef client logs, or via a [Chef Handler](https://github.com/duchatran/chef-handler-sumologic). You will need to integrate these as part of your flow (e.g setup a Sumo [local file source](https://help.sumologic.com/Send-Data/Sources/01Sources-for-Installed-Collectors/Local-File-Source) to collect the local client logs).

### To use the content:
- Download the JSON file(s).
- Find/replace all Source Categories within the JSON with your own Source Category (Ex: sourceCategory=yourSourceCategory).
- [Import](https://help.sumologic.com/docs/get-started/library/#import-content) the content to your desired folder location in Sumo Logic.

### To upload your own content:
Please see [Sumo Logic Community Ecosystem Apps FAQs](https://help.sumologic.com/docs/integrations/community-ecosystem-apps/#faq).