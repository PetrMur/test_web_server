from aiohttp import web
from app.utils.logger import Logger
from app.utils.outgoing_response import Response
from app.utils.exceptions import NotFoundError, ServerException, ValidationError


@web.middleware
async def error_handler_middleware(request: web.Request, handler) -> dict:
    """
    Handle errors

    :param request:
    :param handler:
    :return:
    """

    try:
        response = await handler(request)

    except (ServerException, NotFoundError, ValidationError) as e:
        Logger().error(f'{e.log_error_text}')
        response = Response()
        response.make_exception(e.txt, e.status_code)

    return response
