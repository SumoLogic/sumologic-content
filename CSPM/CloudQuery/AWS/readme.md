# Introduction this is a walk through of Cloudquery w/AWS + Sumo for CSPM

Hello, this repository of code was to establish a "POC" code/solution to CSPM for Sumo Logic to offer to our customers. This has a few dependecies that must be considered/acknowledged. 

1. [Cloudquery](https://www.cloudquery.io/docs) deployed into a cloud env (their preferred is AWS), they do have a lovely [TF](https://github.com/cloudquery/terraform-aws-cloudquery) that can make this deployment very simple. I think when moving this to production we should look at it entirely being hosted in aws. For the sake of the POC, this was done mostly local to my mac with the exception of the database being hosted in AWS (RDS). This was a huge thank you to Chas Clawson who found cloudquery and provided it to the team to test! His research turned up this [link](https://www.cloudquery.io/blog/open-source-cspm#step-1-install-or-deploy-cloudquery): which was used to create this doc. 

2. Sumo currently does NOT have a methodology to pull logs/data from a database very easily. However, we have DO have OTEL support at Sumo for a [postgresql reciever](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.62.0/receiver/postgresqlreceiver) BUT it currently only supports metrics. I am not sure if they will add that functionality but may be something we can use at a later date. Maybe this changes with out deployment of OTEL in the future but for right now this POC code leverages the ability to export the results from the DB table to a csv and then ingested into the sumologic via an installed collector looking at the direcotry. 

    *Please note that the most likely sustainable 'go-live' route would be to leverage a hosted collector by posting the new file to the https endpoint on a re-occuring timeframe*

3. A configured [AWS cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html). If you need help setting up the aws cli, here is a quick [Getting started with the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)

# POC Code Walkthrough Steps

1. Setup Cloudquery locally on your mac or device. Setup instructions can be found [here](https://www.cloudquery.io/docs/quickstart)


2. Configure your input sources (i.e., what cloud provider your querying - see example below aws.yml). For more information or other examples of sources please see [here](https://www.cloudquery.io/docs/plugins/sources)

```yaml
kind: source
spec:
  # Source spec section
  name: aws
  path: cloudquery/aws
  version: "v4.14.0" # latest version of aws plugin
  tables: ["*"]
  destinations: ["postgresql"]
  spec: 
    # AWS Spec section described below
    regions: 
      - us-east-1
    accounts:
      - id: ""
        local_profile: ""
    aws_debug: false
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
cloudquery sync aws.yml postgressql.yml
```
Example: 

![alt text](/cloudquery_sumo_cspm/AWS/screenshots/cloudquery_execute.png)


## This section is how we correlate all the configuration and policy data together. The results of this highlight if the customer is compliant/non-compliant.


5. We will now be executing the OOTB plugins/scripts that cloudquery provides to track state change for the customers resources. 

*Note this can be done either locally (with connection to remote DB) or this can be done in the eks cluster that was deployed with the TF automation.*

```bash
git clone https://github.com/cloudquery/cloudquery.git
cd cloudquery/plugins/source/aws/policies_v1/cis_v1.5.0/
# change the DSN to your PostgreSQL instance populated by CloudQuery
psql postgres://postgres:pass@localhost:5432/postgres -f policy.sql
# ^ the line above will execute all of the policies for CIS Benchmarks 1.5
```
*If you would like to see all of the potentially policy options, please navigate [here](https://www.cloudquery.io/docs/core-concepts/policies)*

6. The results from the *policy.sql* you just ran are then stored in the database under a table called *aws_policy_results* to which we can query the results for either through a script or a database connection. Currently, Sumo does NOT have a way to pull from databases but if we did, then our integration would be very similar to [Grafana's](https://github.com/cloudquery/cq-provider-aws/tree/main/dashboards). 


7. Due to Sumo not having a database connector, we have to query the data via the command below and output the results to a csv file that can then be ingested into Sumo. 

```
psql postgres://$user:$PASSWORD@$RDS_HOSTNAME:5432/postgres -c "select * from aws_policy_results" --csv > cis_v1.5.csv
```

*I have attached an example of the raw CSV output [here](/AWS/results/example_cis_v1.5.csv)


8. Now get this data into Sumo!

*For this POC I used an installed collector but this could be easily done with a hosted collector*

- Create your source to grab the csv: 

Example:

![alt text](/cloudquery_sumo_cspm/AWS/screenshots/local_file_source.png)

- We can now see our data in sumo: 

![alt text](/cloudquery_sumo_cspm/AWS/screenshots/data_in_sumo.png)


- Query / Begin to parse the data in Sumo:

![alt text](/cloudquery_sumo_cspm/AWS/screenshots/query_parse_data.png)

- An example (quick albiet) dashboard for CISv1.5: 

![alt text](/cloudquery_sumo_cspm/AWS/screenshots/example_CIS_Framework_Dashboard.png)


*If we wanted to do additional things like inventory with the data, this can be easy as well leveraging the work grafana already did [here](https://github.com/cloudquery/cq-provider-aws/blob/main/dashboards/grafana/aws_asset_inventory.json) by leveraging their DB queries since they used the default installation.*


## Thank you for taking the time to review this POC code and I hope that we can get this into Sumo quickly!

