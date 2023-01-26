import unittest
from aioredis import Redis
from unittest.mock import patch
from settings.credentials import REDIS_CREDENTIALS
from app.utils.db_clients.redis_client import RedisClient, RedisContextConnection


value = '1'


async def get_value():
    return value


async def set_value():
    pass


class TestRedis(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.redis_context_collection = RedisContextConnection()
        cls.test_value = value
        cls.test_key = '2'

    def test_redis_creds(self):
        self.assertEqual(REDIS_CREDENTIALS,
                         {'password': self.redis_context_collection.password,
                          'host': self.redis_context_collection.host,
                          'port': self.redis_context_collection.port,
                          'user': self.redis_context_collection.user})

    async def test_redis_set(self):
        with patch.object(Redis, 'set') as set_obj:
            set_obj.return_value = set_value()
            await RedisClient().set_item(self.test_key, self.test_value)

    async def test_redis_get(self):
        with patch.object(Redis, 'get') as get_obj:
            get_obj.return_value = get_value()
            self.assertEqual(self.test_value, await RedisClient().get_item(self.test_key))
