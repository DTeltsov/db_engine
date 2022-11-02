from aiohttp import web
from .db_utils import create_db, load_db_paths, load_db, load_table, remove_db
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
    hrefs = [
        {
            'href': str(request.url).replace('dbs', 'db/' + i['name'])
        } for i in data
    ]
    response = {
        'status': 'ok',
        'data': data,
        'links': {
            'dbs': hrefs,
            'add_db': str(request.url).replace('dbs', 'db'),
            'delete_db': str(request.url).replace('dbs', 'db')
        }
    }
    return web.json_response(response, status=200)


@handle_json_error
async def post_db(request):
    conn = request.app['db']
    data = await request.json()
    name = data['name']
    data = await create_db(name, conn)
    response = {
        'status': 'ok',
        'data': data,
        'links': {
            'self': {
                'href': str(request.url) + '/' + name
            },
            'add_table': {
                'href': str(request.url) + '/' + name + '/table'
            }
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
            'dbs': {
                'href': str(request.url) + '/' + name
            }}}
    return web.json_response(response, status=201)


@handle_json_error
async def get_db(request):
    conn = request.app['db']
    db = request.match_info['db_name']
    data = await load_db(db, conn)
    tables_hrefs = [
        {
            'href': str(request.url) + '/table/' + i['table_name']
        } for i in data['tables']
    ]
    response = {
        'status': 'ok',
        'data': data,
        'links': {
            'self': {
                'add_table': str(request.url) + '/table'
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
    response = {
        'status': 'ok',
        'data': data,
        'links': {
            'self': {
                'href': str(request.url)
            }
        }}
    return web.json_response(response, status=200)
