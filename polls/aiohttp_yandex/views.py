from db import DB
from aiohttp import web
import json

db = DB()


async def load_couriers(self, *, loads=json.loads):
    body = await self.text()
    couriers = json.loads(body)['data']
    resp, ids = db.add_courier(couriers=couriers)
    if resp:
        return web.Response(text=json.dumps({'couriers': ids}), status=201)
    else:
        return web.Response(text=json.dumps({"validation_error": {"couriers": ids}}), status=400)


async def couriers(request):
    courier_id = request.match_info['id']
    return web.Response(text=f"Hello, {courier_id}")


async def orders(self, *, loads=json.loads):
    body = await self.text()
    # orders = json.loads(body)
    return loads(body)
