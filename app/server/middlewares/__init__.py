from .error_handler import error_handler_middleware
from .prepare_response import prepare_response_middleware


middlewares = [
    prepare_response_middleware,
    error_handler_middleware,
]
