import re
from abc import ABC, abstractmethod


class Field(ABC):
    rule = None
    name = None
    value = None
    description = None
    max_len = None

    def __init__(self, value, is_required: bool = False):
        self.value = value
        self.is_required = is_required

    @abstractmethod
    def is_correct(self):
        pass


class SmallString(Field):
    name = 'small_string'
    description = f'must be less than 50 symbols'

    def is_correct(self):
        return isinstance(self.value, str) and len(self.value) <= 50


class SmallStringFIO(Field):
    name = 'small_string_fio'
    rule = re.compile(r'^[А-Яа-я\s\-]+$')
    description = 'must be less than 50 symbols and consist only of cyrillic characters, space characters and dashes'

    def is_correct(self):
        return isinstance(self.value, str) and len(self.value) <= 50 and self.rule.search(self.value)


class PhoneNumber(Field):
    name = 'phone_number'
    rule = re.compile(r'^7(\d{10})$')
    description = 'must start with 7 and and include 11 digits'

    def is_correct(self):
        return isinstance(self.value, str) and self.rule.search(self.value)


class Email(Field):
    name = 'email'

    def is_correct(self):
        return True


class FieldsTypesEnum:
    small_string = SmallString
    phone_number = PhoneNumber
    email = Email
