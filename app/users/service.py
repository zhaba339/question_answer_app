from typing import List
from app.users.repository import UserRepository
from app.users.schemas import UserSchema
from uuid import UUID


class UserService:

    @staticmethod
    async def get_all_users() -> List[UserSchema]:
        users = await UserRepository.find_all_users()
        return users

    @staticmethod
    async def get_one_user(user_id: int) -> UserSchema:
        user = await UserRepository.find_user(user_id)
        return user

    @staticmethod
    async def create_one_user(login: str, password: str) -> UserSchema:
        user = await UserRepository.insert_user(login, password)
        return user

    @staticmethod
    async def delete_one_user(user_id) -> bool:
        return await UserRepository.delete_user(user_id)