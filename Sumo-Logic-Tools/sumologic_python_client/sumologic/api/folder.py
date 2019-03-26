from .. import _async_job


class FolderManagementApi:
    '''
    Folder Management API.

    Manage folders in your organization’s library.
    '''
    def __init__(self, api_client):
        self.api_client = api_client

    def get_global_folder(self):
        '''
        Get all items with 'view' permission.
        '''
        base_uri = "v2/content/folders/global"
        async_job_id = self.api_client.get(base_uri).json()['id']

        # workaround for 500 error on status request
        import time
        time.sleep(3)
        uri = "{0}/{1}/status".format(base_uri, async_job_id)
        _async_job.wait_for_job(self.api_client, uri)

        uri = "{0}/{1}/result".format(base_uri, async_job_id)
        rsp = self.api_client.get(uri).json()
        return rsp['data']

    def get_personal_folder(self):
        '''
        Get the 'personal' folder.
        '''
        uri = "v2/content/folders/personal"
        return self.api_client.get(uri).json()

    def get_folder(self, folder_id):
        '''
        Get folder with the given folder_id.
        '''
        uri = "v2/content/folders/{0}".format(folder_id)
        return self.api_client.get(uri).json()
