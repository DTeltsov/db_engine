from .views import db_list


def init_routes(app):
    add_route = app.router.add_route

    add_route('*', '/', db_list, name='index')