import os
import logging
import traceback
from types import FunctionType
from app.utils.singleton import Singleton

file = 'web_service.log'


class Logger(metaclass=Singleton):
    def __init__(self, lvl=logging.INFO):
        self.lvl = lvl
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())
        if file not in os.listdir():
            open(file, 'w+')
        logger_handler = logging.FileHandler(file)
        self.logger.addHandler(logger_handler)

    def error(self, text: str):
        self.logger.error(text)

    def info(self, text: str):
        self.logger.info(text)


def start_logging(func: FunctionType):
    """Wraps function with error log"""

    def wrapper():
        try:
            func()
        except Exception as e:
            Logger().error(traceback.format_exc())
            Logger().error(f'{e}')
    return wrapper
