import unittest
from app.models.field_types import Email
from app.models.models import AbstractModel
from app.utils.incoming_request import IncomingRequest


class TestModel(AbstractModel):
    email = Email
    _required = ('email', )


class TestIncomingRequest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = {'email': 'pmurygin1511@gmail.com'}
        scheme = TestModel
        cls.incoming_request = IncomingRequest(cls.data, scheme)

    def test_request_fields(self):
        self.assertEqual(self.incoming_request.fields.keys(), self.data.keys())
        self.assertEqual(self.incoming_request.model.__class__, TestModel)

    def test_disabled_validation(self):
        IncomingRequest({}, TestModel, need_validation=False)
