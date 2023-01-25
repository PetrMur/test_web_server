import unittest
from app.utils.singleton import Singleton


class CheckingSingleton(metaclass=Singleton):
    value: str = None

    def __init__(self, value: str) -> None:
        self.value = value


class TestSingleton(unittest.TestCase):
    @classmethod
    def get_singleton_value(cls, value: str) -> str:
        singleton = CheckingSingleton(value)
        return singleton.value

    def test_singleton(self):
        assert self.get_singleton_value('123'), self.get_singleton_value('456')
