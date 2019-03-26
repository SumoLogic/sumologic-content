## Sumologic Python Client
Sumologic Python client. API documentation is available [here](https://help.sumologic.com/APIs#APIs).

## Requirements
- Python 3.5+
- [Requests](http://docs.python-requests.org/en/master/) library

## Getting Started
You will need a pair of access ID/key to use the client and API endpoint. Please refer to [API documentation](https://api.sumologic.com/docs/#section/API-Endpoints) to find endpoint corresponding to your geographic location.

## Example Usage
Export and sync content to a different location in the same org.

```python
from sumologic import client
from sumologic.api import content

api_client = client.ApiClient('ACCESS ID', 'ACCESS KEY', 'ENDPOINT')

content_api = content.ContentManagementApi(api_client)
item_to_export = content_api.find_id_by_path('/personal/mySavedSearch')
exported_content = content_api.export(item_to_export)

sync_to_folder = content_api.find_id_by_path('/global/allSavedSearches')
content_api.sync(sync_to_folder, exported_content)
```
