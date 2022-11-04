from .views import (
    get_dbs,
    add_db,
    get_db,
    delete_db,
    add_table,
    get_table,
    delete_table,
    add_column
)


def init_routes(app):
    add_route = app.router.add_route

    add_route('GET', '/dbs', get_dbs, name='dbs')
    add_route('GET', '/db/{db_name}', get_db, name='db')
    add_route('POST', '/db', add_db, name='new-db')
    add_route('DELETE', '/db/{db_name}', delete_db, name='delete-db')
    add_route('GET', '/db/{db_name}/table/{table_name}', get_table, name='table')
    add_route('POST', '/db/{db_name}/table', add_table, name='new-table')
    add_route('DELETE', '/db/{db_name}/table/{table_name}', delete_table, name='delete-table')
    add_route('POST', '/db/{db_name}/table/{table_name}/column', add_column, name='new-column')

