import unittest
from app.utils.outgoing_response import Response


class TestResponse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.response = Response()
        cls.text = 'test_exc'
        cls.status_code = 500

    def test_response(self):
        self.response.make_exception(self.text, self.status_code)
        self.assertEqual(self.response.status_code, self.status_code)

        json_resp = self.response.response_as_json()
        self.assertEqual(json_resp.status, self.status_code)
        self.assertEqual(json_resp.body._value.decode(), self.text)
