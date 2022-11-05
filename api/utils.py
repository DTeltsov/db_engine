import asyncio
from aiohttp import web
from db.exceptions import NotFoundError, AlredyExistsError, InvalidValueError


def handle_json_error(func):
    async def handler(request):
        try:
            return await func(request)
        except asyncio.CancelledError:
            raise
        except NotFoundError as e:
            return web.json_response(
                {'status': 'failed', 'reason': str(e)}, status=404
            )
        except (AlredyExistsError, InvalidValueError) as e:
            return web.json_response(
                {'status': 'failed', 'reason': str(e)}, status=400
            )
        except Exception as e:
            return web.json_response(
                {
                    'status': 'failed',
                    'reason': 'Internal Server Error',
                    'desc': str(e)
                },
                status=500
            )
    return handler
