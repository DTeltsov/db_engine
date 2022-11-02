from db.db import DBManager
import os
import json


async def load_db_paths():
    if os.path.exists('db/db_paths.json'):
        json_data = json.load(open('db/db_paths.json'))
    else:
        path = os.path.expanduser('db/db_paths.json')
        json_data = {'dbs': []}
        json.dump(json_data, open(path, "w+"))
    return json_data


async def add_db_path(db_name):
    if os.path.exists('db/db_paths.json'):
        json_data = json.load(open('db/db_paths.json'))
        json_data['dbs'].append({'name': db_name})
        config_path = os.path.expanduser('db/db_paths.json')
        json.dump(json_data, open(config_path, "w+"))
    else:
        json_data = {'dbs': [{'name': db_name}]}
        config_path = os.path.expanduser('db/db_paths.json')
        json.dump(json_data, open(config_path, "w+"))


async def delete_db_path(db_name):
    json_data = json.load(open('db/db_paths.json'))
    json_data['dbs'] = list(
        filter(lambda db: db['name'] != db_name, json_data['dbs'])
    )
    config_path = os.path.expanduser('db/db_paths.json')
    json.dump(json_data, open(config_path, "w+"))


async def load_db(db_name, conn):
    location = db_name + '.json'
    conn.load_db(location)
    response = conn.db.serialize()
    return response


async def create_db(db_name, conn):
    response = conn.create_db(db_name)
    await add_db_path(db_name)
    return response


async def remove_db(db_name, conn):
    conn.delete_db(db_name)
    await delete_db_path(db_name)


async def load_table(db_name, db_table, conn):
    if conn.db.name != db_name:
        location = db_name + '.json'
        conn.load_db(location)
    table = conn.get_table(db_table)
    response = table.serialize()
    return response


def setup_db(app):
    db = DBManager()
    app['db'] = db
