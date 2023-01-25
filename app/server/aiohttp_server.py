import logging
from aiohttp import web
from .routes import routes
from .middlewares import middlewares
from app.utils.db_clients.mysql_client import MysqlClient

logging.getLogger("aiohttp.access").setLevel(logging.ERROR)


class Server:
    def __init__(self):
        self.app = web.Application(middlewares=middlewares)
        self.app.add_routes(routes)
        self.app.on_startup.append(self.make_db_conn)
        self.app.on_cleanup.append(self.close_db_conn)

    def get_app(self):
        return self.app

    def run(self, host, port):
        web.run_app(self.app, host=host, port=port)

    def crush(self):
        self.app.shutdown()
        self.app.cleanup()

    @staticmethod
    async def make_db_conn(app):
        app['db'] = MysqlClient()
        await app['db'].create_pool()

    @staticmethod
    async def close_db_conn(app):
        await app['db'].close()
