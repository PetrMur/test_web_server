import aiomysql
import traceback
from typing import Tuple
from app.utils.logger import Logger
from app.utils.singleton import Singleton
from settings.credentials import MYSQL_CREDENTIALS


def db_query_error_handler(coroutine):
    async def wrapped(client, query: str, args):
        try:
            return await coroutine(client, query, args)
        except Exception as e:
            Logger().error('db error')
            Logger().error(f'{query}')
            Logger().error(traceback.format_exc())
            try:
                await MysqlClient().create_pool()
                return await coroutine(client, query, args)
            except Exception:
                Logger().error('2 bad attempt')
                Logger().error(traceback.format_exc())
    return wrapped


class MysqlClient(metaclass=Singleton):
    USER = MYSQL_CREDENTIALS['user']
    PASSWORD = MYSQL_CREDENTIALS['password']
    HOST = MYSQL_CREDENTIALS['host']
    DATABASE = MYSQL_CREDENTIALS['database']
    PORT = int(MYSQL_CREDENTIALS['port'])

    def __init__(self):
        self.logger = Logger()
        self.db_connection = None
        self.db_cur = None
        self.pool = None

    async def create_pool(self) -> None:
        if self.pool is None:
            self.pool = await aiomysql.create_pool(host=self.HOST, port=self.PORT,
                                                   user=self.USER, password=self.PASSWORD,
                                                   db=self.DATABASE, minsize=5, maxsize=15)

    @db_query_error_handler
    async def query_select_one(self, query, args) -> Tuple:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, args)
                result = await cursor.fetchone()
                await conn.commit()
                return result

    @db_query_error_handler
    async def query_insert(self, query, args) -> Tuple:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, args)
                await conn.commit()
                return cursor.lastrowid

    @db_query_error_handler
    async def query_update_one(self, query, args) -> Tuple:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, args)
                await conn.commit()
                return cursor.lastrowid

    @db_query_error_handler
    async def query_delete(self, query, args) -> Tuple:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, args)
                await conn.commit()
                return cursor.lastrowid

    async def close(self) -> None:
        if not self.db_connection.closed:
            await self.db_cur.close()
            await self.db_connection.close()

    async def close_pool(self) -> None:
        self.pool.close()
        await self.pool.wait_closed()

    async def commit(self) -> None:
        await self.db_connection.commit()

    async def rollback(self) -> None:
        await self.db_connection.rollback()
