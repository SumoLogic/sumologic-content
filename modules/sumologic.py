import json
import requests
import time
import logzero

from logzero import logger


try:
    import cookielib
except ImportError:
    import http.cookiejar as cookielib

class SumoLogic(object):

    def __init__(self, accessId, accessKey, endpoint=None, cookieFile='cookies.txt'):
        #logzero.loglevel(level=20)
        self.session = requests.Session()
        self.session.auth = (accessId, accessKey)
        self.session.headers = {'content-type': 'application/json', 'accept': 'application/json'}
        cj = cookielib.FileCookieJar(cookieFile)
        self.session.cookies = cj
        if endpoint is None:
            self.endpoint = self._get_endpoint()
        else:
            self.endpoint = endpoint
        if endpoint[-1:] == "/":
          raise Exception("Endpoint should not end with a slash character")

    def _get_endpoint(self):
        """
        SumoLogic REST API endpoint changes based on the geo location of the client.
        For example, If the client geolocation is Australia then the REST end point is
        https://api.au.sumologic.com/api/v1
        When the default REST endpoint (https://api.sumologic.com/api) is used the server
        responds with a 401 and causes the SumoLogic class instantiation to fail and this very
        unhelpful message is shown 'Full authentication is required to access this resource'
        This method makes a request to the default REST endpoint and resolves the 401 to learn
        the right endpoint
        Note the endpoint no longer includes "/v1" at the end as some of the new APIs use "/v2"
        """
        self.endpoint = 'https://api.sumologic.com/api'
        self.response = self.session.get('https://api.sumologic.com/api/v1/collectors')  # Dummy call to get endpoint
        endpoint = self.response.url.replace('/collectors', '')  # dirty hack to sanitise URI and retain domain
        return endpoint


    def delete(self, method, params=None, headers=None, data=None):
        logger.debug("DELETE: " + self.endpoint + method)
        logger.debug("Headers:")
        logger.debug(json.dumps(headers, indent=4))
        logger.debug("Params:")
        logger.debug(json.dumps(params, indent=4))
        logger.debug("Body")
        logger.debug(json.dumps(data, indent=4))
        r = self.session.delete(self.endpoint + method, params=params, headers=headers, data=data)
        logger.debug("Response:")
        logger.debug(r)
        logger.debug("Response Body:")
        logger.debug(r.text)
        if r.status_code != 200:
            r.reason = r.text
        r.raise_for_status()
        time.sleep(.30)
        return r


    def get(self, method, params=None, headers=None):
        logger.debug("GET: " + self.endpoint + method)
        logger.debug("Headers:")
        logger.debug(json.dumps(headers, indent=4))
        logger.debug("Params:")
        logger.debug(json.dumps(params, indent=4))
        r = self.session.get(self.endpoint + method, params=params, headers=headers)
        logger.debug("Response:")
        logger.debug(r)
        logger.debug("Response Body:")
        logger.debug(r.text)
        if r.status_code != 200:
            r.reason = r.text
        r.raise_for_status()
        time.sleep(.30)
        return r


    def post(self, method, data, headers=None, params=None):
        logger.debug("POST: " + self.endpoint + method)
        logger.debug("Headers:")
        logger.debug(json.dumps(headers, indent=4))
        logger.debug("Params:")
        logger.debug(json.dumps(params, indent=4))
        logger.debug("Body")
        logger.debug(json.dumps(data,indent=4))
        r = self.session.post(self.endpoint + method, data=json.dumps(data), headers=headers, params=params)
        logger.debug("Response:")
        logger.debug(r)
        logger.debug("Response Body:")
        logger.debug(r.text)
        if r.status_code != 200:
            r.reason = r.text
        r.raise_for_status()
        time.sleep(.30)
        return r


    def put(self, method, data, headers=None, params=None):
        logger.debug("PUT: " + self.endpoint + method)
        logger.debug("Headers:")
        logger.debug(json.dumps(headers, indent=4))
        logger.debug("Params:")
        logger.debug(json.dumps(params, indent=4))
        logger.debug("Body")
        logger.debug(json.dumps(data, indent=4))
        r = self.session.put(self.endpoint + method, data=json.dumps(data), headers=headers, params=params)
        logger.debug("Response:")
        logger.debug(r)
        logger.debug("Response Body:")
        logger.debug(r.text)
        if r.status_code != 200:
            r.reason = r.text
        r.raise_for_status()
        time.sleep(.30)
        return r

    # Search is deprecated
    # def search(self, query, fromTime=None, toTime=None, timeZone='UTC'):
    #     params = {'q': query, 'from': fromTime, 'to': toTime, 'tz': timeZone}
    #     r = self.get('/v1/logs/search', params)
    #     return json.loads(r.text)

    def search_job(self, query, fromTime=None, toTime=None, timeZone='UTC', byReceiptTime=False):
        data = {'query': str(query), 'from': str(fromTime), 'to': str(toTime), 'timeZone': str(timeZone), 'byReceiptTime': str(byReceiptTime)}
        r = self.post('/v1/search/jobs', data)
        return json.loads(r.text)

    def search_job_status(self, search_job):
        r = self.get('/v1/search/jobs/' + str(search_job['id']))
        return json.loads(r.text)

    def search_job_records_sync(self, query, fromTime=None, toTime=None, timeZone=None, byReceiptTime=None):
        searchjob = self.search_job(query, fromTime=fromTime, toTime=toTime, timeZone=timeZone, byReceiptTime=byReceiptTime)
        status = self.search_job_status(searchjob)
        numrecords = status['recordCount']
        while status['state'] != 'DONE GATHERING RESULTS':
            if status['state'] == 'CANCELLED':
                break
            status = self.search_job_status(searchjob)
            numrecords = status['recordCount']
        if status['state'] == 'DONE GATHERING RESULTS':
            jobrecords=[]
            iterations = numrecords // 10000 + 1

            for iteration in range(1, iterations + 1):
                records = self.search_job_records(searchjob, limit=10000,
                                                  offset=((iteration - 1) * 10000))
                for record in records['records']:
                    jobrecords.append(record)
            return jobrecords   #returns a list
        else:
            return status

    def search_job_messages_sync(self, query, fromTime=None, toTime=None, timeZone=None, byReceiptTime=None):
        searchjob = self.search_job(query, fromTime=fromTime, toTime=toTime, timeZone=timeZone, byReceiptTime=byReceiptTime)
        status = self.search_job_status(searchjob)
        nummessages = status['messageCount']
        while status['state'] != 'DONE GATHERING RESULTS':
            if status['state'] == 'CANCELLED':
                break
            status = self.search_job_status(searchjob)
            nummessages = status['messageCount']
        if status['state'] == 'DONE GATHERING RESULTS':
            jobmessages=[]
            iterations = nummessages // 10000 + 1

            for iteration in range(1, iterations + 1):
                messages = self.search_job_messages(searchjob, limit=10000,
                                                  offset=((iteration - 1) * 10000))
                for message in messages['messages']:
                    jobmessages.append(message)
            return jobmessages   #returns a list
        else:
            return status

    def search_job_messages(self, search_job, limit=None, offset=0):
        params = {'limit': limit, 'offset': offset}
        r = self.get('/v1/search/jobs/' + str(search_job['id']) + '/messages', params)
        return json.loads(r.text)

    def search_job_records(self, search_job, limit=None, offset=0):
        params = {'limit': limit, 'offset': offset}
        r = self.get('/v1/search/jobs/' + str(search_job['id']) + '/records', params)
        return json.loads(r.text)

    def delete_search_job(self, search_job):
        return self.delete('/v1/search/jobs/' + str(search_job['id']))

    def get_collectors(self, limit=1000, offset=None):
        params = {'limit': limit, 'offset': offset}
        r = self.get('/v1/collectors', params)
        return json.loads(r.text)['collectors']

    def get_collectors_sync(self, limit=1000):
        offset = 0
        results = []
        r = self.get_collectors(limit=limit, offset=offset)
        offset = offset + limit
        results = results + r
        while not(len(r) < limit):
            r = self.get_collectors(limit=limit, offset=offset)
            offset = offset + limit
            results = results + r
        return results

    def collector(self, collector_id):
        r = self.get('/v1/collectors/' + str(collector_id))
        return json.loads(r.text), r.headers['etag']

    def create_collector(self, collector, headers=None):
        return self.post('/v1/collectors', collector, headers)

    def update_collector(self, collector, etag):
        headers = {'If-Match': etag}
        return self.put('/v1/collectors/' + str(collector['collector']['id']), collector, headers)

    def delete_collector(self, collector_id):
        return self.delete('/v1/collectors/' + str(collector_id))

    def sources(self, collector_id, limit=None, offset=None):
        params = {'limit': limit, 'offset': offset}
        r = self.get('/v1/collectors/' + str(collector_id) + '/sources', params)
        return json.loads(r.text)['sources']

    def source(self, collector_id, source_id):
        r = self.get('/v1/collectors/' + str(collector_id) + '/sources/' + str(source_id))
        return json.loads(r.text), r.headers['etag']

    def create_source(self, collector_id, source):
        return self.post('/v1/collectors/' + str(collector_id) + '/sources', source)

    def update_source(self, collector_id, source, etag):
        headers = {'If-Match': etag}
        return self.put('/v1/collectors/' + str(collector_id) + '/sources/' + str(source['source']['id']), source, headers)

    def delete_source(self, collector_id, source_id):
        return self.delete('/v1/collectors/' + str(collector_id) + '/sources/' + str(source_id))

    def dashboards(self, monitors=False):
        params = {'monitors': monitors}
        r = self.get('/v1/dashboards', params)
        return json.loads(r.text)['dashboards']

    def dashboard(self, dashboard_id):
        r = self.get('/v1/dashboards/' + str(dashboard_id))
        return json.loads(r.text)['dashboard']

    def dashboard_data(self, dashboard_id):
        r = self.get('/v1/dashboards/' + str(dashboard_id) + '/data')
        return json.loads(r.text)['dashboardMonitorDatas']

    def search_metrics(self, query, fromTime=None, toTime=None, requestedDataPoints=600, maxDataPoints=800):
        '''Perform a single Sumo metrics query'''
        def millisectimestamp(ts):
            '''Convert UNIX timestamp to milliseconds'''
            if ts > 10**12:
                ts = ts/(10**(len(str(ts))-13))
            else:
                ts = ts*10**(12-len(str(ts)))
            return int(ts)

        data = {'query': [{"query":query, "rowId":"A"}],
                  'startTime': millisectimestamp(fromTime),
                  'endTime': millisectimestamp(toTime),
                  'requestedDataPoints': requestedDataPoints,
                  'maxDataPoints': maxDataPoints}
        r = self.post('/v1/metrics/results', data)
        return json.loads(r.text)

    # Folder API

    def create_folder(self, folder_name, parent_id, adminmode=False):
        headers = {'isAdminMode': str(adminmode)}
        data = {'name': str(folder_name), 'parentId': str(parent_id)}
        r = self.post('/v2/content/folders', data, headers=headers)
        return json.loads(r.text)

    def get_folder(self, folder_id, adminmode=False):
        headers = {'isAdminMode': str(adminmode).lower()}
        r = self.get('/v2/content/folders/' + str(folder_id), headers=headers)
        return json.loads(r.text)

    def get_personal_folder(self):
        r = self.get('/v2/content/folders/personal')
        return json.loads(r.text)

    def get_global_folder_job_status(self, job_id):
        r = self.get('/v2/content/folders/global/' + str(job_id) + '/status')
        return json.loads(r.text)

    def get_global_folder(self, adminmode=False):
        headers = {'isAdminMode': str(adminmode).lower()}
        r = self.get('/v2/content/folders/global', headers=headers)
        return json.loads(r.text)

    def get_global_folder_job_result(self, job_id):
        r = self.get('/v2/content/folders/global/' + str(job_id) + '/result')
        return json.loads(r.text)

    def get_global_folder_sync(self, adminmode=False):
        r = self.get_global_folder(adminmode=adminmode)
        job_id = str(r['id'])
        status = self.get_global_folder_job_status(job_id)
        while status['status'] == 'InProgress':
            status = self.get_global_folder_job_status(job_id)
        if status['status'] == 'Success':
            r = self.get_global_folder_job_result(job_id)
            return r
        else:
            return status

    def get_admin_folder_job_status(self, job_id):

        r = self.get('/v2/content/folders/adminRecommended/' + str(job_id) + '/status')
        return json.loads(r.text)

    def get_admin_folder(self, adminmode=False):
        headers = {'isAdminMode': str(adminmode).lower()}
        r = self.get('/v2/content/folders/adminRecommended',  headers=headers)
        return json.loads(r.text)

    def get_admin_folder_job_result(self, job_id):
        r = self.get('/v2/content/folders/adminRecommended/' + str(job_id) + '/result')
        return json.loads(r.text)

    def get_admin_folder_sync(self, adminmode=False):
        r = self.get_admin_folder(adminmode=adminmode)
        job_id = str(r['id'])
        status = self.get_admin_folder_job_status(job_id)
        while status['status'] == 'InProgress':
            status = self.get_admin_folder_job_status(job_id)
        if status['status'] == 'Success':
            r = self.get_admin_folder_job_result(job_id)
            return r
        else:
            return status
    # Content API

    def delete_content_job(self, item_id, adminmode=False):
        headers = {'isAdminMode': str(adminmode).lower()}
        r = self.delete('/v2/content/' + str(item_id) + '/delete', headers=headers)
        return json.loads(r.text)

    def get_delete_content_job_status(self, item_id, job_id, adminmode=False):
        headers = {'isAdminMode': str(adminmode)}
        r = self.get('/v2/content/' + str(item_id) + '/delete/' + str(job_id) + '/status', headers=headers)
        return json.loads(r.text)

    def delete_content_job_sync(self, item_id, adminmode=False):
        r = self.delete_content_job(str(item_id), adminmode=adminmode)
        job_id = str(r['id'])
        status = self.get_delete_content_job_status(str(item_id), str(job_id), adminmode=adminmode)
        while status['status'] == 'InProgress':
            status = self.get_delete_content_job_status(str(item_id), str(job_id), adminmode=adminmode)
        return status

    def export_content_job(self, item_id, adminmode=False):
        headers = {'isAdminMode': str(adminmode).lower()}
        data = {}
        r = self.post('/v2/content/' + str(item_id) + '/export', data, headers=headers)
        return json.loads(r.text)

    def get_export_content_job_status(self, item_id, job_id, adminmode=False):
        headers = {'isAdminMode': str(adminmode).lower()}
        r = self.get('/v2/content/' + str(item_id) + '/export/' + str(job_id) + '/status', headers=headers)
        return json.loads(r.text)

    def get_export_content_job_result(self, item_id, job_id, adminmode=False):
        headers = {'isAdminMode': str(adminmode).lower()}
        r = self.get('/v2/content/' + str(item_id) + '/export/' + str(job_id) + '/result', headers=headers)
        return json.loads(r.text)

    def export_content_job_sync(self, item_id, adminmode=False):
        r = self.export_content_job(str(item_id), adminmode=adminmode)
        job_id = str(r['id'])
        status = self.get_export_content_job_status(item_id, job_id, adminmode=adminmode)
        while status['status'] == 'InProgress':
            status = self.get_export_content_job_status(item_id, job_id, adminmode=adminmode)
        if status['status'] == 'Success':
            r = self.get_export_content_job_result(item_id, job_id, adminmode=adminmode)
            return r
        else:
            return status

    def import_content_job(self, folder_id, content, adminmode=False):
        headers = {'isAdminMode': str(adminmode).lower()}
        r = self.post('/v2/content/folders/' + str(folder_id) + '/import', content, headers=headers)
        return json.loads(r.text)

    def get_import_content_job_status(self, folder_id, job_id, adminmode=False):
        headers = {'isAdminMode': str(adminmode).lower()}
        r = self.get('/v2/content/folders/' + str(folder_id) + '/import/' + str(job_id) + '/status', headers=headers)
        return json.loads(r.text)

    def import_content_job_sync(self, folder_id, content, adminmode=False):
        r = self.import_content_job(str(folder_id), content, adminmode=adminmode)
        job_id = str(r['id'])
        status = self.get_import_content_job_status(str(folder_id), str(job_id), adminmode=adminmode)
        while status['status'] == 'InProgress':
            status = self.get_import_content_job_status(str(folder_id), str(job_id), adminmode=adminmode)
        return status


    # User API

    def get_users(self, limit=1000, token=None, sort_by='lastName', email=None):
        params = {'limit': limit, 'token': token, 'sortBy': sort_by, 'email':email }
        r = self.get('/v1/users', params=params)
        return json.loads(r.text)

    def get_user(self, user_id):
        r = self.get('/v1/users/' + str(user_id))
        return json.loads(r.text)

    def create_user(self, first_name, last_name, email, roleIDs):
        data = {'firstName': str(first_name), 'lastName': str(last_name), 'email': str(email), 'roleIds': roleIDs}
        r = self.post('/v1/users', data)
        return json.loads(r.text)

    # Connections API

    def get_connections(self, limit=1000, token=''):
        params = {'limit': limit, 'token': token}
        r = self.get('/v1/connections', params=params)
        return json.loads(r.text)

    def get_connections_sync(self, limit=1000):
        token = None
        results = []
        while not(token):
            r = self.get_connections(limit=limit, token=token)
            token = r['next']
            results = results + r['data']
        return results

    # Field Extraction Rules API

    def get_fers(self, limit=1000, token=''):
        params = {'limit': limit, 'token': token}
        r = self.get('/v1/extractionRules', params=params)
        return json.loads(r.text)

    def get_fers_sync(self, limit=1000):
        token = None
        results = []
        while True:
            r = self.get_fers(limit=limit, token=token)
            token = r['next']
            results = results + r['data']
            if token is None:
                break
        return results

    def create_fer(self, name, scope, parse_expression, enabled=False):
        data = {'name': name, 'scope': scope, 'parseExpression': parse_expression, 'enabled': str(enabled).lower()}
        r = self.post('/v1/extractionRules', data)
        return json.loads(r.text)

    def get_fer(self, item_id):
        r = self.get('/v1/extractionRules/' + str(item_id))
        return json.loads(r.text)

    def update_fer(self, item_id, name, scope, parse_expression, enabled=False):
        data = {'name': name, 'scope': scope, 'parseExpression': parse_expression, 'enabled': str(enabled).lower()}
        r = self.put('/v1/extractionRules/' + str(item_id), data)
        return json.loads(r.text)

    def delete_fer(self, item_id):
        r = self.delete('/v1/extractionRules/' + str(item_id))
        return r.text


    # Scheduled View API

    def get_scheduled_views(self, limit=1000, token=''):
        params = {'limit': limit, 'token': token}
        r = self.get('/v1/scheduledViews', params=params)
        return json.loads(r.text)

    def get_scheduled_views_sync(self, limit=1000):
        token = None
        results = []
        while True:
            r = self.get_scheduled_views(limit=limit, token=token)
            token = r['next']
            results = results + r['data']
            if token is None:
                break
        return results

    #start time must be in RFC3339 format
    # https://tools.ietf.org/html/rfc3339
    # https://medium.com/easyread/understanding-about-rfc-3339-for-datetime-formatting-in-software-engineering-940aa5d5f68a
    def create_scheduled_view(self, index_name, query, start_time, retention_period=-1, data_forwarding_id=None):
        data = {'indexName': index_name, 'query': query, 'startTime': start_time, 'retentionPeriod': retention_period, "dataForwardingId": data_forwarding_id }
        r = self.post('/v1/scheduledViews', data)
        return json.loads(r.text)

    def get_scheduled_view(self, item_id):
        r = self.get('/v1/scheduledViews/' + str(item_id))
        return json.loads(r.text)

    def update_scheduled_view(self, item_id, data_forwarding_id=None, retention_period=-1, reduce_retention_period_immediately=False):
        data = {'retentionPeriod': retention_period, "dataForwardingId": data_forwarding_id, "reduceRetentionPeriodImmediately" : str(reduce_retention_period_immediately).lower()}
        r = self.put('/v1/scheduledViews/' + str(item_id), data)
        return json.loads(r.text)

    def disable_scheduled_view(self, item_id):
        r = self.delete('/v1/scheduledViews/' + str(item_id) + '/disable')
        return r.text



