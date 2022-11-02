from aiohttp import web
from routes import init_routes


def setup_app(app):
    init_routes(app)


if __name__ == '__main__':
    app = web.Application()
    setup_app(app)
    web.run_app(app)
