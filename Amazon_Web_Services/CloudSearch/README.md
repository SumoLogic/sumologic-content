# Amazon CloudSearch

![Screenshot-Amazon-CloudSearch-ULM](Screenshot-Amazon-CloudSearch-ULM.png)

[Amazon CloudSearch](https://aws.amazon.com/cloudsearch/) is an AWS product that allows for rich search capabilities to your website or application. 

This Sumo Logic app is an overview dashboard that unifies AWS CloudTrail logs and AWS CloudWatch Metrics. It gives insights into indexed objects, search metrics, and resources that have been modified.

## Log Collection

For the log portion of the app, you will need to ingest CloudTrail logs. Configure an [AWS CloudTrail Source](https://help.sumologic.com/Send-Data/Sources/02Sources-for-Hosted-Collectors/Amazon_Web_Services/AWS_CloudTrail_Source) to ingest the logs into Sumo Logic.

## Metrics Collection

For the metrics portion of the app, you will need to ingest [CloudWatch Metrics](https://help.sumologic.com/Metrics/Metrics-Sources/02Amazon-CloudWatch-Source-for-Metrics) with at least the *AWS/CloudSearch* namespace.

## Setup and Installation

Using the Amazon-CloudSearch-ULM.json, perform a find-and-replace for `_sourceCategory=*cloudtrail*` with your appropriate scope for CloudTrail logs, and perform a find-and-replace for `_sourceCategory=*cloudwatch/metrics*` with the appropriate scope for your CloudWatch Metrics.

Import the modified JSON into your Sumo Logic library.
