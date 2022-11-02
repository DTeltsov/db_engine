from aiohttp import web
from .utils import load_db_paths
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
async def db_list(request):
    dbs = load_db_paths()['dbs']
    data = {'status': 'ok', 'data': dbs}
    return web.json_response(data, status=200)


@handle_json_error
async def create_db(request):
    data = await request.json()
    name = data['name']