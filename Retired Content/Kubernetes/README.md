IMPORTANT: DEPRECATED. Official Kubernetes Application is now available in the Sumo Logic App Catalog.
//////////////////////////////////////
//////////////////////////////////////
Contains all Kubernetes technology and product lines for which Sumo Logic has content for.

See [Sumo Logic Documentation](https://help.sumologic.com/) for instructions on how to collect logs and metrics for use with content.

Guidelines PLEASE READ:

To contribute to subfolders or create new subfolders here, please follow the standards below:

1. All application, dashboard and search content in .json format. Please use descriptive naming such as:
   a. Company_TechnologyLine_ContentFunction. E.g. AWS_Kinesis_Errors.json or Sentinel_Vanguard_All.json

2. Relevant screenshot(s) in .png or equivalent format. Naming similar or equivalent to .json content it represents.
   a. More than 1 screenshot? Please create a "Screenshots" folder.

3. Create/update a README.md file (like this one) within the folder to track:
   a. Technology and product lines, authors, versions, etc.
   b. Link(s) to relevant 3rd party documentation to specify what types of data need to be collected for content to work.

2017/12/04 - Updated:

  Kubernetes Logs - Collect:
    - Kube System
    - Kube Controller Manager
    - Kube ApiServer
    - Kube Scheduler
  For more information, see Kubernetes documentation here:
  [Google K8s Logs](https://kubernetes.io/docs/concepts/cluster-administration/logging/)
