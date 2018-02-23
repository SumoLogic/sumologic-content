## This repo shows examples of how to create a new Zendesk ticket from a Sumo Logic Alert or Scheduled Search.

For more information, see Zendesk's API documentation here: https://developer.zendesk.com/rest_api/docs/core/tickets#create-ticket

After you've set up your search or alert, follow these steps inside Sumo Logic:

1.)	Go to Manage > Connections
2.)	Select Add
3.)	Select Webhook
4.)	Enter the following details

a.	Name: The name for your Webhook
b.	Description: A description for your Webhook
c.	URL: Your Zendesk subdomain and path to the Create Ticket API. 

Example: 

https://{YOUR_SUBDOMAIN}.zendesk.com/api/v2/tickets.json

d.	Authentication Header: Your Base 64 encoded Zendesk API credentials. For more information, see the SUmo Logic     documentation here: https://help.sumologic.com/Manage/Connections-and-Integrations/Webhook-Connections/About-Webhook-Connections#Example_Authorization_Header

Example: 

Basic <your base 64 encoded “user:password”>

or 

Basic <your base 64 encoded “username/token:<api token>”

e.	Payload: The payload you wish to send to Zendesk to create the ticket. This needs to be in the format accepted by  Zendesk based on their Create Ticket API.

Example:

{
	"ticket": {
		"subject": "Alert fired for $SearchName",
		"comment": {
			"body": " timerange: $TimeRange \n firetime: $FireTime \n num: $NumRawResults \n agg: $AggregateResultsJson \n raw: $RawResultsJson"
		},
		"priority": "high"
	}
}

f.	Test your Connection.
