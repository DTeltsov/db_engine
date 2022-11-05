from db.db import DBManager
import os
import json
from db.exceptions import InvalidValueError


def check_db(db_name, conn):
    if conn.db.name != db_name:
        location = db_name + '.json'
        conn.load_db(location)


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


async def create_db(data, conn):
    try:
        db_name = data['name']
    except KeyError:
        raise InvalidValueError(data)
    db = conn.create_db(db_name)
    await add_db_path(db_name)
    return db


async def remove_db(data, conn):
    try:
        db_name = data['name']
    except KeyError:
        raise InvalidValueError(data)
    conn.delete_db(db_name)
    await delete_db_path(db_name)


async def load_table(db_name, db_table, conn):
    check_db(db_name, conn)
    table = conn.get_table(db_table)
    return table


async def create_table(db_name, data, conn):
    check_db(db_name, conn)
    try:
        table_name = data['name']
    except KeyError:
        raise InvalidValueError(data)
    table = conn.add_table(table_name)
    conn.save_db()
    return table


async def remove_table(db_name, table_name, conn):
    check_db(db_name, conn)
    conn.delete_table(table_name)
    conn.save_db()


async def update_table(db_name, table_name, data, conn):
    check_db(db_name, conn)
    table = conn.get_table(table_name)
    try:
        name = data['name']
    except KeyError:
        raise InvalidValueError(data)
    table.update_table(name)
    conn.save_db()


async def create_column(db_name, table_name, data, conn):
    check_db(db_name, conn)
    table = conn.get_table(table_name)
    try:
        name, attr, is_null = data['name'], data['attr'], data['is_null']
    except KeyError:
        raise InvalidValueError(data)
    try:
        default_value = data['default_value']
    except KeyError:
        default_value = None
    table.add_column(name, attr, is_null, default_value)
    conn.save_db()


async def remove_column(db_name, table_name, column_name, conn):
    check_db(db_name, conn)
    table = conn.get_table(table_name)
    table.delete_column(column_name)
    conn.save_db()


async def update_column(db_name, table_name, data, conn):
    check_db(db_name, conn)
    table = conn.get_table(table_name)
    try:
        name, attr, is_null = data['name'], data['attr'], data['is_null']
    except KeyError:
        raise InvalidValueError(data)
    table.update_column(name, name, attr, is_null)
    conn.save_db()


async def create_row(db_name, table_name, values, conn):
    check_db(db_name, conn)
    table = conn.get_table(table_name)
    table.add_row(values)
    conn.save_db()


async def remove_row(db_name, table_name, row_index, conn):
    check_db(db_name, conn)
    table = conn.get_table(table_name)
    table.delete_row(row_index)
    conn.save_db()


async def update_row(db_name, table_name, row_index, values, conn):
    check_db(db_name, conn)
    table = conn.get_table(table_name)
    table.update_row(row_index, values)
    conn.save_db()


def setup_db(app):
    db = DBManager()
    app['db'] = db
