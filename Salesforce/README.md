# SFDC Logs to Sumo

**Prerequisites**
* [Create a Connected](https://help.salesforce.com/articleView?id=connected_app_create.htm&type=5) App in your SFDC app for this lambda function.
* Once the Connected App is created, follow [this OAuth flow](https://help.salesforce.com/articleView?id=remoteaccess_oauth_web_server_flow.htm&type=5) to get an `access_token` and `refresh_token`. 

**Sumo Setup**

Create a new hosted collector and create an HTTP source for the collector. When creating the source, under “Advanced Options for Logs”, “Timestamp Format”, select “Specify a format” and enter `yyyyMMddHHmmss.SSS` for the format; leave the “Timestamp locator” empty.

**AWS Systems Manager**

In the AWS console go to AWS Systems Manager then select the Parameter Store. Create the following parameters.

1. Sumo Logic HTTP data source
  * Name: `sumo_collector_url`
  * Tier: Standard
  * Type: SecureString
  * KMS Key Source: My current account
  * KMS Key ID: select the correct one
  * Value: URL of the Sumo Logic HTTP data source

2. SFDC Latest Timestamp
  * Name: `sfdc_latest_timestamp`
  * Tier: Standard
  * Type: String
  * Value: Current time in `yyyy-MM-dd'T'HH:mm:ss'Z'` format e.g. `2020-01-08T08:36:53Z`

3. SFDC Access Token
  * Name: `sfdc_access_token`
  * Tier: Standard
  * Type: SecureString
  * KMS Key Source: My current account
  * KMS Key ID: select the correct one
  * Value: HTTP Bearer token for accessing the SFDC API for your account

4. SFDC Refresh Token
  * Name: `sfdc_refresh_token`
  * Tier: Standard
  * Type: SecureString
  * KMS Key Source: My current account
  * KMS Key ID: select the correct one
  * Value: HTTP Refresh token for your SFDC API


5. SFDC-Sumo Lambda Client ID
* Name: `sfdc_sumo_client_id`
  * Tier: Standard
  * Type: SecureString
  * KMS Key Source: My current account
  * KMS Key ID: select the correct one
  Value: Client ID for the app that you have registered in your SFDC account.

**AWS Lambda**

* Go to AWS Lambda “Layers” and create a new layer. Select “upload a .zip file” and upload the `lambda_layer.zip` file in this directory. Select Python 3.8 for the runtime. 
* Create a new Lambda function with name “sumo_sfdc_upload” with runtime Python 3.8. Create a new execution role with basic lambda permissions. Copy-paste the code here for the function code. Add the layer to the function that was just created.
* Create the following environment variables.
  * `accessToken`
    * Value: `sfdc_access_token`
  * `clientId`
    * Value: `sfdc_sumo_client_id`
  * `latestTimestamp`
    * Value: `sfdc_latest_timestamp`
  * `sumoCollectorUrl`
    * Value: `sumo_collector_url`
  * `refreshToken`
    * Value: `sfdc_refresh_token`
    
Increase the timeout to 1 minute and save.

**AWS IAM**

In order to access the parameters in the AWS Systems Manager, specific rights needs to be granted to the AWS Lambda function role.

For this:
1. Open AWS IAM
2. Select Roles
3. Locate the role associated to the Lambda function created previously and click on it
4. Click on the associated policy
5. Click on edit policy (the policy should already grant access to CloudWatch logs)
6. Click on Add additional permissions
  * Service: Systems Manager
  * Actions: 
    * GetParameter
    * PutParameter
  * Resources: 
    * Add all 5 parameters created previously
7. Click on Preview Policy
8. Click on Save changes

**AWS Cloud Watch**
1. Create a scheduler for the Lambda function:
2. Select Events/Rules
3. Click on Create rule
4. Select Schedule
5. Select Fixed rate of 6 hours
6. Click on Add target
7. Select the Lambda function created previously
8. Click on Configure details
9. Enter a name (for example: `sfdc_to_sumo`)
10. Click on Create rule

