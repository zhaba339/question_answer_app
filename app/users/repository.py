from app.users.models import Users
from app.base_repository import BaseRepository


class UserRepository(BaseRepository):
    model = Users

    @classmethod
    async def find_all_users(cls) -> Users or None:
        users = await cls.find_all()
        return users

    @classmethod
    async def find_user(cls, user_id) -> Users or None:
        user = await cls.find_by_id(user_id)
        return user

    @classmethod
    async def insert_user(cls, login, password) -> Users or None:
        user = await cls.insert(login=login, password=password)
        return user

    @classmethod
    async def delete_user(cls, user_id) -> bool:
        return await cls.delete(user_id)