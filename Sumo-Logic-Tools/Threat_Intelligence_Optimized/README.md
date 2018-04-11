# Threat Intelligence Quick Analysis - Optimized

While the included Threat Intelligence Quick Analysis app is a great place to start for valuable threat intelligence, it still needs to be optimized to get the most value out of it.  This is an optimized version of the included app.

## Setup

### Setup Scheduled Views

Scheduled Views are key to making the Threat Intelligence optimized to rapidly query.  These scheduled views are created to search across *all* data ingested into Sumo Logic. They can be grouped in different ways including Source Category and Source.  Add additional metadata as needed.  

Using the *scheduled_views.txt* file, create a new view for each in the list.

Once created, it will take time to initially run the scheduled views and queue them up.  Once setup, querying for threats will be done off of these indexes. 

>**NOTE:**
Use the specified Index Name for the dashboards and queries to properly work!

### Import App

Once imported, the app should automatically be setup to query against the scheduled views created to optimize the app and its queries.