import json
import logging
import json
from urllib.parse import urljoin
import requests

logger = logging.getLogger('sumologic')


class ApiClient:
    '''
    Sumologic API client.

    Supports POST, GET, PUT, and DELETE HTTP methods.
    On success, requests.Response object is returned. On failure (HTTP status
    code >= 400), exception requests.HTTPError is raised.
    '''

    def __init__(self, access_id, access_key, endpoint):
        self._validate(access_id, access_key, endpoint)

        self.headers = {
            'content-type': 'application/json',
            'accept': 'application/json',
            'user-agent': 'sumologic-python-client/0.0.1'
        }
        self.timeout = 30  # request timeout in seconds
        self.auth = requests.auth.HTTPBasicAuth(access_id, access_key)
        self.endpoint = endpoint

        self.kwargs = {
            'headers': self.headers,
            'auth': self.auth,
            'timeout': self.timeout
        }

    def _validate(self, access_id, access_key, endpoint):
        url = urljoin(endpoint, "v1/users?limit=1")
        auth = requests.auth.HTTPBasicAuth(access_id, access_key)
        ok = True
        try:
            rsp = requests.get(url=url, auth=auth, timeout=10)
            if rsp.status_code == requests.codes.unauthorized:
                msg = "Invalid credentials. Please verify credentials."
                ok = False
            elif rsp.status_code == requests.codes.not_found:
                msg = ("Invalid endpoint. Please see list of endpoints at " +
                       "https://api.sumologic.com/docs/#section/API-Endpoints")
                ok = False
        except requests.exceptions.InvalidURL:
            msg = ("Invalid url: " + endpoint)
            ok = False

        if not ok:
            raise ValueError(msg)

    def post(self, uri, params=None, data=None):
        return self._invoke_request(
            'POST', uri, params=params, data=json.dumps(data))

    def get(self, uri, params=None):
        return self._invoke_request('GET', uri, params=params)

    def put(self, uri, params=None, data=None):
        return self._invoke_request(
            'PUT', uri, params=params, data=json.dumps(data))

    def delete(self, uri, params=None):
        return self._invoke_request('DELETE', uri, params=params)

    def _invoke_request(self, method, uri, params=None, data=None):
        url = urljoin(self.endpoint, uri)
        rsp = requests.request(
            method, url, params=params, data=data, **self.kwargs)
        logger.debug("Got response. code: %s, body: %s", rsp.status_code,
                     rsp.text)
        self._handle_response(rsp)
        return rsp

    def _handle_response(self, rsp):
        if not rsp.ok:
            body = rsp.text
            if rsp.headers['content-type'] == 'application/json':
                body = json.dumps(rsp.json(), indent=4)
            logger.error("Request '%s %s' failed. code: %s, error: %s",
                         rsp.request.method, rsp.url, rsp.status_code, body)
        rsp.raise_for_status()
