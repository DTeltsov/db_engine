from .views import (
    get_dbs,
    add_db,
    get_db,
    delete_db,
    add_table,
    get_table,
    delete_table,
    put_table,
    add_column,
    delete_column,
    put_column,
    add_row,
    delete_row,
    put_row
)


def init_routes(app):
    add_route = app.router.add_route

    add_route('GET', '/api/dbs', get_dbs, name='dbs')
    add_route('GET', '/api/db/{db_name}', get_db, name='db')
    add_route('POST', '/api/db', add_db, name='new-db')
    add_route('DELETE', '/api/db/{db_name}', delete_db, name='delete-db')
    add_route('GET', '/api/db/{db_name}/table/{table_name}', get_table, name='table')
    add_route('POST', '/api/db/{db_name}/table', add_table, name='new-table')
    add_route('DELETE', '/api/db/{db_name}/table/{table_name}', delete_table, name='delete-table')
    add_route('PUT', '/api/db/{db_name}/table/{table_name}', put_table, name='update-table')
    add_route('POST', '/api/db/{db_name}/table/{table_name}/column', add_column, name='new-column')
    add_route('DELETE', '/api/db/{db_name}/table/{table_name}/column/{column_name}', delete_column, name='delete-column')
    add_route('PUT', '/api/db/{db_name}/table/{table_name}/column/{column_name}', put_column, name='update-column')
    add_route('POST', '/api/db/{db_name}/table/{table_name}/row', add_row, name='new-row')
    add_route('DELETE', '/api/db/{db_name}/table/{table_name}/row/{row_pk}', delete_row, name='delete-row')
    add_route('PUT', '/api/db/{db_name}/table/{table_name}/row/{row_pk}', put_row, name='update-row')


