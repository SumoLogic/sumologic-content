import json
import logging
import time

logger = logging.getLogger('sumologic')


class AsyncJobStatus:
    IN_PROGRESS = "InProgress"
    SUCCESS = "Success"
    FAILED = "Failed"


class AsyncJobException(Exception):
    def __init__(self, message, error=None):
        self.message = message
        self.error = error

    def __str__(self):
        return self.message


def wait_for_job(api_client, uri, wait_time=60*2):
    job_status = api_client.get(uri).json()
    timeout = time.time() + wait_time
    while (job_status['status'] == AsyncJobStatus.IN_PROGRESS and
            time.time() < timeout):
        time.sleep(1)
        job_status = api_client.get(uri).json()

    if job_status['status'] == AsyncJobStatus.IN_PROGRESS:
        logger.error("Timed out waiting for job: {}".format(uri))
        raise AsyncJobException("Timed out waiting for job")
    elif job_status['status'] == AsyncJobStatus.FAILED:
        logger.error("Job '{0}' failed: {1}".format(uri, job_status['error']))
        raise AsyncJobException("Job failed", error=job_status['error'])

    return job_status
