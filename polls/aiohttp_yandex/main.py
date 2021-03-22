from aiohttp import web
from routes import setup_routes
from settings import config_db

app = web.Application()
setup_routes(app)
app['config'] = config_db
web.run_app(app)
print(app['config'])
