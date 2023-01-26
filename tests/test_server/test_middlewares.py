import json
import unittest
from app.utils.exceptions import ServerException
from app.utils.outgoing_response import Response
from app.server.middlewares.error_handler import error_handler_middleware
from app.server.middlewares.prepare_response import prepare_response_middleware


test_data = {'test': True}


async def mock_handler_error(req):
    raise ServerException


async def mock_handler_response(req):
    return Response().as_json_data(test_data)


class TestMiddlewares(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.req = None

    async def test_error_handler(self):
        result = await error_handler_middleware(self.req, mock_handler_error)
        self.assertEqual(result.status_code, ServerException.status_code)

    async def test_prepare_response(self):
        result = await prepare_response_middleware(self.req, mock_handler_response)
        self.assertEqual(result.text, json.dumps(test_data))
        self.assertEqual(result.status, 200)
