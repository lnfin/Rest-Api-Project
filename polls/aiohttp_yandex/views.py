from db import DB
from aiohttp import web
import json

db = DB()


async def load_couriers(self, *, loads=json.loads):
    body = await self.text()
    couriers = json.loads(body)['data']
    resp, ids = db.add_courier(couriers)
    if resp:
        return web.Response(text=json.dumps({'couriers': ids}), status=201)
    else:
        return web.Response(text=json.dumps({"validation_error": {"couriers": ids}}), status=400)


async def patch_couriers(request):
    body = await request.text()
    courier_id = request.match_info['id']
    resp, info = db.patch_courier(courier_id, json.loads(body))
    if resp:
        return web.Response(text=json.dumps(info), status=200)
    else:
        return web.Response(status=400)


async def load_orders(self, *, loads=json.loads):
    body = await self.text()
    orders = json.loads(body)['data']
    resp, ids = db.add_orders(orders)
    if resp:
        return web.Response(text=json.dumps({'orders': ids}), status=201)
    else:
        return web.Response(text=json.dumps({"validation_error": {"orders": ids}}), status=400)


async def assign_orders(self, *, loads=json.loads):
    body = await self.text()
    id = json.loads(body)['courier_id']
    resp, orders, time = db.assign_orders(id)
    if resp:
        if orders:
            return web.Response(text=json.dumps({"orders": orders, "assign_time": time}), status=200)
        else:
            return web.Response(text=json.dumps({"orders": orders}), status=200)
    else:
        return web.Response(status=400)


async def order_complete(self, *, loads=json.loads):
    body = await self.text()
    req = json.loads(body)
    resp, id = db.complete_order(req)
    if resp:
        return web.Response(text=json.dumps({"order_id": id}), status=200)
    else:
        return web.Response(status=400)


async def get_courier(request):
    courier_id = request.match_info['id']
    resp, info = db.courier_info(courier_id)
    if resp:
        return web.Response(text=json.dumps(info), status=200)
    else:
        return web.Response(status=400)
