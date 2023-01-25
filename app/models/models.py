from abc import ABC
from app.models.field_types import PhoneNumber, SmallString, Email, SmallStringFIO


class AbstractModel(ABC):
    _required = tuple()

    def __init__(self, fields):
        self._fields = {}
        for name, value in fields.items():
            if hasattr(self.__class__, name):
                self._fields[name] = getattr(self.__class__, name)(value, name in self._required)

    @property
    def get_fields(self):
        return self._fields

    @property
    def get_required(self):
        return self._required

    @classmethod
    def create_object(cls, fields):
        return cls(fields)


class SaveUserData(AbstractModel):
    name = SmallStringFIO
    surname = SmallStringFIO
    patronymic = SmallStringFIO
    phone_number = PhoneNumber
    email = Email
    country = SmallString

    _required = ('name', 'surname', 'phone_number', 'country')


class GetUserData(AbstractModel):
    phone_number = PhoneNumber

    _required = ('phone_number', )


class DeleteUserData(AbstractModel):
    phone_number = PhoneNumber

    _required = ('phone_number', )
