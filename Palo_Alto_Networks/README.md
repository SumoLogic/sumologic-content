<<<<<<< HEAD:Palo_Alto_Networks/README.md
Contains all Palo Alto Networks specific apps for which Sumo Logic has content for.
=======
IMPORTANT: DEPRECATED. Official Kubernetes Application is now available in the Sumo Logic App Catalog.
//////////////////////////////////////
//////////////////////////////////////
Contains all Kubernetes technology and product lines for which Sumo Logic has content for.
>>>>>>> 1597c048cb929a8a7bfdfca02ca4d4514b1fcae4:Kubernetes/README.md

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