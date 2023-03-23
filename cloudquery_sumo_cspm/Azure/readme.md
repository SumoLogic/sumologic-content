# Introduction this is a walk through of Cloudquery w/Azure + Sumo for CSPM

Hello, this repository of code was to establish a "POC" code/solution to CSPM for Sumo Logic to offer to our customers. This has a few dependecies that must be considered/acknowledged. 

1. [Cloudquery](https://www.cloudquery.io/docs) deployed into a cloud env (their preferred is AWS). I think when moving this to production we should look at it entirely being hosted in AWS. For the sake of the POC, this was done mostly local to my mac with the exception of the database being hosted in AWS (RDS). This was a huge thank you to Chas Clawson who found cloudquery and provided it to the team to test! His research turned up this [link](https://www.cloudquery.io/blog/open-source-cspm#step-1-install-or-deploy-cloudquery): which was used to create this doc. 

*Please note that you can host your DB in AWS and just run the cloudquery to HIT azure and store data in to database* 

2. Sumo currently does NOT have a methodology to pull logs/data from a database very easily. However, we have DO have OTEL support at Sumo for a [postgresql reciever](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.62.0/receiver/postgresqlreceiver) BUT it currently only supports metrics. I am not sure if they will add that functionality but may be something we can use at a later data. Maybe this changes with out deployment of OTEL in the future but for right now this POC code leverages the ability to export the results from the DB table to a csv and then ingested into the sumologic via an installed collector looking at the direcotry. 

    *Please note that the most likely sustainable 'go-live' route would be to leverage a hosted collector by posting the new file to the https endpoint on a re-occuring timeframe*

3. A configured [Azure cli](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli). If you need help setting up the Azure cli, here is a quick [Getting started with the Azure CLI](https://learn.microsoft.com/en-us/cli/azure/get-started-with-azure-cli)


# POC Code Walkthrough Steps

1. Setup Cloudquery locally on your mac or device. Setup instructions can be found [here](https://www.cloudquery.io/docs/quickstart)


2. Configure your input sources (i.e., what cloud provider your querying - see example below azure.yml). For more information or other examples of sources please see [here](https://www.cloudquery.io/docs/plugins/sources)

```yaml
kind: source
spec:
  name: azure
  path: cloudquery/azure
  version: "v1.4.3" # latest version of azure plugin
  tables: ["*"]
  destinations: ["postgresql"]
```


3. Configure your output sources (i.e., where is the list of configuration data going to be stored). In this example, you can see my configuration file points to an RDS database in AWS. For more information or a list of other destinations please see [here](https://www.cloudquery.io/docs/plugins/destinations).

```yaml
kind: destination
spec:
  ## Required. name of the plugin.
  ## This is an alias so it should be unique if you have a number of postgresql destination plugins.
  name: "postgresql"
 
  ## Optional. Where to search for the plugin. Default: "github". Options: "github", "local", "grpc".
  # registry: "github"
 
  ## Path for the plugin.
  ## If registry is "github" path should be "repo/name"
  ## If registry is "local", path is path to binary. If "grpc" then it should be address of the plugin (usually useful in debug).
  path: "cloudquery/postgresql"
 
  ## Required. Must be a specific version starting with v, e.g. v1.2.3
  ## checkout latest versions here https://github.com/cloudquery/cloudquery/releases?q=plugins-destination-postgresql&expanded=true
  version: "v1.7.7" # latest version of postgresql plugin
 
  ## Optional. Default: "overwrite-delete-stale". Available: "overwrite-delete-stale", "overwrite", "append". 
  ##  Not all modes are supported by all plugins, so make sure to check the plugin documentation for more details.
  write_mode: "overwrite-delete-stale" # overwrite-delete-stale, overwrite, append
 
  spec:
    ## plugin-specific configuration for PostgreSQL.
    ## See all available options here: https://github.com/cloudquery/cloudquery/tree/main/plugins/destination/postgresql#postgresql-spec
 
    ## Required. Connection string to your PostgreSQL instance
    ## In production it is highly recommended to use environment variable expansion
    ## connection_string: ${PG_CONNECTION_STRING}
    connection_string: "postgres://$user:$PASSWORD@$RDS_HOSTNAME:5432/postgres?sslmode=disable"
```

4. Now that we have staged our source and destination files, we need to tell cloudquery to 'sync'. Run the command below, where you have cloudquery installed. 

```bash
cloudquery sync azure.yml postgressql.yml
```
Example: 

![alt text](/CSPM/CloudQuery/Azure/screenshots/cloudquery_execute.png)


## This section is how we correlate all the configuration and policy data together. The results of this highlight if the customer is compliant/non-compliant.


5. We will now be executing the OOTB plugins/scripts that cloudquery provides to track state change for the customers resources. 

    *Note this can be done either locally (with connection to remote DB) or this can be done in the eks cluster that was deployed with the TF automation.*

```bash
git clone https://github.com/cloudquery/cloudquery.git
cd cloudquery/plugins/source/azure/policies_v1/hipaa_hitrust_v9.2/
# change the DSN to your PostgreSQL instance populated by CloudQuery
psql postgres://postgres:pass@localhost:5432/postgres -f policy.sql
# ^ the line above will execute all of the policies for CIS Benchmarks 1.5
```
*If you would like to see all of the potentially policy options, please navigate [here](https://www.cloudquery.io/docs/core-concepts/policies)*

6. The results from the *policy.sql* you just ran are then stored in the database under a table called *azure_policy_results* to which we can query the results for either through a script or a database connection. Currently, Sumo does NOT have a way to pull from databases. 

7. Due to Sumo not having a database connector, we have to query the data via the command below and output the results to a csv file that can then be ingested into Sumo. 

```
psql postgres://$user:$PASSWORD@$RDS_HOSTNAME:5432/postgres -c "select * from azure_policy_results" --csv > hipaa_hitrust_v9.2.csv
```

*I have attached an example of the raw CSV output [here](/CSPM/CloudQuery/Azure/results/hipaa_hitrust_v9.2.csv)


8.  Now get this data into Sumo! 

*For this POC I used an installed collector but this could be easily done with a hosted collector*

- Create your source to grab the csv: 

Example:

![alt text](/CSPM/CloudQuery/Azure/screenshots/local_file_source.png)

- We can now see our data in sumo: 

![alt text](/CSPM/CloudQuery/Azure/screenshots/data_in_sumo.png)


- Query / Begin to parse the data in Sumo:

![alt text](/CSPM/CloudQuery/Azure/screenshots/query_parse_data.png)

- An example (quick albiet) dashboard for HIPAA Hi-Trust: 

![alt text](/CSPM/CloudQuery/Azure/screenshots/example_HIPAA_Hi-trust.png)


## Thank you for taking the time to review this POC code and I hope that we can get this into Sumo quickly!

