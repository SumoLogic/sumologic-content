import json
from api_client import parser, client, content, permission
from util import pretty_print, read_json_file


parser.add_argument('path', type=str, help="Path to content")
parser.add_argument('action', type=str, help="Get, add, or remove permissions",
                    choices=['get', 'add', 'remove'])
parser.add_argument('--data_file', '-d', type=str,
                    help="File to read permission from when adding or removing permissions")
args = parser.parse_args()

api_client = client.ApiClient(args.access_id, args.access_key, args.endpoint)
content_api = content.ContentManagementApi(api_client)
permissions_api = permission.ContentPermissionApi(api_client)

content_id = content_api.find_id_by_path(args.path)
if args.action == 'get':
    permissions = permissions_api.get_permissions(content_id)
    pretty_print(permissions['explicitPermissions'])
else:
    permissions = read_json_file(args.data_file)
    body = {
        'contentPermissionAssignments': permissions,
        'notifyRecipients': False,
        'notificationMessage': ""
    }
    if args.action == 'add':
        permissions_api.add_permissions(content_id, body)
    elif args.action == 'remove':
        permissions_api.remove_permissions(content_id, body)
