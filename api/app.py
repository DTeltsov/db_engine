from aiohttp import web
from .routes import init_routes
from .db_utils import setup_db
from aiohttp_swagger import setup_swagger


def create_app():
    app = web.Application()
    init_routes(app)
    setup_db(app)
    setup_swagger(app, swagger_url="/api/v1/doc", ui_version=3)
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app)
