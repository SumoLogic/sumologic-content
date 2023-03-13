# MISP to Sumo Logic Threat Intel Source

This Python script allows you to send data from a MISP instance to a Sumo Logic Threat Intel Source.

## Prerequisites
1. You need to have a Sumo Logic account.
2. You need to have a Sumo Logic Threat Intel Source. Please update the "{TI-ID}" value with the TI ID you would like to ingest the indicators into. (Please see [here for some standalone scripts to do different tasks with the Sumo API](/sumo/standalone_cse_pyscripts). )
3. You need to obtain your MISP API key and set it as an environment variable named "misp_api_key".
4. You need to obtain your Sumo Logic Access ID and Access Key and set them as environment variables named "cip_access_id" and "cip_access_key", respectively.

## Usage
1. Download the script to your local machine.
2. Run the script with python scriptname.py.
3. Enter the MISP URL and CIP deployment name when prompted.
4. The script will send the data from the MISP instance to the Sumo Logic Threat Intel Source.

## Notes
- This script uses the MISP API to get the data from the MISP instance. You can customize the request data in the script to get different data from the MISP instance.
- The script paginates through the results from the MISP API request and sends them to the Sumo Logic Threat Intel Source.
- The remap_attributes() function remaps certain attributes to a specific payload that is required by the Sumo Logic Threat Intel Source API.
- If the script encounters an error while sending data to the Sumo Logic Threat Intel Source, it will print an error message and continue execution. You can modify the error handling in the script to suit your needs.