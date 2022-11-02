import os
import json


def load_db_paths():
    if os.path.exists('db_paths.json'):
        json_data = json.load(open('db_paths.json'))
    else:
        path = os.path.expanduser('db_paths.json')
        json_data = {'dbs': []}
        json.dump(json_data, open(path, "w+"))
    return json_data
