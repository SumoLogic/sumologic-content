import json
from api_client import parser, client, content
from util import pretty_print


parser.add_argument('path', type=str, help="Path of content to export")
args = parser.parse_args()

api_client = client.ApiClient(args.access_id, args.access_key, args.endpoint)
content_api = content.ContentManagementApi(api_client)
content_id = content_api.find_id_by_path(args.path)
exported_content = content_api.export(content_id)
pretty_print(exported_content)
