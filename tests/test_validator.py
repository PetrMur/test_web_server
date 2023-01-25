import unittest
from app.validator import Validator
from app.utils.exceptions import ValidationError
from app.models.field_types import SmallStringFIO


class TestValidator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fields_with_name = {
            'name': SmallStringFIO('Иван')
        }
        fields_with_surname = {
            'surname': SmallStringFIO('Иванов')
        }
        fields_with_error = {
            'name': SmallStringFIO('Иван1')
        }

        required_name = ('name', )
        cls.validator = Validator(fields_with_name, required_name)
        cls.validator_with_req_exc = Validator(fields_with_surname, required_name)
        cls.validator_with_exc = Validator(fields_with_error, required_name)

    def test_check_required_fields(self):
        self.validator.check_required_fields()

    def test_check_required_with_exceptions(self):
        self.assertRaises(ValidationError, self.validator_with_req_exc.check_required_fields)

    def test_check_validate_fields(self):
        self.validator.check_required_fields()

    def test_check_validate_fields_with_exc(self):
        self.assertRaises(ValidationError, self.validator_with_exc.validate_fields)
