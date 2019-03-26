from . import folder
from .. import _async_job


class ContentManagementApi:
    '''
    Content Management API.

    Manage content in your organization’s library.
    '''
    def __init__(self, api_client):
        self.folder_api = folder.FolderManagementApi(api_client)
        self.api_client = api_client

    def export(self, content_id):
        '''
        Export content with the given content_id.
        '''
        # submit the job
        base_uri = "v2/content/{0}/export".format(content_id)
        export_job = self.api_client.post(base_uri).json()

        # wait for async job to finish
        uri = "{0}/{1}/status".format(base_uri, export_job['id'])
        _async_job.wait_for_job(self.api_client, uri)
        # fetch the result
        uri = "{0}/{1}/result".format(base_uri, export_job['id'])
        content = self.api_client.get(uri).json()
        return content

    def sync(self, folder_id, content):
        '''
        Sync content inside the folder with the given folder_id.
        '''
        # submit the job
        base_uri = "v2/content/folders/{0}/synchronize".format(folder_id)
        sync_job = self.api_client.post(base_uri, data=content).json()

        # wait for job to finish
        uri = "{0}/{1}/status".format(base_uri, sync_job['id'])
        _async_job.wait_for_job(self.api_client, uri, 1)

    def delete(self, content_id):
        '''
        Delete content with the given content_id.
        '''
        # submit the job
        base_uri = "v2/content/{0}/delete".format(content_id)
        delete_job = self.api_client.delete(base_uri).json()

        # wait for job to finish
        uri = "{0}/{1}/status".format(base_uri, delete_job['id'])
        _async_job.wait_for_job(self.api_client, uri)

    def find_content_by_path(self, path):
        '''
        Find content by path.
        '''
        path_elements = path.split('/')
        path_elements = list(filter(lambda x: x, path_elements))

        # validate path
        if (len(path_elements) == 1):
            raise ValueError("Root folder must be followed by a child")
        if path_elements[0].lower() == 'personal':
            rsp = self.folder_api.get_personal_folder()
        elif path_elements[0].lower() == 'global':
            global_content = self.folder_api.get_global_folder()
            rsp = {'children': global_content}
        else:
            raise ValueError("Root folder must be 'personal' or 'global'")

        # traverse path to find content
        traversed_path = path_elements[0]
        del path_elements[0]
        content = None
        for name in path_elements:
            if content:
                rsp = self.folder_api.get_folder(content['id'])
            content = None
            for child in rsp['children']:
                if child['name'] == name:
                    content = child
            if not content:
                raise ValueError("'{0}' does not exist in '{1}'".format(
                    name, traversed_path))
            traversed_path += "/" + name

        return content

    def find_id_by_path(self, path):
        '''
        Find content identifier by path.
        '''
        content = self.find_content_by_path(path)
        return content['id']
