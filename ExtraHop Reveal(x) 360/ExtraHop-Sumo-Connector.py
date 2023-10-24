#!/usr/bin/python3

# ExtraHop-Sumo-Connector.py


import boto3
import decimal
import json
import logging
import os
import urllib3

from botocore.exceptions import ClientError
from botocore.config import Config

# set up boto3 retry options
config = Config(retries={"max_attempts": 5, "mode": "standard"})

# set up logging
logging.basicConfig(
    format="[%(levelname)-4s, line %(lineno)d] %(message)s",
    datefmt="%d-%m-%Y:%H:%M:%S",
    level=logging.INFO,
    force=True,
)
logger = logging.getLogger(__name__)


def deserializeItem(low_level_data):
    # Lazy-eval the dynamodb attribute (boto3 is dynamic!)
    boto3.resource("dynamodb")
    # Go from low-level format to python dict
    deserializer = boto3.dynamodb.types.TypeDeserializer()
    python_data = {k: deserializer.deserialize(v) for k, v in low_level_data.items()}
    return python_data


def replaceDecimals(obj):
    # Recursive function to find all Decimal instances and replace
    # with int and float
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = replaceDecimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in iter(obj.keys()):
            obj[k] = replaceDecimals(obj[k])
        return obj
    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj


def get_parameter(key):
    """
    Returns the value of the key provided from the Systems Manager
    Prameter Store (SSM).
    """
    ssm = boto3.client("ssm", config=config)
    resp = ssm.get_parameter(Name=key, WithDecryption=True)

    logger.debug(f"Response from SSM Client:{resp}")
    try:
        param_value = resp["Parameter"]["Value"]
    except ClientError as e:
        raise e
    else:
        return param_value


## MAIN
def handler(event, context):
    """
    Triggers on an event passed from DynamoDB stream for table, "ExtraHop-Detections".
    On a new detection create or update the new version is passed to this function.
    Items in stream are converted from DynamoDB low level data back to their original
    structure then forwarded to the Sumo Logic logs API for ingestion.
    """

    # Get target URL from Parameter Store
    target = str(get_parameter("/ExtraHop/Rx360/Integrations/SumoLogic/ConnectorUrl"))

    db_items = [item["dynamodb"] for item in event["Records"]]
    # DynamoDB streams are low level data structures and need to be unmarshaled
    # These items have the detection id and type at a higher level since those are
    # being used as the partition and sort keys, let's colapse them back into the obj
    converted_items = []
    for item in db_items:
        # colapse the item
        colapsed_item = {
            "id": item["Keys"]["detection_id"],
            "type": item["Keys"]["type"],
        }
        colapsed_item.update(item["NewImage"])
        # deserialize the low level data into a dict then replace the decimals
        # with ints and floats as needed.  Append to a new list of items.
        converted_item = replaceDecimals(deserializeItem(colapsed_item))
        converted_items.append(converted_item)

    entries = 0
    sumo_errors = []
    http = urllib3.PoolManager()

    for item in converted_items:
        sumoLogging = http.request_encode_body(
            method="POST",
            url=target,
            headers={"Content-Type": "application/json"},
            encode_multipart=False,
            body=json.dumps(item),
        )
        resp_data = (
            json.loads(sumoLogging.data.decode("utf-8")) if sumoLogging.data else None
        )
        if sumoLogging.status >= 400:
            sumo_errors.append({"id": item["detection_id"], "response": resp_data})
            logger.info(resp_data)
        else:
            logger.info(
                f"Success! Status code:{sumoLogging.status} from Sumo "
                f'for Detection id:{item["detection_id"]}'
            )
            entries += 1
    if len(sumo_errors) > 0:
        return {
            "statusCode": 400,
            "body": (
                "There were errors with the following detection IDs"
                f':{str([e["id"] for e in sumo_errors])}'
            ),
        }
    else:
        return {
            "statusCode": 201,
            "body": f"Pushed {entries} detections to Sumo Logic.",
        }
