# AWSCloudwatchExistingLogsSender

This script downloads existing log files from a given AWS CloudWatch log group withing a start and end interval. It generates a shell script which can be used to ingest the downloaded files into Sumo Logic.

Note - The script hasn't been tested for very large file sizes and very long time range. It is recommended to use it for smaller intervals.

## Prerequisites

* Linux machine with Python 3 installed
* Install and setup boto 3  https://pypi.org/project/boto3/
* Export the profile. For more information https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html
    
      export AWS_PROFILE="prod"

* Export the region where the loggroup is located
      
      export AWS_REGION="us-west-2"
      
* Export the sumologic http source endpoint
      
      export SUMO_HTTP_ENDPOINT="https://collectors.sumologic.com/receiver/v1/http/<token>"

## Downloading the files

Run the below command replacing loggroup, start epoch milliseconds and end epoch milliseconds.

    python downloadexistingcwlogs.py --log-group "/aws/lambda/AG"  --start-epoch-milli 1476814230000 --end-epoch-milli 1476814237000 >> download_log.txt 2>&1

Check if any stream failed to download re run above command with stream-name-prefix from the Error line which is printed in log.txt

    python downloadexistingcwlogs.py --log-group "/aws/lambda/AG"  --start-epoch-milli 1596656636000 --end-epoch-milli 1596656876000 --stream-name-prefix "stream name" >> download_log.txt 2>&1

The above command creates a cwlogsdump folder in current working directory and appends the bash file with curl commands

Check whether file size is less than 1MB, if not then break the file and update the curl command for that file in send_to_sumo.sh
    
    ls -ltrh cwlogsdump/

Note down the number of files

## Sending the files

    sh send_to_sumo.sh >> send_to_sumo_log.txt 2>&1

To verify whether all files are sent successfully grep for "We are completely uploaded and fine" line in log file.It should match the number of files.

## Cleanup
    rm -r download_log.txt  send_to_sumo_log.txt cwlogsdump send_to_sumo_*.sh

## Sample log
Note here ingestionTime is replaced with id to keep the log format consistent

``` json
{
    "timestamp": 1596656776311
    , "message": "REPORT RequestId: c07c185a-5616-4bd4-b208-5b099daaa7ce\tDuration: 120270.62 ms\tBilled Duration: 120300 ms\tMemory Size: 128 MB\tMax Memory Used: 80 MB\t
    ",
    "id": 1596656785159
}
```
