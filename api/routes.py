from .views import (
    get_dbs_view,
    add_db_view,
    get_db_view,
    delete_db_view,
    add_table_view,
    get_table_view,
    delete_table_view,
    put_table_view,
    union_tables_view,
    add_column_view,
    delete_column_view,
    put_column_view,
    add_row_view,
    delete_row_view,
    put_row_view
)


def init_routes(app):
    add_route = app.router.add_route

    # all db related routes
    add_route('GET', '/api/dbs', get_dbs_view, name='dbs')
    add_route('GET', '/api/db/{db_name}', get_db_view, name='db')
    add_route('POST', '/api/db', add_db_view, name='new-db')
    add_route('DELETE', '/api/db/{db_name}', delete_db_view, name='delete-db')

    # all table related routes
    add_route(
        'GET', '/api/db/{db_name}/table/{table_name}',
        get_table_view, name='table'
    )
    add_route(
        'POST', '/api/db/{db_name}/table',
        add_table_view, name='new-table'
    )
    add_route(
        'DELETE', '/api/db/{db_name}/table/{table_name}',
        delete_table_view, name='delete-table'
    )
    add_route(
        'PUT', '/api/db/{db_name}/table/{table_name}',
        put_table_view, name='update-table'
    )
    add_route(
        'GET', '/api/db/{db_name}/table/{table_name1}/union/{table_name2}',
        union_tables_view, name='union-tables'
    )

    # all column related routes
    add_route(
        'POST', '/api/db/{db_name}/table/{table_name}/column',
        add_column_view, name='new-column'
    )
    add_route(
        'DELETE', '/api/db/{db_name}/table/{table_name}/column/{column_name}',
        delete_column_view, name='delete-column'
    )
    add_route(
        'PUT', '/api/db/{db_name}/table/{table_name}/column/{column_name}',
        put_column_view, name='update-column'
    )

    # all row related routes
    add_route(
        'POST', '/api/db/{db_name}/table/{table_name}/row',
        add_row_view, name='new-row'
    )
    add_route(
        'DELETE', '/api/db/{db_name}/table/{table_name}/row/{row_pk}',
        delete_row_view, name='delete-row'
    )
    add_route(
        'PUT', '/api/db/{db_name}/table/{table_name}/row/{row_pk}',
        put_row_view, name='update-row'
    )
