from views import index, load_couriers, couriers


def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_post('/couriers', load_couriers)
    app.router.add_patch('/couriers/{id:\d+}', couriers)
