# Data Volume Analysis

These are dashboards and queries to analyze and investigate to find things like where a spike in ingestion began.

## Setup

### Turn On Data Volume Index

Make sure the [Data Volume Index](https://help.sumologic.com/Manage/Ingestion-and-Volume/Enable-and-Manage-the-Data-Volume-Index) is enabled.  There must be enough data logged in the index for these dashboards to properly analyze the data.

### Import App

Once imported, the app should automatically be setup to show the top ingestion by different metadatas by timeslice and the largest spikes on those days.