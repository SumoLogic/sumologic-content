import json


def pretty_print(item):
    print(json.dumps(item, indent=4, sort_keys=True))


def read_json_file(filename):
    with open(filename) as fd:
        json_data = json.load(fd)
    return json_data
