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
    max_len = 50
    description = f'must be less than {max_len} symbols'

    def is_correct(self):
        return isinstance(self.value, str) and len(self.value) <= self.max_len


class SmallStringFIO(Field):
    name = 'small_string_fio'
    max_len = 50
    rule = re.compile(r'^[А-Яа-я\s\-]+$')
    description = f'must be less than {max_len} ' \
                  f'symbols and consist only of cyrillic characters, space characters and dashes'

    def is_correct(self):
        return isinstance(self.value, str) and len(self.value) <= self.max_len and self.rule.search(self.value)


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
