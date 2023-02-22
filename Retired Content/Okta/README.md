# sumo-okta-lambda

This document describes how to configure the AWS Lambda based collection between Sumo Logic and Okta.

**Prerequisites:**

* Create an Okta “Admin - Read Only” token as described [here](https://developer.okta.com/docs/api/getting_started/getting_a_token)
* Configure a Hosted Collector and record it’s URL as described [here](https://help.sumologic.com/Send-Data/Hosted-Collectors/Configure-a-Hosted-Collector)

NOTE: Significant portions of this guide are taken from the AWS Samples, [here](https://github.com/aws-samples/aws-serverless-workshops/tree/master/WebApplication/3_ServerlessBackend) on GitHub.


<!--## Building the Lambda Function
The code here is the basic lambda function, it requres some supporting libraries to be bundled and the documentation assumes you have built the zip file.

There are two steps for preparing the function for upload to AWS. Firstly clone this project, then:

1. Build the lib folder (on Linux/Mac), in the root of the project:

`pip3 install -t lib/ --upgrade requests requests_toolbelt`

NOTE: The `requests_toolbelt` is needed specifically for AWS Lambda, see here.


For packaging the zip, from this directory:

`zip -r okta-logs-to-sumo.zip . -x "*.git*" -x "*.DS_Store*"`-->

## NOTE: Building the Lambda Function
Previous versions of this collector required the lambda function to be built into a zip containing additional libraries. With AWS Lambda now supporting a usable version of pythons `requests` module this is no longer needed and the function can be pasted directly into the editor.

## 1. Create an Amazon DynamoDB Table
We will use the Amazon DynamoDB console to create a new DynamoDB table. Call your table `sumo-to-okta` and give it a partition key called `okta_org_url` with type `String`. The table name and partition key are case sensitive. Make sure you use the exact IDs provided. Use the defaults for all other settings.

After you've created the table, note the ARN for use in the next step.

Step-by-step instructions:

1. From the AWS Management Console, choose **Services** then select **DynamoDB** under Databases.
1. Choose **Create table**.
1. Enter `sumo-to-okta` for the Table name. This field is case sensitive.
1. Enter `okta_org_url` for the Partition key and select `String` for the key type. This field is case sensitive.
1. Check the `Use default settings` box and choose **Create**.
1. Scroll to the bottom of the Overview section of your new table and note the ARN. You will use this in the next section.


## 2. Create an IAM Role for Your Lambda function
Next we use the IAM console to create a new role. Name it `OktaToSumoLambda` and select AWS Lambda for the role type. You'll need to attach policies that grant your function permissions to write to Amazon CloudWatch Logs and put items to your DynamoDB table.

Attach the managed policy called `AWSLambdaBasicExecutionRole` to this role to grant the necessary CloudWatch Logs permissions. Also, create a custom inline policy for your role that allows the `ddb:PutItem` action for the table you created in the previous section.

Step-by-step instructions:

1. From the AWS Management Console, click on **Services** and then select **IAM** in the Security, Identity & Compliance section.
1. Select **Roles** in the left navigation bar and then choose **Create role**.
1. Select **Lambda** for the role type from the AWS service group, then click **Next: Permissions**
1. Begin typing `AWSLambdaBasicExecutionRole` in the Filter text box and check the box next to that role.
1. Click **Next: Review**.
1. Enter `OktaToSumoLambda` for the Role name.
1. Choose **Create role**.
1. Type `OktaToSumoLambda` into the filter box on the Roles page and choose the role you just created.
1. On the Permissions tab, choose the **Add inline policy** link in the lower right corner to create a new inline policy. 
1. Select **Choose a service**.
1. Begin typing `DynamoDB` into the search box labeled Find a service and select **DynamoDB** when it appears.
1. Choose **Select actions**.
1. Begin typing `PutItem` into the search box labeled Filter actions and check the box next to **PutItem** when it appears.
1. Repeat step 13 for **GetItem** 
1. Select the **Resources** section.
1. With the Specific option selected, choose the **Add ARN** link in the table section.
1. Paste the ARN of the table you created in the previous section in the **Specify ARN for table** field, and choose **Add**.
1. Choose **Review Policy**.
1. Enter `DynamoDBReadWriteAccess` for the policy name and choose **Create policy**.


## 3. Create a Lambda Function for Sending Logs

Use the AWS Lambda console to create a new Lambda function called `OktaToSumo` that will run as a scheduled task to send the logs.

Make sure to configure your function to use the `OktaToSumoLambda` IAM role you created in the previous section.

Step-by-step instructions:

1. Choose on **Services** then select **Lambda** in the Compute section.
1. Click **Create function**.
1. Keep the default “Author from scratch” card selected.
1. Enter `OktaToSumoLambda` in the Name field.
1. Select **Python 3.7** for the Runtime.
1. Ensure **Choose an existing role** is selected from the Role dropdown.
1. Select **OktaToSumoLambda** from the Existing Role dropdown.
1. Click on **Create function**.

## 4. Setup the Trigger

1. Under **Add Triggers** select **CloudWatch Events**
1. Select the new trigger and under **Configure Triggers** select **Create a new rule**
1. Enter `every_5_minutes` as the rule name
1. Enter `Every 5 Minutes` as the rule description
1. Choose **Schedule expression**
1. For the rate enter `rate(5 minutes)`
1. **Enable Trigger**
1. Click **Add**

## 1. Copy the Code

1. Select the lambda function
1. In the code editor copy the contents of `okta-logs-to-sumo.py` from the repo into the editor
2. **Click Save**

### Setup the Environment Variables

1. Under “Environment Variables” add:

	| Variable Name | Example Value | Description |
	|---|---|---|
	| `SLEU_DDB_TABLE` | `sumo-to-okta` | The DynamoDB table name |
	| `SLEU_SUMO_COLLECTOR ` | `https://endpoint1.collection.us2.sumologic.com/receiver/v1/http/<REDACTED> ` | URL for Sumo Logic Hosted collector |
	| `SLEU_OKTA_ORG_URL ` | `https://myorg.okta.com` | The URL of your Okta instance |
	| `SLEU_OKTA_API_KEY ` | `00XXXXX_wjkbJksue789s7s99d-0QrGh3jj12rAQ` | API key generated for Okta Access |

2. Under “Basic Settings” configure the timeout for the function to two (2) minutes
For the handler set “okta-logs-to-sumo-lambda.lambda_handler”
Save the function

3. **Click Save**

NOTE: Data will be transferred once the first scheduled execution of the function takes place, or you can run a `Test` of the function with any/default test event payload.

