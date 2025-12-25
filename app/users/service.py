from typing import List
from app.users.repository import UserRepository
from app.users.schemas import UserSchema
from uuid import UUID
from app.answers.repository import AnswerRepository
from app.users.exceptions import EntityNotFoundError, EntityHasDependenciesError
from app.users.models import Users


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
        user_exists = await UserRepository.exists_user(user_id)
        if not user_exists:
            raise EntityNotFoundError("User", user_id)
        if await UserRepository.exists_by_user(user_id):
            raise EntityHasDependenciesError("User has existing answers or questions")
        await UserRepository.delete(user_id)
        return True