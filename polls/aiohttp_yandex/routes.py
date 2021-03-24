from views import load_couriers, patch_couriers, load_orders, assign_orders


def setup_routes(app):
    app.router.add_post('/couriers', load_couriers)
    app.router.add_patch('/couriers/{id:\d+}', patch_couriers)
    app.router.add_post('/orders', load_orders)
    app.router.add_post('/orders/assign', assign_orders)
