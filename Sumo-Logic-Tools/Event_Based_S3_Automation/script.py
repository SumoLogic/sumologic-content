import requests
import boto3
import json
import getpass
from requests.auth import HTTPBasicAuth
from collections import defaultdict

'''
Helps in taking in the inputs required for the script to function properly.
There are 3 things the user has to enter.
1. Select the API endpoint. https://help.sumologic.com/APIs/General-API-Information/Sumo-Logic-Endpoints-and-Firewall-Security can help in making the selection.
2. Enter the Sumo accessId.
3. Enter the Sumo accessKey.
https://help.sumologic.com/Manage/Security/Access-Keys can help with the second and third step.
'''
class InitialSetupHelper:

	apiEndpointOrderedList = ['https://api.us2.sumologic.com/api', 'https://api.sumologic.com/api', 'https://api.au.sumologic.com/api', 'https://api.eu.sumologic.com/api', 'https://api.de.sumologic.com/api']

	def takeRequiredInputs(self):
		print("\n WELCOME! THIS SCRIPT WILL AUTOMATE THE EVENT BASED S3 SETUP FOR YOU. IT WILL ADD THE NOTIFICATION BASED MECHANISM ON ALL OF YOUR POLLING SOURCES! \n")
		print("\nBUT FIRST YOU NEED TO PROVIDE SOME INPUTS \n")
		print("\nMAKE SURE THAT YOU HAVE RUN AWS CONFIG AND CONFIGURED THE AWS CLI PROPERLY WITH THE CORRECT CREDENTIALS AND REGION \n")
		print("\nWHICH SUMO API ENDPOINT DO YOU GUYS USE? [1-5]")
		print("1. ", self.apiEndpointOrderedList[0], "\n2. ", self.apiEndpointOrderedList[1], "\n3. ", self.apiEndpointOrderedList[2], "\n4. ", self.apiEndpointOrderedList[3], "\n5. ", self.apiEndpointOrderedList[4])

		while True:
			deployment = int(input("Enter your choice: "))
			if (deployment < 1 or deployment > 5):
				print("Please select a value between 1 to 5")
				continue
			else:
				break

		base_url = str(self.apiEndpointOrderedList[deployment - 1])

		print("\nEnter you SUMO ACCESS ID AND ACCESS KEY")

		access_id = input("ACCESS ID: ")
		access_key = getpass.getpass("ACCESS KEY: ")

		return (base_url, access_id, access_key)


'''
Helps in getting the list of sources on which event based S3 has to be set up.
It does the following tasks:
1. Get a list of all the collectors.
2. Get a list of all the sources in every collector.
3. Extract the list of polling sources on which event-based-S3 can be set up.
4. Create a map between bucket name and endpoint and return it for further processing. So if there are multiple sources collecting from the same bucket 
then the map can look like: Map("bucket1" -> ["endpoint1", "endpoint2"], "bucket2" -> ["endpoint3"]).
'''
class SumoSetupHelper():

	collector_url = '/v1/collectors/'
	pollingTypeSources = ['AwsS3Bucket', 'AwsCloudTrailBucket', 'AwsCloudFrontBucket', 'AwsConfigBucket', 'AwsElbBucket', 'AwsS3AuditBucket']
	mapOfBucketNameToEndpoint = defaultdict(list)

	def __init__(self, base_url, access_id, access_key):
		self.base_url = base_url
		self.access_id = access_id
		self.access_key = access_key

	def calculateMappingOfBucketNameToEndpoint(self):
		listOfCollectors = self.getListOfCollectors()

		listOfSourcesLink = self.getSourcesLinks(listOfCollectors)

		listOfPollingSources = self.getPollingSources(listOfSourcesLink)

		self.populateMapOfBucketNameToEndpoint(listOfPollingSources)

		return self.mapOfBucketNameToEndpoint

	def getListOfCollectors(self):
		return self.makeGetRequest(self.collector_url).json()

	def makeGetRequest(self, url):
		return requests.get(url = self.base_url + str(url), auth = HTTPBasicAuth(self.access_id, self.access_key))

	def getSourcesLinks(self, listOfCollectors):
		listOfSourcesLink = list()
		try:
			for collector in listOfCollectors['collectors']:
				links = collector['links']
				listOfSourcesLink.extend(self.extractSourcesLink(collector['links']))
		except KeyError as e:
			try:
				collector = listOfCollectors['collector']
				links = collector['links']
				listOfSourcesLink.extend(self.extractSourcesLink(collector['links']))
			except KeyError as e:
				print("The API did not return any collectors!")
		return listOfSourcesLink

	def extractSourcesLink(self, links):
		listOfSourcesLink = list()
		for link in links:
			if (link['rel'] == 'sources'):
				listOfSourcesLink.append(link['href'])

		return listOfSourcesLink

	def getPollingSources(self, listOfSourcesLink):
		listOfPollingSources = list()
		for sourceLink in listOfSourcesLink:
			allSources = self.makeGetRequest(sourceLink).json()
			for source in allSources['sources']:
				if (self.isPollingSource(source) == True):
					listOfPollingSources.append(source)

		return listOfPollingSources

	def isPollingSource(self, source):
		# get returns None if contentType is not available. The source cannot be polling if it does not have a content type
		contentType = source.get('contentType')
		return (contentType in self.pollingTypeSources)

	def populateMapOfBucketNameToEndpoint(self, listOfPollingSources):
		for source in listOfPollingSources:
			bucketName = self.getBucketName(source)
			endpoint = self.getEndpoint(source)
			if (bucketName is not None and endpoint is not None):
				self.mapOfBucketNameToEndpoint[bucketName].append(endpoint)

	def getBucketName(self, source):
		try:
			thirdPartyRef = source['thirdPartyRef']
			resources = thirdPartyRef['resources']
			path = resources[0]['path']
			return path['bucketName']
		except:
			return None

	def getEndpoint(self, source):
		return source.get('url')


'''
Helps in setting up event based S3 using the appropriate AWS APIs.
It does the following tasks:
1. Using the map of bucket name to endpoint generated above, it creates a topic per bucket. (So a topic for every key in that map)
2. Configure event notification on the bucket to send the object creation notification to the corresponding topic created in step 1.
3. Creates a subscription per endpoint for the corresponding topic to allow sending the notifications to Sumo Logic.
'''
class AwsSetupHelper:

	mapOfBucketNameToTopicArn = {}

	# AWS Clients
	snsClient = boto3.client('sns')
	s3Client = boto3.client('s3')
	stsClient = boto3.client('sts')

	def __init__(self, mapOfBucketNameToEndpoint):
		self.mapOfBucketNameToEndpoint = mapOfBucketNameToEndpoint

	def setupEventNotifications(self):
		self.createTopicPerBucket()
		self.createSubscriptionsPerTopic()

	def createTopicPerBucket(self):
		for bucketName, endpointList in self.mapOfBucketNameToEndpoint.items():
			topicName = "Sumo-" + str(bucketName) + "-Topic"
			response = self.snsClient.create_topic(Name = topicName)
			topicArn = response.get('TopicArn')
			self.setTopicPolicy(bucketName, topicArn)
			self.putBucketNotification(bucketName, topicArn)
			self.mapOfBucketNameToTopicArn[bucketName] = topicArn

	def setTopicPolicy(self, bucketName, topicArn):
		self.snsClient.set_topic_attributes(
			TopicArn = topicArn,
			AttributeName = 'Policy',
			AttributeValue = self.getTopicPolicy(bucketName, topicArn)
		)

	def getTopicPolicy(self, bucketName, topicArn):
		accountId = self.stsClient.get_caller_identity()["Account"]
		policy = {
			"Version": "2008-10-17",
			"Id": "SumoTopicPolicy",
			"Statement": [
				{
					"Effect": "Allow",
					"Principal": {
						"AWS": "*"
					},
					"Action": "sns:Publish",
					"Resource": str(topicArn),
					"Condition": {
						"StringEquals": {
							"aws:SourceAccount": str(accountId)
						},
						"ArnLike": {
							"aws:SourceArn": "arn:aws:s3:*:*:" + str(bucketName)
						}
					}
				}
			]
		}

		return json.dumps(policy)

	def putBucketNotification(self, bucketName, topicArn):
		self.s3Client.put_bucket_notification_configuration(
			Bucket = bucketName,
			NotificationConfiguration = {
				'TopicConfigurations': [
					{
						'Id': "Sumo" + str(bucketName) + "Topic",
						'TopicArn': topicArn,
						'Events': ['s3:ObjectCreated:*']
					}
				]
			}
		)

	def createSubscriptionsPerTopic(self):
		for bucketName, listOfEndpoint in self.mapOfBucketNameToEndpoint.items():
			for endpoint in listOfEndpoint:
				self.snsClient.subscribe(
					TopicArn = self.mapOfBucketNameToTopicArn.get(bucketName),
					Protocol = "https",
					Endpoint = endpoint,
					Attributes = {
						'DeliveryPolicy': self.getDeliveryPolicy()
					}
				)

	def getDeliveryPolicy(self):
		retryPolicy = {
			"healthyRetryPolicy": {
				"minDelayTarget": 10,
				"maxDelayTarget": 300,
				"numRetries": 40,
				"numMaxDelayRetries": 5,
				"numNoDelayRetries": 0,
				"numMinDelayRetries": 3,
				"backoffFunction": "exponential"
			}
		}

		return json.dumps(retryPolicy)

def main():

	inputHelper = InitialSetupHelper()
	(base_url, access_id, access_key) = inputHelper.takeRequiredInputs()

	print("..........DONE READING INPUT. NOW STARTING THE AUTOMATION...........")

	sumoHelper = SumoSetupHelper(base_url, access_id, access_key)
	mapOfBucketNameToEndpoint = sumoHelper.calculateMappingOfBucketNameToEndpoint()

	print("..........DONE FINDING THE LIST OF SOURCES TO APPLY EVENT BASED S3 ON..........")

	awsHelper = AwsSetupHelper(mapOfBucketNameToEndpoint)
	awsHelper.setupEventNotifications()

	print("..........DONE CONFIGURING THE TOPICS AND SUBSCRIPTIONS. YOU ARE ALL SET NOW!..........")

if __name__ == '__main__':
	main()
