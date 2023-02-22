# Microsoft Teams 

This is a dashboard for Microsoft Teams audit logs.

Microsoft Teams audit logs include audit activity such as:

* Added channel/members/connector
* Changed setting/role
* Created team
* Deleted org/app/channel/team/app
* Removed connector/members/tab
* Uninstalled app
* Updated app
* User signed in to Teams


Notice: Microsoft Teams audit logs does not include user activity other than number of user logins.


# Set up and collection

Microsoft Teams audit logs are included in Office 365 General Logs.
So if you are already ingesting Office 365 General Logs, you are already ingesting Microsoft Teams logs. 
so you don't need to set up new thing.

If you didn't ingest Microsoft logs yet, please follow our [help](https://help.sumologic.com/03Send-Data/Sources/02Sources-for-Hosted-Collectors/Microsoft-Office-365-Audit-Source) to ingest Office 365 General Logs.

# Update Source Categories
Update source categories:

Microsoft Teams: Update $o365 to yourSourceCategory
