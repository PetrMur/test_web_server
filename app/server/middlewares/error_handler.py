from aiohttp import web
from app.utils.logger import Logger
from app.utils.exceptions import ServerException
from app.utils.outgoing_response import ServerResponse


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

    except ServerException as e:
        Logger().error(f'{e.log_error_text}')
        response = ServerResponse()
        response.make_exception(e.txt, e.status_code)

    return response
