from settings.credentials import DADATA
from aiohttp.client import ClientSession
from app.utils.exceptions import NotFoundError
from app.utils.db_clients.redis_client import RedisClient


class Dadata:
    token = DADATA['token']
    secret = DADATA['secret']
    url = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/country'

    @classmethod
    async def get_country_data(cls, country):
        """Get country code from dadata (or cache)"""

        country_code = await RedisClient.get_item(country)
        if not country_code:
            async with ClientSession() as session:
                headers = cls.get_headers()
                data = {"query": country}
                response = await session.post(url=cls.url, headers=headers, json=data)
                response.raise_for_status()
                country_code = await response.json()
                try:
                    country_code = country_code['suggestions'][0]['data']['code']
                except Exception:
                    raise NotFoundError(description=f"Not found county {country}")
            await RedisClient.set_item(country, country_code)
        country_code = country_code if isinstance(country_code, str) else country_code.decode()
        return country_code

    @classmethod
    def get_headers(cls):
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token {cls.token}",
        }
        if cls.secret:
            headers["X-Secret"] = cls.secret
        return headers
