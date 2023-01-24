import re
from abc import ABC, abstractmethod


class Field(ABC):
    rule = None

    def __init__(self, value, is_required: bool = False):
        self.value = value
        self.is_required = is_required

    @abstractmethod
    def is_correct(self):
        pass


class SmallString(Field):
    def is_correct(self):
        return isinstance(self.value, str) and len(self.value) <= 50


class PhoneNumber(Field):
    rule = re.compile(r'7(\d{10})')

    def is_correct(self):
        return isinstance(self.value, str) and self.rule.search(self.value)


class Email(Field):
    def is_correct(self):
        return True


class FieldsTypesEnum:
    small_string = SmallString
    phone_number = PhoneNumber
    email = Email
