import logging
import unittest
from app.utils.logger import Logger, start_logging


@start_logging
def test_func():
    raise AssertionError


class TestLogger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        lvl = logging.INFO
        cls.logger = Logger(lvl)
        cls.lvl = lvl

    def test_logger(self):
        self.assertEqual(self.logger.lvl, self.lvl)
        test_func()
