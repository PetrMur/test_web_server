import unittest
from unittest.mock import patch
from app.utils.dadata import Dadata
from app.utils.db_clients.redis_client import RedisClient


class TestDadata(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.dadata = Dadata()

    async def test_get_country_data_got_from_redis(self):
        with patch.object(RedisClient, 'get_item') as country_code:
            country_code.return_value = '643'
            code = await Dadata.get_country_data('Россия')
            self.assertEqual(code, '643')
