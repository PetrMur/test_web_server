import unittest
from unittest.mock import patch
from app.utils.dadata import Dadata
from app.server.api.api import MainAPI
from app.utils.exceptions import NotFoundError


class MockDB:
    def __init__(self, value):
        self.value = value

    async def query_select_one(self, var1, var2):
        return self.value

    async def query_update_one(self, var1, var2):
        pass

    async def query_insert(self, var1, var2):
        pass

    async def query_delete(self, var1, var2):
        pass


class MockRequest:
    def __init__(self, body, value=None):
        self.body = body
        self._app = {'db': MockDB(value)}

    @property
    def app(self):
        return self._app

    async def post(self):
        return self.body


class TestMainAPI(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        body_save = {'name': 'Иван', 'surname': 'Иванов', 'patronymic': 'Иванович', 'phone_number': '70000000000',
                     'email': 'ivan@mail.ru', 'country': 'Россия', 'country_code': '643'}
        body_get_delete = {'phone_number': '70000000000'}
        cls.returned_for_get = ('Иван', 'Иванов', 'Иванович', '70000000000', 'ivan@mail.ru', 'Россия', '643')
        cls.request_for_save_update = MockRequest(body_save, True)
        cls.request_for_save_insert = MockRequest(body_save, False)
        cls.request_for_get = MockRequest(body_get_delete, cls.returned_for_get)
        cls.request_for_get_not_found = MockRequest(body_get_delete, False)
        cls.request_for_delete = MockRequest(body_get_delete, ['Иван', 'Иванов'])
        cls.request_for_delete_not_found = MockRequest(body_get_delete, False)

    async def test_save_user_data_insert(self):
        with patch.object(Dadata, 'get_country_data') as country_code:
            country_code.return_value = '643'
            api_answer = await MainAPI.save_user_data(self.request_for_save_insert)
            self.assertEqual(api_answer._data, 'Created user Иван Иванов with phone 70000000000')

    async def test_save_user_data_update(self):
        with patch.object(Dadata, 'get_country_data') as country_code:
            country_code.return_value = '643'
            api_answer = await MainAPI.save_user_data(self.request_for_save_update)
            self.assertEqual(api_answer._data, 'Updated user Иван Иванов with phone 70000000000')

    async def test_get_user_data(self):
        answer = {'name': 'Иван', 'surname': 'Иванов', 'patronymic': 'Иванович', 'phone_number': '70000000000',
                  'email': 'ivan@mail.ru', 'country': 'Россия', 'country_code': '643'}
        api_answer = await MainAPI.get_user_data(self.request_for_get)
        self.assertEqual(api_answer._data, answer)

    async def test_get_user_data_not_found(self):
        with self.assertRaises(NotFoundError):
            await MainAPI.get_user_data(self.request_for_get_not_found)

    async def test_delete_user_data(self):
        api_answer = await MainAPI.delete_user_data(self.request_for_delete)
        self.assertEqual(api_answer._data, 'Deleted user Иван Иванов with phone 70000000000')

    async def test_delete_user_data_not_found(self):
        with self.assertRaises(NotFoundError):
            await MainAPI.delete_user_data(self.request_for_delete_not_found)
