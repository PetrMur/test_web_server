import aioredis
from typing import Union, List
from settings.credentials import REDIS_CREDENTIALS

__all__ = ['RedisClient']


class RedisContextConnection:
    """This is context async manager used to connect redis"""

    def __init__(self):
        self.host: str = REDIS_CREDENTIALS['host']
        self.port: str = REDIS_CREDENTIALS['port']
        self.user: str = REDIS_CREDENTIALS['user']
        self.password: str = REDIS_CREDENTIALS['password']

    async def __aenter__(self):
        self.redis = aioredis.from_url(f'redis://[[{self.user}]:[{self.password}]]@{self.host}:{self.port}') \
            if self.password else aioredis.from_url(f'redis://{self.host}:{self.port}')
        return self.redis.client()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.redis.close()


class RedisClient:
    @classmethod
    async def get_item(cls, key: str) -> List[Union[dict, str]]:
        """Takes object from redis"""

        async with RedisContextConnection() as conn:
            value = await conn.get(key)
            return value

    @classmethod
    async def set_item(cls, pair) -> None:
        """Set new value in redis"""

        async with RedisContextConnection() as conn:
            await conn.set(*pair)
