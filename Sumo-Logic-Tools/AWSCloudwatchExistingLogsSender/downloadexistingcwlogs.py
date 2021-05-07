#!/usr/bin/env python
import os
import re
import time
import math
import calendar
import threading
import argparse
from functools import partial
import json
import boto3
from botocore.config import Config
import traceback

config = Config(retries={'max_attempts': 5, 'mode': 'standard'})
LOG_EVENTS_PAGINATION = 10000
GET_STREAMS_PAGINATION = 50
LOGDUMP_FOLDER = "cwlogsdump"
SUMO_HTTP_ENDPOINT = os.getenv('SUMO_HTTP_ENDPOINT')
AWS_REGION = os.getenv('AWS_REGION')
logfile_metadata = []


def slugify(text):
    # replacing any contiguous sequence of non alphabet(spaces, "_" etc) with underscore `-`
    text = re.sub(r"[ @_!#$%^&*()<>?/\|}{~:`',\\\[\]]+", '-', text.strip())
    # replacing any contiguous - with single -
    text = re.sub(r"[-]+", '-', text.strip())

    # remove last -
    text = text.strip("-")
    return text


def split(l, n):
    size = int(math.ceil(len(l)/float(n)))
    cutoff = len(l) % n
    result = []
    pos = 0
    for i in range(0, n):
        end = pos + size if cutoff == 0 or i < cutoff else pos + size - 1
        result.append(l[pos:end])
        pos = end
    return result


def get_streams(logGroup, start, end, prefix):
    '''
      returns all the log streams by fetching 50 stream per request present in
      a given log group within start and end interval
    '''
    client = boto3.client('logs', region_name=AWS_REGION, config=config)

    token = None
    first = True
    streams = []
    if prefix:
        get_streams = partial(client.describe_log_streams,
                              logGroupName=logGroup,
                              logStreamNamePrefix=prefix,
                              orderBy='LastEventTime',
                              descending=True,
                              limit=GET_STREAMS_PAGINATION)
    else:
        get_streams = partial(client.describe_log_streams,
                              logGroupName=logGroup, limit=GET_STREAMS_PAGINATION)
    while first or token:
        if token:
            batch = get_streams(nextToken=token)
        else:
            batch = get_streams()
        if not batch['logStreams']:
            break
        for stream in batch['logStreams']:
            if end < stream.get('firstEventTimestamp', end + 1):
                continue
            if start > stream.get('lastEventTimestamp', start - 1):
                continue
            streams.append(stream['logStreamName'])

        #  exit because log streams in next pages will have events before start timestamp
        if batch['logStreams'][-1].get('lastEventTimestamp', start - 1) < start:
            break
        token = batch.get('nextToken')
        first = False
    return streams


def download_files(logGroup, streams, start, end):
    '''
        fetches 10k events from a given loggroup and streams within start and end interval and saves all the events in a .log file
    '''
    client = boto3.client('logs', region_name=AWS_REGION, config=config)

    for stream_name in streams:
        print("Fetching data from stream: %s between start: %d end: %d" % (stream_name, start, end))
        token = None
        first = True
        filename = "%s-%s.log" % (logGroup, stream_name)
        filename = slugify(filename)
        filepath = os.path.join(LOGDUMP_FOLDER, filename)

        try:
            # overwrites the file if it exists or create a new one
            with open(filepath, "w+") as logfile:
                while first or token:
                    if token:
                        events = client.get_log_events(
                            logGroupName=logGroup, logStreamName=stream_name, nextToken=token,
                            startTime=start, endTime=end, limit=LOG_EVENTS_PAGINATION)
                    else:
                        events = client.get_log_events(
                            logGroupName=logGroup, logStreamName=stream_name, startTime=start,
                            endTime=end, limit=LOG_EVENTS_PAGINATION)
                    if not events['events']:
                        break
                    for ev in events['events']:
                        if ev['timestamp'] >= start and ev['timestamp'] <= end:
                            # changing ingestionTime (when CW received logline) to id to make the format consistent
                            ev["id"] = ev.pop("ingestionTime")
                            logfile.write(json.dumps(ev) + os.linesep)
                    token = events.get('nextForwardToken')
                    first = False
            print("Finished writing to file: %s" % (filepath))
            logfile_metadata.append((filepath, logGroup, stream_name))
        except Exception as e:
            print("Failed to fetch stream: %s Error: %s Traceback: %s" % (s, e, traceback.format_exc()))


def create_curl_file():
    # appends to the file if it exists or create a new one
    curl_filename = "send_to_sumo_%s.sh" % time.strftime("%Y%m%d-%H%M%S")
    print('Generating the send_to_sumo curl command file: %s' % curl_filename)
    with open(curl_filename, 'w+') as shfile:
        first_line = "#!bin/bash"
        shfile.write(first_line+os.linesep)
        shfile.write(os.linesep)
        for (filepath, logGroup, stream_name) in logfile_metadata:
            cmd = "curl -v -X POST -T \"%s\" \"%s\" -H 'Content-Encoding:application/json' -H 'X-Sumo-Name:%s' -H 'X-Sumo-Host:%s'" % (filepath, SUMO_HTTP_ENDPOINT, stream_name, logGroup)
            shfile.write(cmd+os.linesep)

if __name__ == "__main__":
    # build args
    parser = argparse.ArgumentParser()
    parser.add_argument('--log-group', type=str,
                        help='The name of the log group whose logs we are targeting', required=True)
    parser.add_argument('--start-epoch-milli', type=int,
                        help='Show only stuff that is later than or equal to this', default=0)
    parser.add_argument('--end-epoch-milli', type=int, help='Show only stuff that is earlier than or equal to this',
                        default=calendar.timegm(time.gmtime()) * 1000)
    parser.add_argument('--stream-name-prefix', type=str,
                        help='A prefix to only show log streams whose names match')
    parser.add_argument('--threads', type=int,
                        help='How many threads to use at one time', default=1)

    args = parser.parse_args()

    print("========= Starting Log Group Downloader for: %s ===========\n" % args.log_group)
    # creating directory
    if not os.path.isdir(LOGDUMP_FOLDER):
        os.mkdir(LOGDUMP_FOLDER)

    # get the proper log streams
    streams = get_streams(args.log_group, args.start_epoch_milli,
                          args.end_epoch_milli, args.stream_name_prefix)

    print("Total Log streams fetched between start: %s end: %s : %d" % (args.start_epoch_milli, args.end_epoch_milli, len(streams)))

    # for each chunk of streams spawn a thread to get them
    streams = split(streams, args.threads)
    threads = []
    for s in streams:
        threads.append(threading.Thread(target=download_files, args=(
            args.log_group, s, args.start_epoch_milli, args.end_epoch_milli)))
        threads[-1].start()
    for t in threads:
        t.join()

    # generate sh file containing curl commands to post data to sumo
    create_curl_file()



