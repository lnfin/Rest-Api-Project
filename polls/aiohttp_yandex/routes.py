from views import load_couriers, couriers


def setup_routes(app):
    app.router.add_post('/couriers', load_couriers)
    app.router.add_patch(r'/couriers/{id:\d+}', couriers)
