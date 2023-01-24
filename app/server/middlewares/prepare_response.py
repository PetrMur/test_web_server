from aiohttp import web
from app.utils.outgoing_response import ServerResponse


@web.middleware
async def prepare_response_middleware(request: web.Request, handler) -> web.Response:
    """
    Prepare response

    :param request:
    :param handler:
    :return:
    """

    response: ServerResponse = await handler(request)

    response: web.Response = response.response_as_json()

    return response
