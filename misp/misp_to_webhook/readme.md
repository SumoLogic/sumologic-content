# MISP to Sumo Logic webhook

This Python script allows you to send data from a MISP instance to a Sumo Logic endpoint using webhooks.

## Prerequisites

1. You need to have a Sumo Logic account.
2. You need to have a MISP instance.
3. You need to create a Sumo Logic HTTP source to receive the data from the webhook.
4. You need to obtain your MISP API key and set it as an environment variable named "misp_api_key".

## Usage

1. Download the script to your local machine.
2. Run the script with python scriptname.py.
3. Enter the MISP URL and Sumo Logic endpoint URL when prompted.
4. The script will send the data from the MISP instance to the Sumo Logic endpoint using webhooks.

## Notes

- This script uses the MISP API to get the data from the MISP instance. You can customize the request data in the script to get different data from the MISP instance.
- The script paginates through the results from the MISP API request and sends them to the Sumo Logic endpoint using webhooks.
- If the script encounters an error while sending data to the Sumo Logic endpoint, it will raise an exception and stop execution. You can modify the error handling in the script to suit your needs.