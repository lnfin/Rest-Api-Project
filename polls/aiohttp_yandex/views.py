from aiohttp import web
import json


async def index(request):
    response_obj = {'status': 'success'}
    return web.Response(text=json.dumps(response_obj))


async def load_couriers(self, *, loads=json.loads):
    body = await self.text()
    couriers = json.loads(body)
    return loads(body)


async def couriers(request):
    id = request.match_info['id']
    return web.Response(text=f"Hello, {id}")


async def orders(self, *, loads=json.loads):
    body = await self.text()
    orders = json.loads(body)
    return loads(body)