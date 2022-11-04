from aiohttp import web
from .db_utils import (
    create_db,
    load_db_paths,
    load_db,
    load_table,
    remove_db,
    create_table,
    remove_table,
    create_column
)
from .serializers import serialize_db, serialize_table
import asyncio


def handle_json_error(func):
    async def handler(request):
        try:
            return await func(request)
        except asyncio.CancelledError:
            raise
        except Exception as ex:
            return web.json_response(
                {'status': 'failed', 'reason': str(ex)}, status=400
            )

    return handler


@handle_json_error
async def get_dbs(request):
    dbs = await load_db_paths()
    data = [{'name': i['name']} for i in dbs['dbs']]
    hrefs = [{
            'self': {
                'href': str(request.url).replace('dbs', 'db/' + i['name'])
            },
            'delete_db': {
                'href': str(request.url).replace('dbs', 'db/' + i['name'])
            }
        } for i in data]
    response = {
        'status': 'ok',
        'data': data,
        'links': {
            'dbs': hrefs,
            'add_db': str(request.url).replace('dbs', 'db'),
        }}
    return web.json_response(response, status=200)


@handle_json_error
async def add_db(request):
    conn = request.app['db']
    data = await request.json()
    name = data['name']
    data = await create_db(name, conn)
    response = {
        'status': 'ok',
        'data': data,
        'links': {
            'self': {'href': str(request.url) + '/' + name},
            'add_table': {'href': str(request.url) + '/' + name + '/table'},
            'delete_db': {'href': str(request.url) + '/' + name}
        }}
    return web.json_response(response, status=201)


@handle_json_error
async def delete_db(request):
    conn = request.app['db']
    name = request.match_info['db_name']
    await remove_db(name, conn)
    response = {
        'status': 'ok',
        'links': {
            'dbs': {'href': str(request.url) + '/' + name}
        }}
    return web.json_response(response, status=201)


@handle_json_error
async def get_db(request):
    conn = request.app['db']
    db = request.match_info['db_name']
    await load_db(db, conn)
    data = serialize_db(conn.db)
    tables_hrefs = [{
            'self': {'href': str(request.url) + '/table/' + i['table_name']},
            'delete_table': {'href': str(request.url) + '/table/' + i['table_name']}
        } for i in data['tables']]
    response = {
        'status': 'ok',
        'data': data,
        'links': {
            'self': {
                'add_table': {'href': str(request.url) + '/table'},
                'delete_db': {'href': str(request.url)}
            },
            'db_tables': tables_hrefs
        }}
    return web.json_response(response, status=200)


@handle_json_error
async def get_table(request):
    conn = request.app['db']
    db = request.match_info['db_name']
    table = request.match_info['table_name']
    data = await load_table(db, table, conn)
    data = serialize_table(data)
    response = {
        'status': 'ok',
        'data': data,
        'links': {
            'self': {
                'delete_table': {'href': str(request.url)},
                'add_column': {'href': str(request.url) + '/column'}
            },
            'columns': {
                'delete_column': {'href': str(request.url)}
            }
        }}
    return web.json_response(response, status=200)


@handle_json_error
async def add_table(request):
    conn = request.app['db']
    data = await request.json()
    db = request.match_info['db_name']
    table = data['name']
    data = await create_table(db, table, conn)
    data = serialize_table(data)
    response = {
        'status': 'ok',
        'data': data,
        'links': {
            'self': {'href': str(request.url) + '/' + table},
            'add_column': {'href': str(request.url) + '/' + table + '/column'},
            'delete_table': {'href': str(request.url) + '/' + table}
        }}
    return web.json_response(response, status=201)


@handle_json_error
async def delete_table(request):
    conn = request.app['db']
    db = request.match_info['db_name']
    table = request.match_info['table_name']
    await remove_table(db, table, conn)
    response = {
        'status': 'ok',
        'links': {
            'db': {'href': str(request.url).replace('/table/' + table, '')}
        }}
    return web.json_response(response, status=201)


@handle_json_error
async def add_column(request):
    conn = request.app['db']
    data = await request.json()
    name, attr, is_null = data['name'], data['attr'], data['is_null']
    db = request.match_info['db_name']
    table = request.match_info['table_name']
    await create_column(db, table, name, attr, is_null, conn)
    response = {
        'status': 'ok',
        'links': {
            'table': {'href': str(request.url).replace('/column', '')}
        }}
    return web.json_response(response, status=201)
