from views import load_couriers, patch_couriers, load_orders, \
    assign_orders, order_complete, get_courier


def setup_routes(app):
    app.router.add_post('/couriers', load_couriers)
    app.router.add_patch(r'/couriers/{id:\d+}', patch_couriers)
    app.router.add_post('/orders', load_orders)
    app.router.add_post('/orders/assign', assign_orders)
    app.router.add_post('/orders/complete', order_complete)
    app.router.add_get(r'/couriers/{id:\d+}', get_courier)
