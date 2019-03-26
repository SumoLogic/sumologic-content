class ContentPermissionApi:
    '''
    Content Permission Management API.

    Manage permissions on content in your organization’s library.
    '''
    def __init__(self, api_client):
        self.api_client = api_client

    def get_permissions(self, content_id, explicitOnly=True):
        '''
        Get permissions for a content item.
        With explicitOnly set to True (default), only explicit permissions are fetched.
        '''
        uri = "v2/content/%s/permissions" % content_id
        params = {"explicitOnly": explicitOnly}
        return self.api_client.get(uri, params=params).json()

    def add_permissions(self, content_id, permissions):
        '''
        Add permissions to a content item.
        '''
        uri = "v2/content/%s/permissions/add" % content_id
        return self.api_client.put(uri, data=permissions).json()

    def remove_permissions(self, content_id, permissions):
        '''
        Remove permissions from a content item.
        '''
        uri = "v2/content/%s/permissions/remove" % content_id
        return self.api_client.put(uri, data=permissions).json()
