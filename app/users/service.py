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
        if not users:
            return []
        return users

    @staticmethod
    async def get_one_user_by_id(user_id: int) -> UserSchema:
        user = await UserRepository.find_user_by_id(user_id)
        if not user:
            raise EntityNotFoundError
        return user

    @staticmethod
    async def get_one_user_by_login(login: str) -> UserSchema:
        user = await UserRepository.find_user_by_login(login)
        if not user:
            raise EntityNotFoundError
        return user

    @staticmethod
    async def create_one_user(login: str, password: str) -> UserSchema:
        user = await UserRepository.insert_user(login, password)
        return user

    @staticmethod
    async def delete_one_user(user_id) -> bool:
        user = await UserRepository.find_user_by_id(user_id)
        if not user:
            raise EntityNotFoundError("User", user_id)
        user_has_content = await UserRepository.exists_answers_questions(user_id)
        if user_has_content is True:
            raise EntityHasDependenciesError("User has existing answers or questions")
        else:
            await UserRepository.delete(user_id)
            return True

    @staticmethod
    async def get_exists_user(login: str) -> UserSchema or None:
        exists_user = await UserRepository.find_user_by_login(login)
        return exists_user

    @staticmethod
    async def update_role_user(user_id: int, is_admin_user: bool) -> UserSchema:
        user = await UserRepository.find_user_by_id(user_id)
        if not user:
            raise EntityNotFoundError("User", user_id)
        updated_user = await UserRepository.update_role_user(user_id, is_admin_user)
        return updated_user
