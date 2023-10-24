#!/usr/bin/python3

# ExtraHop-Detection-Sync.py


import base64, boto3, decimal, json, logging, os, urllib3, time, random, base64

from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
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


def boto3_retry_handler(fn, retries=5, backoff_in_seconds=1):
    """
    Accepts a boto3 client function and handles any encountered `429`
    rate limit exceeded errors by implementing exponential backoff and
    adding some jitter.
        Parameters:
            fn (func): a boto3 client function
            retries (int): number of times to retry if rate limit exceeded
            backoff_in_seconds (int): number of seconds to wait after first failure
        Returns:
            boto3 client response or raised exception
    """
    x = 0
    while True:
        try:
            return fn()
        except ClientError as error:
            if error.response.get("Error").get("Code") == "LimitExceededException":
                if x == retries - 1:
                    raise
                else:
                    sleep = backoff_in_seconds * 2**x + random.uniform(0, 1)
                    time.sleep(sleep)
                    x += 1
            else:
                raise


def get_token(Api_id, Api_secret, Target):
    """
    Method that generates and retrieves a REST API token for Reveal(x) 360 authentication.

        Returns:
            str: A REST API token
    """
    id_secret = f"{Api_id}:{Api_secret}"
    auth = base64.b64encode(bytes(id_secret, "utf-8")).decode("utf-8")
    headers = {
        "Authorization": "Basic " + auth,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    http = urllib3.PoolManager()
    r = http.request_encode_body(
        method="POST",
        url=f"{Target}/oauth2/token",
        headers=headers,
        encode_multipart=False,
        fields={"grant_type": "client_credentials"},
    )
    tokenResp = json.loads(r.data.decode("utf-8")) if r.data else None
    logger.debug("Reveal(X) 360 /oauth2/token response:" + json.dumps(tokenResp))
    return tokenResp.get("access_token")


def get_detections(Lookback: int, Target, Token):
    logger.debug(f"Lookback ({type(Lookback)}): {Lookback}")

    Now = int(time.time() * 1000)
    logger.debug(f"Now ({type(Now)}): {Now}")

    From = Now - Lookback
    logger.debug(f"From ({type(From)}): {From}")

    headers = {"Authorization": "Bearer " + Token}
    http = urllib3.PoolManager()
    r = http.request_encode_body(
        method="POST",
        url=f"{Target}/api/v1/detections/search",
        headers=headers,
        encode_multipart=False,
        body=json.dumps({"from": From, "until": 0}),
    )

    logger.info(f"Reveal(X) 360 /detections/search status code:" f"{str(r.status)}")
    r_data = json.loads(r.data.decode("utf-8")) if r.data else None
    logger.debug(f"r_data ({type(r_data)}): {r_data}")
    returned_ids = [d.get("id") for d in r_data]
    logger.info(
        f"Reveal(X) 360 /detections/search returned the following Detection IDs:"
        f"{str(returned_ids)}"
    )
    if r.status >= 400:
        logger.error(
            "Failed to get recent Detections from Reveal(X) 360, status code:"
            f"{str(r.status)}"
        )
    else:
        return r_data


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


def get_secret(Secret_name):
    secretsmanager = boto3.client("secretsmanager", config=config)

    try:
        get_secret_value_response = secretsmanager.get_secret_value(
            SecretId=Secret_name
        )

    except ClientError as e:
        raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary,
        # one of these fields will be populated.
        if "SecretString" in get_secret_value_response:
            secret = get_secret_value_response["SecretString"]
        else:
            secret = base64.b64decode(get_secret_value_response["SecretBinary"])
        return secret


def db_get_detection(Detection, Table):
    """Queries for a Detection in a DynamoDB table.
    Returns the matching items as a list."""
    logger.info(
        f'Querying DB with "id"=[{str(Detection["id"])}]'
        f' and "type"=[{str(Detection["type"])}]'
    )

    response = Table.query(
        KeyConditionExpression=Key("detection_id").eq(Detection["id"])
        & Key("type").eq(Detection["type"])
    )

    return response.get("Items")


def db_device_in_detection(Device_id, Item):
    """Checks a result of the "db_get_detection()" function to see if a participant
    is already present, returns device details if present, else returns None"""
    devices = [d for d in Item["offenders"] if d["object_type"] == "device"]
    devices.extend([d for d in Item["victims"] if d["object_type"] == "device"])
    for obj in devices:
        if obj["object_id"] == Device_id:
            return obj["device_details"] if "device_details" in obj else None


def get_device_details(Object_id, Target, Token):
    """Gets the Device Details for a Device Object ID from Reveal(X) 360.
    Returns the response body"""
    headers = {"Authorization": "Bearer " + Token}
    http = urllib3.PoolManager()
    r = http.request_encode_body(
        method="GET",
        url=f"{Target}/api/v1/devices/{str(Object_id)}",
        headers=headers,
        encode_multipart=False,
    )

    logger.debug(f"Reveal(X) 360 /device/{str(Object_id)} status code:{r.status}")
    if r.status >= 400:
        logger.warning("Failed to get details for Device id:" + {str(Object_id)})
        return {}
    else:
        return json.loads(r.data.decode("utf-8")) if r.data else None


def replace_decimals(obj):
    # Recursive function to find all Decimal instances and replace
    # with int and float
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = replace_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in iter(obj.keys()):
            obj[k] = replace_decimals(obj[k])
        return obj
    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj


def handler(event, context):
    """
    Accepts an event object such as:
    {
        "host": "customer.api.cloud.extrahop.com",           #Reveal(X) 360 target
        "lookback": -300000                                  #negative lookback in ms
    }
    Gets all Detections which were active within the lookback period and writes them to a
    DynamoDB table called, "ExtraHop-Detections". Before writing, all Detections are
    processed and Detection Participants are sorted into separate lists for Offenders and
    Victims. Each Participant which is a Device Object (and not an IP Address Object) get's
    an additional request made to Reveal(X) 360 for it's Device Details and these are
    appended to the Participant's database entry for added context.
    If a Detection has already been written to the database it will only be updated.
    If a Detection Participant's details are already in the database, it won't be queried
    again.
    """

    # Get event values if present, else use environment variables
    lookback = int(
        event.get(
            "lookback",
            get_parameter("/ExtraHop/Rx360/Administration/DetectionLookback"),
        )
    )
    target = event.get("host", get_parameter("/ExtraHop/Rx360/API/URL"))

    # Get API ID and Secret from event else get from the Secrets Manager
    rx_secrets = json.loads(get_secret("/ExtraHop/Rx360/API/DetectionSync"))
    logger.debug(f"Connecting to Reveal(x) 360 with:\n {rx_secrets}")
    if not (lookback or target or rx_secrets):
        return {
            "statusCode": 400,
            "body": ("Missing required parameters"),
        }
    api_id = rx_secrets["rx360_id"]
    api_secret = rx_secrets["rx360_secret"]

    logger.info(
        "Executing with the following parameters:"
        f"DetectionLookback={lookback},"
        f"Reveal(X) API ID=*******{api_id[-4::]},"
        f"Reveal(X) API Secret=*******{api_secret[-4::]},"
        f"Reveal(X) URL ={target}"
    )

    # get an access token from Reveal(X) 360
    token = get_token(api_id, api_secret, target)
    if not token:
        logger.error("failed to aquire an access token from Reveal(X) 360")
        return {
            "statusCode": 400,
            "body": "Execution failed, could not aquire an access token from Reveal(X) 360.",
        }

    # get recent Detections
    logger.info("Getting recent Detections.")
    returned_detections = get_detections(lookback, target, token)
    if not returned_detections:
        return {
            "statusCode": 200,
            "body": (
                "No recent Detections were returned from Reveal(X) 360."
                "Nothing to process."
            ),
        }

    logger.info('Preparing DynamoDB table, "ExtraHop-Detections".')
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("ExtraHop-Detections")

    # Sort offenders and victims, get additional info about each participant
    logger.info(
        "Sorting all Detection participants into offenders and victims "
        "and getting additional details for devices."
    )
    mod_detections = []
    for detection in returned_detections:
        logger.info(f'Processing Detection id:{str(detection["id"])}')
        participants = detection["participants"]
        db_items = db_get_detection(Detection=detection, Table=table)
        if not db_items:
            logger.info(
                f'Detection:{detection["id"]} is not in the DB, this is first observation.'
            )
            detection["is_new"] = True
        else:
            detection["is_new"] = False
        if (
            db_items
            and replace_decimals(db_items[0])["update_time"] == detection["update_time"]
        ):
            logger.info(
                f'Detection:{detection["id"]} last update already in DB, skipping'
            )
            continue

        for p in participants:
            if p["object_type"] == "device":
                details = (
                    db_device_in_detection(Device_id=p["object_id"], Item=db_items[0])
                    if len(db_items) >= 1
                    else None
                )
                if details:
                    logger.info("Device details already in DynamoDB.")
                    p["device_details"] = details
                else:
                    logger.info(
                        f'Device details for {str(p["object_id"])} not found in DynamoDB, '
                        "getting from Reveal(X) 360."
                    )
                    p["device_details"] = get_device_details(
                        Object_id=p["object_id"], Target=target, Token=token
                    )
        detection["offenders"] = [o for o in participants if o["role"] == "offender"]
        detection["victims"] = [v for v in participants if v["role"] == "victim"]
        del detection["participants"]
        url = (
            f'{target.replace(".api.",".")}/extrahop/#/'
            f'detections/detail/{str(detection["id"])}'
        )
        detection["url"] = url
        detection["detection_id"] = detection["id"]
        del detection["id"]
        mod_detections.append(detection)

    if len(mod_detections) == 0:
        return {
            "statusCode": 200,
            "body": f"No new detection updates to process.",
        }
    entries = 0
    errors = []
    for detection in mod_detections:
        db_put = table.put_item(Item=detection)
        if "error" not in db_put:
            entries += 1
            logger.debug(
                f'Successfully wrote Detection ID:{str(detection["detection_id"])} to DynamoDB.'
            )
        else:
            err_obj = {"id": detection["detection_id"], "error": str(db_put["error"])}
            errors.append(err_obj)
            logger.error(f"Error writing Detection to DynamoDB. {json.dumps(err_obj)}")
    if errors:
        return {
            "statusCode": 400,
            "body": (
                f"Wrote {entries} Detections to DynamoDB, some Detections "
                "failed when writing to DynamoDB. Detections with errors:"
                f"{print([json.dumps(e) for e in errors])}"
            ),
        }
    else:
        return {
            "statusCode": 201,
            "body": f"Pushed {entries} detections to ExtraHop-Detections DynamoDB table.",
        }
