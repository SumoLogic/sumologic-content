# Indago CloudSOAR Integration for Sumo Logic

Sumo Logic Custom CloudSOAR Integration for Indago, provided by the community. This integration allows you to post JSON payloads into an Indago collection via the Indago API.

## What's Included:
1. **Integration YAML File**: Contains the configuration and test connection script for Indago API.
2. **Action YAML File(s)**:
    - **Post Collection (Custom Action)**: Sends JSON data into an Indago collection.

## Prerequisites:
Before using this integration, ensure you have:
- API access to Indago.
- API key for authentication.
- A valid collection ID in Indago.

## How to Use:
### 1. Download the Integration and Action YAML Files:
   - Download `Indago.integration.yaml`
   - Download `Post_collection.action.yaml`

### 2. Create a New CloudSOAR Integration:
   1. Log into **CloudSOAR**.
   2. Navigate to **Settings** (Cogwheel) > **Automation** > **Integrations**.
   3. Click the **Plus (+)** icon.
   4. Select **Upload Integration YAML** and choose `Indago.integration.yaml`.

### 3. Add Actions to the Integration:
   1. After adding the integration, select the **Upload Action YAML** icon.
   2. Upload `Post_collection.action.yaml`.

### 4. Configure the Integration:
   Fill in the API details, including:
   - **API URL**: `https://staging.indagoapp.com/`
   - **API Key** (stored securely)
   - **Collection ID** (where data will be sent)

### 5. Test the Integration:
   - Click **Test** to verify the connection.
   - Ensure the API key and collection ID are valid.

### 6. Run the Action:
   1. Navigate to **Automation > Actions**.
   2. Select **Indago Post Collection**.
   3. Enter the required parameters:
      - **Title**: A descriptive title for the collection entry.
      - **Content**: The JSON payload to be sent.

### 7. Validate the Output:
   - If successful, the response will include:
     - `collectionItemId`: The ID of the stored collection item.
     - `ok`: Boolean indicating success or failure.
     - `errors`: List of errors (if any).

## Additional Information:
- For more details on uploading custom integrations and actions, refer to [Working with Integrations](https://help.sumologic.com/docs/cloud-soar/cloud-soar-integration-framework/#working-with-integrations).
- To contribute or report issues, please use the Sumo Logic Community platform.