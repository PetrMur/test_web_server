from typing import List
from app.utils.db_clients.mysql_client import MysqlClient


class MysqlManager:
    @classmethod
    async def select_user_by_phone(cls, db: MysqlClient, needed: List[str], phone: str):
        """Get needed user data by phone"""

        query = f"SELECT {', '.join(needed)} FROM user_data " \
                f"WHERE phone_number = %s"
        args = (phone,)
        return await db.query_select_one(query, args)

    @classmethod
    async def delete_user_by_phone(cls, db: MysqlClient, phone: str):
        """Delete user by phone"""

        query = f"DELETE FROM user_data " \
                f"WHERE phone_number = %s"
        args = (phone,)
        await db.query_delete(query, args)

    @classmethod
    async def update_user_by_phone(cls, db: MysqlClient, params: List[str], phone: str):
        """Update needed params of user data by phone"""

        query = f"UPDATE user_data " \
                f"SET name=%s, surname=%s, patronymic=%s, phone_number=%s, email=%s, country=%s, " \
                f"country_code=%s, date_updated=NOW() " \
                f"WHERE phone_number = %s"
        args = (*params, phone)
        await db.query_update_one(query, args)

    @classmethod
    async def insert_new_user(cls, db: MysqlClient, params: List[str]):
        """Save new user"""

        query = f"INSERT INTO user_data (name, surname, patronymic, phone_number, email, country, " \
                f"country_code, date_created, date_updated) " \
                f"VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())"
        args = (*params, )
        await db.query_insert(query, args)
