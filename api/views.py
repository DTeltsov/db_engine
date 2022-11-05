from aiohttp import web
from .db_utils import (
    create_db,
    load_db_paths,
    load_db,
    load_table,
    remove_db,
    create_table,
    remove_table,
    update_table,
    union_tables,
    create_column,
    remove_column,
    update_column,
    create_row,
    remove_row,
    update_row
)
from aiohttp_swagger import swagger_path
from .serializers import serialize_db, serialize_table, serialize_dbs
from .utils import handle_json_error


@swagger_path("api/swagger/db/get_dbs.yaml")
@handle_json_error
async def get_dbs_view(request):
    dbs = await load_db_paths()

    data = serialize_dbs(dbs)
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


@swagger_path("api/swagger/db/get.yaml")
@handle_json_error
async def get_db_view(request):
    conn = request.app['db']
    db = request.match_info['db_name']
    await load_db(db, conn)

    data = serialize_db(conn.db)
    tables_hrefs = [{
            'self': {'href': str(request.url) + '/table/' + i['table_name']},
            'delete_table': {
                'href': str(request.url) + '/table/' + i['table_name']
            },
            'put_table': {
                'href': str(request.url) + '/table/' + i['table_name']
            }
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


@swagger_path("api/swagger/db/post.yaml")
@handle_json_error
async def add_db_view(request):
    conn = request.app['db']
    data = await request.json()
    db = await create_db(data, conn)
    name = data['name']

    data = serialize_db(db)
    response = {
        'status': 'ok',
        'data': data,
        'links': {
            'self': {'href': str(request.url) + '/' + name},
            'add_table': {'href': str(request.url) + '/' + name + '/table'},
            'delete_db': {'href': str(request.url) + '/' + name}
        }}

    return web.json_response(response, status=201)


@swagger_path("api/swagger/db/delete.yaml")
@handle_json_error
async def delete_db_view(request):
    conn = request.app['db']
    name = request.match_info['db_name']
    await remove_db(name, conn)

    response = {
        'status': 'ok',
        'links': {
            'dbs': {'href': str(request.url) + '/' + name}
        }}

    return web.json_response(response, status=200)


@swagger_path("api/swagger/table/get.yaml")
@handle_json_error
async def get_table_view(request):
    conn = request.app['db']
    db = request.match_info['db_name']
    table = request.match_info['table_name']
    data = await load_table(db, table, conn)

    data = serialize_table(data)
    columns_hrefs = [{
        'delete_column': {
            'href': str(request.url) + '/column/' + i['column_name']
        },
        'put_column': {
            'href': str(request.url) + '/column/' + i['column_name']
        }
        } for i in data['columns']]
    rows_hrefs = [{
        'delete_row': {'href': str(request.url) + '/row/' + str(i['pk'])},
        'put_row': {'href': str(request.url) + '/row/' + str(i['pk'])}
        } for i in data['rows']]
    response = {
        'status': 'ok',
        'data': data,
        'links': {
            'self': {
                'delete_table': {'href': str(request.url)},
                'put_table': {'href': str(request.url)},
                'add_column': {'href': str(request.url) + '/column'},
                'add_row': {'href': str(request.url) + '/row'}
            },
            'columns': columns_hrefs,
            'rows': rows_hrefs
        }}

    return web.json_response(response, status=200)


@swagger_path("api/swagger/table/post.yaml")
@handle_json_error
async def add_table_view(request):
    conn = request.app['db']
    data = await request.json()
    db = request.match_info['db_name']
    data = await create_table(db, data, conn)

    data = serialize_table(data)
    table = data['table_name']
    response = {
        'status': 'ok',
        'data': data,
        'links': {
            'self': {'href': str(request.url) + '/' + table},
            'add_column': {'href': str(request.url) + '/' + table + '/column'},
            'delete_table': {'href': str(request.url) + '/' + table}
        }}

    return web.json_response(response, status=201)


@swagger_path("api/swagger/table/delete.yaml")
@handle_json_error
async def delete_table_view(request):
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


@swagger_path("api/swagger/table/put.yaml")
@handle_json_error
async def put_table_view(request):
    conn = request.app['db']
    db = request.match_info['db_name']
    table = request.match_info['table_name']
    data = await request.json()
    await update_table(db, table, data, conn)

    response = {
        'status': 'ok',
        'links': {
            'db': {'href': str(request.url)}
        }}

    return web.json_response(response, status=201)


@swagger_path("api/swagger/table/union.yaml")
@handle_json_error
async def union_tables_view(request):
    conn = request.app['db']
    db = request.match_info['db_name']
    table1 = request.match_info['table_name1']
    table2 = request.match_info['table_name2']
    result_table = await union_tables(db, table1, table2, conn)

    data = serialize_table(result_table)
    response = {
        'status': 'ok',
        'data': data
    }

    return web.json_response(response, status=201)


@swagger_path("api/swagger/column/post.yaml")
@handle_json_error
async def add_column_view(request):
    conn = request.app['db']
    db = request.match_info['db_name']
    table = request.match_info['table_name']
    data = await request.json()
    await create_column(db, table, data, conn)

    response = {
        'status': 'ok',
        'links': {
            'table': {'href': str(request.url).replace('/column', '')}
        }}

    return web.json_response(response, status=201)


@swagger_path("api/swagger/column/delete.yaml")
@handle_json_error
async def delete_column_view(request):
    conn = request.app['db']
    db = request.match_info['db_name']
    table = request.match_info['table_name']
    column = request.match_info['column_name']
    await remove_column(db, table, column, conn)

    response = {
        'status': 'ok',
        'links': {
            'table': {
                'href': str(request.url).replace('/column/' + column, '')
            }
        }}

    return web.json_response(response, status=201)


@swagger_path("api/swagger/column/put.yaml")
@handle_json_error
async def put_column_view(request):
    conn = request.app['db']
    db = request.match_info['db_name']
    table = request.match_info['table_name']
    column = request.match_info['column_name']
    data = await request.json()
    await update_column(db, table, column, data, conn)

    response = {
        'status': 'ok',
        'links': {
            'table': {
                'href': str(request.url).replace('/column/' + column, '')
            }
        }}

    return web.json_response(response, status=201)


@swagger_path("api/swagger/row/post.yaml")
@handle_json_error
async def add_row_view(request):
    conn = request.app['db']
    data = await request.json()
    db = request.match_info['db_name']
    table = request.match_info['table_name']
    await create_row(db, table, data, conn)

    response = {
        'status': 'ok',
        'links': {
            'table': {'href': str(request.url).replace('/row', '')}
        }}

    return web.json_response(response, status=201)


@swagger_path("api/swagger/row/delete.yaml")
@handle_json_error
async def delete_row_view(request):
    conn = request.app['db']
    db = request.match_info['db_name']
    table = request.match_info['table_name']
    row = int(request.match_info['row_pk'])
    await remove_row(db, table, row, conn)

    response = {
        'status': 'ok',
        'links': {
            'table': {'href': str(request.url).replace('/row/' + str(row), '')}
        }}

    return web.json_response(response, status=201)


@swagger_path("api/swagger/row/delete.yaml")
@handle_json_error
async def put_row_view(request):
    conn = request.app['db']
    db = request.match_info['db_name']
    table = request.match_info['table_name']
    row = int(request.match_info['row_pk'])
    data = await request.json()
    await update_row(db, table, row, data, conn)

    response = {
        'status': 'ok',
        'links': {
            'table': {'href': str(request.url).replace('/row/' + str(row), '')}
        }}

    return web.json_response(response, status=201)
