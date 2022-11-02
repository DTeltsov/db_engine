from aiohttp import web
from .routes import init_routes
from .db_utils import setup_db


def create_app():
    app = web.Application()
    init_routes(app)
    setup_db(app)
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app)
