from .views import (
    get_dbs,
    post_db,
    get_db,
    get_table,
    delete_db
)


def init_routes(app):
    add_route = app.router.add_route

    add_route('GET', '/dbs', get_dbs, name='dbs')
    add_route('POST', '/db', post_db, name='new-db')
    add_route('DELETE', '/db/{db_name}', delete_db, name='delete-db')
    add_route('GET', '/db/{db_name}', get_db, name='db')
    add_route('GET', '/db/{db_name}/table/{table_name}', get_table, name='table')