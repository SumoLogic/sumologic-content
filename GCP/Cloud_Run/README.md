# Sumo Logic application for Google Cloud Run
 
Contains Dashboards for Google Cloud Run

To use the content:
1. Deploy the Sumo Logic Helm chart for Kubernetes to collect logs and metrics and; send them to Sumo Logic
2. Create Field pod_labels_serving.knative.dev/service by naviagting to Manage Data > Settings > Fields. This ensures that your logs are tagged with relevant metadata, which is required by the app dashboard.

This dashboard provides inforamtion sbout Applications running on Google Cloud Run
![Google - Cloud Run](Screenshots/GCP-CR.png)




See [Sumo Logic Documentation](https://help.sumologic.com/) for instructions on how to collect logs and metrics for use with content.

Guidelines PLEASE READ:

To contribute to subfolders or create new subfolders here, please follow the standards below:

1. All application, dashboard and search content in .json format. Please use descriptive naming such as:
   a. Company_TechnologyLine_ContentFunction. E.g. AWS_Kinesis_Errors.json or Sentinel_Vanguard_All.json

2. Relevant screenshot(s) in .png or equivalent format. Naming similar or equivalent to .json content it represents.

3. Create/update a README.md file (like this one) within the folder to track:
   a. Technology and product lines, authors, versions, etc.
   b. Link(s) to relevant 3rd party documentation to specify what types of data need to be collected for content to work.

