# Notification based S3 Setup Automator Script

### NOTE: This script is *community supported* and no guarantees are made by Sumo Logic.

### DESCRIPTION
This script is intended to perform automated configuration of SNS-based object discovery on existing S3 sources which previously used our legacy polling-based approach.
SNS is an AWS service through which Sumo Logic gets notified about any objects that are added to your S3 bucket rather than us polling the bucket to fetch new objects. 
The polling mechanism can be slow if the bucket is very large. SNS-based object discovery is the way to go in such cases. 

## Inputs required by this script
* Your Sumo Logic API endpoint. https://help.sumologic.com/APIs/General-API-Information/Sumo-Logic-Endpoints-and-Firewall-Security can help in making the selection.
* Your Sumo Logic accessId.
* Your Sumo Logic accessKey.
https://help.sumologic.com/Manage/Security/Access-Keys can help with the second and third step.
* AWS CLI should be configured with your AWS accessId and accessKey and the correct region. (The region should match where your buckets are located in)

# Steps performed by this script
1. Gets a list of all the collectors.
2. Gets a list of all the sources in every collector.
3. Extract the list of polling sources on which SNS-based object discovery can be set up.
4. Create a map between bucket name and endpoint and return it for further processing. So if there are multiple sources collecting from the same bucket 
then the map can look like: Map("bucket1" -> ["endpoint1", "endpoint2"], "bucket2" -> ["endpoint3"]).
5. Using the map of bucket name to endpoint generated above, it creates a topic per bucket. (So a topic for every key in that map)
6. Configure event notification on the bucket to send the object creation notification to the corresponding topic created in step 5.
7. Creates a subscription per endpoint for the corresponding topic to allow sending the notifications to Sumo Logic.


# Steps to run the automation script
* Run **sudo apt-get install python3-pip** to install pip3
* Run **sudo pip3 install -r requirements.txt** to install the requirements
* Run **aws configure** to configure aws cli
* Run **chmod +x script.py** to give execution permission to the script
* Run the script using **python3 script.py**