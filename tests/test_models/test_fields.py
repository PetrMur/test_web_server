import unittest
from app.models.field_types import SmallStringFIO, SmallString, Email, PhoneNumber


class TestFields(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.small_string_fio = SmallStringFIO('Иван')
        cls.bad_char_small_string_fio = SmallStringFIO('Иван1')
        cls.too_long_small_string_fio = SmallStringFIO('ф'*51)
        cls.small_string = SmallString('Hello')
        cls.too_long_small_string = SmallString('l'*51)
        cls.email = Email('pmurygin1511@gmail.com')
        cls.phone_number = PhoneNumber('78007773535')
        cls.incorrect_phone_number = PhoneNumber('82342342323')

    def test_field(self):
        pass

    def test_correct_small_string(self):
        self.assertTrue(self.small_string.is_correct())
        self.assertFalse(self.too_long_small_string.is_correct())

    def test_correct_small_string_fio(self):
        self.assertTrue(self.small_string_fio.is_correct())
        self.assertFalse(self.bad_char_small_string_fio.is_correct())
        self.assertFalse(self.too_long_small_string_fio.is_correct())

    def test_correct_phone_number(self):
        self.assertTrue(self.phone_number.is_correct())
        self.assertFalse(self.incorrect_phone_number.is_correct())

    def test_correct_email(self):
        self.assertTrue(self.email.is_correct())
