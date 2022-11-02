import os
import json


def load_db_paths():
    if os.path.exists('db/db_paths.json'):
        json_data = json.load(open('db/db_paths.json'))
    else:
        path = os.path.expanduser('db/db_paths.json')
        json_data = {'dbs': []}
        json.dump(json_data, open(path, "w+"))
    return json_data
