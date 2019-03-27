from api_client import parser, client, content


parser.add_argument('path', type=str, help="Path of content")
args = parser.parse_args()

api_client = client.ApiClient(args.access_id, args.access_key, args.endpoint)
content_api = content.ContentManagementApi(api_client)
print(content_api.find_id_by_path(args.path))
