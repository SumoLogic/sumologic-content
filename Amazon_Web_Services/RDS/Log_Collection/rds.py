from datetime import datetime

import sys
import time
import ast
import boto3

# Start from 1 day ago if it hasn't been run yet
INITIAL_DAYS_TO_INGEST = 1

client=boto3.client('rds')

dBInstanceIdentifier='ENTER_INSTANCE_IDENTIFIER' #Enter your Instance ID here or as a command line argument
if len(sys.argv) > 1:
    dBInstanceIdentifier=sys.argv[1]

try:
    f=open(dBInstanceIdentifier + '_rds_log_state', 'r')
    lastReadDate=int(f.readline())
    readState=f.readline()
    f.close()
    readState=ast.literal_eval(readState)
except IOError:
    lastReadDate=int(round(time.time() * 1000)) - ((1000 * 60 * 60 * 24) * INITIAL_DAYS_TO_INGEST)
    readState={}

# Wait for the instance to be available -- need to possibly fix this or replace it with a custom waiter
#client.get_waiter('db_instance_available').wait(DBInstanceIdentifier=dBInstanceIdentifier)
#Get a list of the logs that have been modified since last run
dbLogs=client.describe_db_log_files(
    DBInstanceIdentifier=dBInstanceIdentifier,
    FileLastWritten=lastReadDate, # Base this off of last query
)
lastReadDate=int(round(time.time() * 1000))

# Iterate through list of log files and print out the entries
for logFile in dbLogs['DescribeDBLogFiles']:
    if logFile['LogFileName'] in readState:
        readMarker=readState[logFile['LogFileName']]
    else:
        readMarker='0'
    ext=['xel', 'trc'] # Ignore binary data log files for MSSQL
    if not logFile['LogFileName'].endswith(tuple(ext)):
        # Also may need to fix this waiter
        #client.get_waiter('db_instance_available').wait(
        #    DBInstanceIdentifier=dBInstanceIdentifier,
        #)
        response=client.download_db_log_file_portion(
            DBInstanceIdentifier=dBInstanceIdentifier,
            LogFileName=logFile['LogFileName'],
            Marker=readMarker,
        )
        if len(response['LogFileData']) > 0:
            logLines=response['LogFileData'].strip().splitlines() # LogFileData sends all entries as a single string. Split it up into a list to be able to append text to the start
            for entry in logLines:
                print("["+ dBInstanceIdentifier + " " + logFile['LogFileName'] + "] " + entry)
        readState[logFile['LogFileName']]=response['Marker']


f=open(dBInstanceIdentifier + '_rds_log_state', 'w')
f.write(str(lastReadDate))
f.write("\n")
f.write(str(readState))
f.close()
