# Kandji API Data Streamer

## This script fetches data from the Kandji API and sends it to a specified SIEM HTTPS endpoint. The data fetched includes threat details, device information, lost device mode status, device commands, installed apps on devices, and detailed device inventory.

### Prerequisites
- Python 3
- requests library: Install using ```pip install requests```

### Setup
### Environment Variables

Before running the script, you need to set up the following environment variables:

1. SUBDOMAIN: Your Kandji API subdomain.
1. SIEM_HTTPS_ENDPOINT: The HTTPS endpoint where the fetched data will be sent.
1. TOKEN: Your Kandji API authorization token.

On a Unix-based system (like Linux or MacOS), you can set the environment variables using:

```bash
export SUBDOMAIN=your_subdomain
export SIEM_HTTPS_ENDPOINT=https://https-endpoint
export TOKEN=your_token_value
```

On Windows, you can set environment variables using the set command in the Command Prompt:

```arduino
set SUBDOMAIN=your_subdomain
set SIEM_HTTPS_ENDPOINT=https://your-siem-endpoint-url.com/ingest
set TOKEN=your_token_value
```

### Running the Script

To run the script, navigate to its directory and execute:

```bash
python3 main.py
```
_Replace main.py with the actual name of the script if you've renamed it._

### Features

The script performs the following tasks:

1. Fetches all devices with pagination.
1. Retrieves threat details from the Kandji API.
1. For each device:
    - Fetches its lost device mode status.
    - Retrieves device commands.
    - Gets installed apps on the device.
    - Obtains detailed device inventory.

All the retrieved data is sent to the SIEM HTTPS endpoint specified, with appropriate source categories in the header.

### Error Handling

The script has built-in error handling. If a request to the Kandji API fails, the script will retry once before moving on to the next task. If the response from an API call is not valid JSON, the script will log an error message and retry the request.