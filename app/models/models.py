from abc import ABC
from app.models.field_types import Field, FieldsTypesEnum, PhoneNumber


class AbstractModel(ABC):
    __fields = {}
    __required = []

    def __init__(self, fields):
        for name, value in fields.items():
            self.__fields[name] = getattr(self.__class__, name)(value, name in self.__required)

    @classmethod
    def get_fields(cls):
        return cls.__fields

    @classmethod
    def create_object(cls, fields):
        return cls(fields)
