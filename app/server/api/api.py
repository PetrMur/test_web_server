from aiohttp import web
from app.utils.dadata import Dadata
from app.utils.exceptions import NotFoundError
from app.utils.outgoing_response import Response
from app.utils.mysql_manager import MysqlManager
from app.utils.incoming_request import IncomingRequest
from app.models.models import SaveUserData, GetUserData, DeleteUserData


class MainAPI:
    @classmethod
    async def save_user_data(cls, request: web.Request):
        """
        Save new user or update existed

        :param request:
        :return:
        """

        body = await request.post()
        incoming_request = IncomingRequest(body, SaveUserData)
        surname = incoming_request.fields.get('surname').value
        name = incoming_request.fields.get('name').value
        phone = incoming_request.fields.get('phone_number').value
        patronymic = incoming_request.fields['email'].value if incoming_request.fields.get('email') else None
        email = incoming_request.fields['email'].value if incoming_request.fields.get('email') else None

        country_code = await Dadata.get_country_data(incoming_request.fields.get('country').value)

        if await MysqlManager.select_user_by_phone(request.app['db'], ['id'], phone):
            params = [name, surname, patronymic, phone, email, incoming_request.fields['country'].value, country_code]
            await MysqlManager.update_user_by_phone(request.app['db'], params, phone)
            return Response().as_json_data(f"Updated user {name} {surname} with phone {phone}")

        else:
            params = [name, surname, patronymic, phone, email, incoming_request.fields['country'].value, country_code]
            await MysqlManager.insert_new_user(request.app['db'], params)
            return Response().as_json_data(f"Created user {name} {surname} with phone {phone}")

    @classmethod
    async def get_user_data(cls, request: web.Request):
        """
        Get user from DB

        :param request:
        :return:
        """

        body = await request.post()
        incoming_request = IncomingRequest(body, GetUserData)
        phone = incoming_request.fields.get('phone_number').value

        needed = ['name', 'surname', 'patronymic', 'phone_number', 'email', 'country', 'country_code']

        result = await MysqlManager.select_user_by_phone(request.app['db'], needed, phone)
        if result:
            result_dict = {needed[i]: result[i] for i in range(len(needed))}
            return Response().as_json_data(result_dict)
        else:
            raise NotFoundError(f'User with phone {phone} not found')

    @classmethod
    async def delete_user_data(cls, request: web.Request):
        """
        Delete user from DB

        :param request:
        :return:
        """

        body = await request.post()
        incoming_request = IncomingRequest(body, DeleteUserData)
        phone = incoming_request.fields.get('phone_number').value

        result = await MysqlManager.select_user_by_phone(request.app['db'], ['name', 'surname'], phone)

        if result:
            await MysqlManager.delete_user_by_phone(request.app['db'], phone)
            return Response().as_json_data(f'Deleted user {result[0]} {result[1]} with phone {phone}')
        else:
            raise NotFoundError(f'User with phone {phone} not found')
