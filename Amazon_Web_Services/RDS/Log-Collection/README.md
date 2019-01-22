# RDS Log Ingestion Script (Beta)

**Disclaimer**: This script is still being tested, and it is community supported.

RDS collects different logs depending on the database engine. They include different ones such as error, slow query, general, audit, and trace logs depending on the engine. These are for the most part the standard vendor logs these database engines typically have outside of RDS as well, so prebuilt Sumo content should work typically.

To collect RDS logs, you'll first need to determine which database engine is being used with RDS. There are currently 6 database engines that can be used for RDS:

* Aurora
* PostgreSQL
* MySQL
* MariaDB
* Oracle
* Microsoft SQL Server

Aurora MySQL, MySQL, and MariaDB logs can be configured to send their logs to CloudWatch Logs. Follow this AWS blog post on how to configure it: [Monitor Amazon Aurora MySQL, Amazon RDS for MySQL and MariaDB logs with Amazon CloudWatch](https://aws.amazon.com/blogs/database/monitor-amazon-rds-for-mysql-and-mariadb-logs-with-amazon-cloudwatch/).

Once those logs are forwarded to CloudWatch Logs, then the standard Sumo Lambda function will work to pull those logs into Sumo Logic.

For all other database engines, the logs are not made readily available at this time. These engines will require the AWS API to access those logs and pull them into Sumo Logic. A script is currently being developed to pull these logs into Sumo Logic, but the general flow is:

1. Install the [AWS CLI](https://aws.amazon.com/cli/) as root on an instance with Python.
2. Configure the AWS CLI as the "root" user of the instance, and configure it with an IAM user with the permissions in the permission.json file.
3. Install the [AWS SDK for Python (boto3)](https://aws.amazon.com/sdk-for-python/) as root.
4. Copy the Python script (rds.py) to a folder on the instance.
5. Test the script by running python *rds.py [INSTANCE-NAME]*. It will pull all logs from the last day. You can configure this in the rds.py file under "INITIAL_DAYS_TO_INGEST=". Note that going too far back may throttle your AWS API access. Future iterations of this script should handle throttling to bring in more historial logs.
6. You should see the log files stream across the command line, and you'll see a temporary file created in that folder called *[INSTANCE-NAME]_rds_log_state*. This will store the state of the last log messages the script read. The next time the script runs, it will use this file to know to only pull logs since the last time the script ran.
7. Delete the temporary file if you want the script to pull all the logs from the test, or leave it if you only want it pulling logs going forward from the current time.
9. Configure a [Script Source](https://help.sumologic.com/Send-Data/Sources/01Sources-for-Installed-Collectors/Script-Source) to run the rds.py script.

# Notes

* The script currently passes over .XEL and .TRC log files for Microsoft SQL Server. These are binary data files that cannot be read in plaintext.
