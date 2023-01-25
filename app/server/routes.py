from aiohttp import web
from app.server.api.api import MainAPI


routes = [
    (web.post('/get_user_data', MainAPI.get_user_data)),
    (web.post('/save_user_data', MainAPI.save_user_data)),
    (web.post('/delete_user_data', MainAPI.delete_user_data))
]
