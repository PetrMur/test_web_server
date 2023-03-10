import unittest
from unittest.mock import patch
from aiohttp import ClientSession
from app.utils.dadata import Dadata
from app.utils.exceptions import NotFoundError
from app.utils.db_clients.redis_client import RedisClient


class MockPost:
    def __init__(self, with_error=False):
        if with_error:
            self.returnable_json = {}
        else:
            self.returnable_json = {
                 "suggestions": [
                   {
                     "data": {
                       "code": "643"
                     }
                   }
                 ]
               }

    def raise_for_status(self):
        pass

    async def json(self):
        return self.returnable_json

    @classmethod
    async def get_mock(cls):
        return cls()

    @classmethod
    async def get_error_mock(cls):
        return cls(True)


class TestDadata(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.dadata = Dadata()
        dadata_with_tokens = Dadata()
        dadata_with_tokens.token = 'token'
        dadata_with_tokens.secret = 'secret'
        cls.dadata_with_tokens = dadata_with_tokens
        cls.test_header = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token "
        }
        cls.test_header_with_tokens = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token token",
            "X-Secret": "secret"
        }

    async def test_get_country_data_got_from_redis(self):
        with patch.object(RedisClient, 'get_item') as country_code:
            country_code.return_value = '643'
            code = await Dadata.get_country_data('Россия')
            self.assertEqual(code, '643')

        with patch.object(RedisClient, 'get_item') as country_code, patch.object(RedisClient, 'set_item'), \
                patch.object(ClientSession, 'post') as post_data:
            post_data.return_value = MockPost.get_mock()
            country_code.return_value = None
            code = await Dadata.get_country_data('Россия')
            self.assertEqual(code, '643')

        with patch.object(RedisClient, 'get_item') as country_code, patch.object(RedisClient, 'set_item'), \
                patch.object(ClientSession, 'post') as post_data:
            post_data.return_value = MockPost.get_error_mock()
            country_code.return_value = None
            with self.assertRaises(NotFoundError):
                await Dadata.get_country_data('Россия')

    def test_get_headers(self):
        self.assertEqual(self.test_header, self.dadata.get_headers())
