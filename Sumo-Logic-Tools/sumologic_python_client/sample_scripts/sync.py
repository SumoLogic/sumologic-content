import json
from api_client import parser, client, content
from util import pretty_print, read_json_file


parser.add_argument('folder_path', type=str, help="Path to folder to sync to")
parser.add_argument('data_file', type=str, help="File to read contents from")
args = parser.parse_args()

api_client = client.ApiClient(args.access_id, args.access_key, args.endpoint)
content_api = content.ContentManagementApi(api_client)
folder_id = content_api.find_id_by_path(args.folder_path)
content_item = None
content_item = read_json_file(args.data_file)
content_api.sync(folder_id, content_item)
