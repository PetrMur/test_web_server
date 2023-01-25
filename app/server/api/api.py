from aiohttp import web
from app.utils.dadata import Dadata
from app.utils.exceptions import NotFoundError
from app.utils.outgoing_response import Response
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
        query = f"SELECT id FROM user_data2 " \
                f"WHERE phone_number = %s"
        args = (phone, )
        result = await request.app['db'].query_select_one(query, args)

        if result:
            query = f"UPDATE user_data2 " \
                    f"SET name=%s, surname=%s, patronymic=%s, phone_number=%s, email=%s, country=%s, " \
                    f"country_code=%s, date_updated=NOW() " \
                    f"WHERE phone_number = %s"
            args = (name, surname, patronymic, phone, email,
                    incoming_request.fields['country'].value, country_code, phone)
            await request.app['db'].query_update_one(query, args)
            return Response().as_json_data(f"Updated user {name} {surname} with phone {phone}")

        else:
            query = f"INSERT INTO user_data2 (name, surname, patronymic, phone_number, email, country, " \
                    f"country_code, date_created, date_updated) " \
                    f"VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())"
            args = (name, surname, patronymic, phone, email, incoming_request.fields['country'].value, country_code)
            await request.app['db'].query_insert(query, args)
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

        needed = f"name, surname, patronymic, phone_number, email, country, country_code"

        query = f"SELECT {needed} FROM user_data2 " \
                f"WHERE phone_number = %s"
        args = (phone, )
        result = await request.app['db'].query_select_one(query, args)
        if result:
            needed = needed.split(', ')
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

        query = f"SELECT name, surname FROM user_data2 " \
                f"WHERE phone_number = %s"
        args = (phone, )
        result = await request.app['db'].query_select_one(query, args)

        if result:
            query = f"DELETE FROM user_data2 " \
                    f"WHERE phone_number = %s"
            args = (phone, )
            await request.app['db'].query_delete(query, args)
            return Response().as_json_data(f'Deleted user {result[0]} {result[1]} with phone {phone}')
        else:
            raise NotFoundError(f'User with phone {phone} not found')
