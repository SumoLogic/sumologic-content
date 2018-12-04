# Sumo Logic Alerts to SNS

### NOTE: This CloudFormation template is community supported and no guarantees are made by Sumo Logic!

This is a CloudFormation template that creates different resources to allow for Sumo Logic to send alerts to SNS.

Since SNS can be used to deliver to a variety of services and endpoints, this extends Sumo's notification functionality. For example, it can send an alert to multiple emails and phone numbers by creating more subscriptions for the SNS topic. 

## AWS Resources

This CFN template creates the following AWS resources:

* Lambda function - SumoLambdaToSNS: This function takes the message from Sumo and pushes it to SNS.
* IAM Role - LambdaExecutionRole: This role allows Lambda to run and work with the appropriate resources.
* API Gateway RestApi, Method, and Deployment: This is the API gateway that generates a RESTful URL protected by an IAM.
* IAM User - SumoLambdaUser: This user is created with the appropriate IAM permissions to execute the API Gateway URL.
* SNS Topic - SumoAlert: The topic is what receives the notifications. It does not deliver them unless there are subscriptions assigned to the topic.
* SNS Subscription(s):  This template creates 2 optional subscriptions: email and phone. You can manually subscribe other endpoints as well if needed.

## Deployment and Setup

### Deploy to AWS

1. Navigate to the CloudFormation console in AWS.
2. Click "Create Stack".
3. Under "Choose a template", select "Upload a template to Amazon S3" and select the .yaml file. 
4. Click "Next".
5. Enter a name for the stack such as "SumoToSNS".
6. Optionally enter the email address and/or phone number for alerts. If you do not setup these endpoints during setup, you must manually create an SNS subscription later on. Be sure to enter the country code without a plus (+) for phone numbers. US country code is 1.
7. Click "Next".
8. Click "Next".
9. Acknowledge the disclaimer that the template is creating IAM resources, and click "Create".

Once initiated, it will take approximately 1-2 minutes to complete the creation of the resources.

### Optional: Verify SNS Email Subscription

If you entered an email, you will get a verification email once it is subscribed. Open the email and follow the verification link.

### Obtain AWS Parameters

1. Navigate to the API Gateway console. 
2. Select the newly created API, "SumoAPIGatewayRestAPI".
3. Select the "Stages" tab.
4. Select "Prod".
5. Copy the "Invoke URL" located at the top (e.g., https://abc123.execute-api.us-west-2.amazonaws.com/Prod).
6. Navigate to IAM console.
7. Select "Users".
8. Select the newly created user, "SumoLambdaUser".
9. Select "Security Credentials" tab.
10. Click "Create Access Key". 
11. Securely take note of the access key and ID.


### Create a Sumo Logic Connection

1. Navigate to Connections in Sumo Logic. This is located under Manage Data -> Settings.
2. Click the plus sign (+) to create a new connection.
3. Select "AWS Lambda".
4. Enter a name to describe this connection.
5. Enter the URL generated from the API Gateway deployment resource.
6. Enter the Access Key ID and Secret Access Key obtained from SumoLambdaUser.
7. Select the region you deployed the CloudFormation template to. 
8. Enter *execute-api* as the Service Name.
9. Enter the payload from payload.json. You can customize the Subject, Email_Message, and SMS_Message values for your alerts.
10. Click "Test Connection". You should receive alerts to the all of the endpoints that you have subscribed to the SNS Topic.