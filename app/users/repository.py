from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import Users
from app.base_repository import BaseRepository
from sqlalchemy import select, exists
from app.answers.models import Answers
from app.questions.models import Questions
from database import async_session_maker
from users.schemas import UserSchema


class UserRepository(BaseRepository):
    model = Users

    @classmethod
    async def find_all_users(cls) -> Users or None:
        users = await cls.find_all()
        return users

    @classmethod
    async def find_user_by_id(cls, user_id) -> Users or None:
        user = await cls.find_by_id(user_id)
        return user

    @classmethod
    async def find_user_by_login(cls, login: str) -> Users or None:
        async with async_session_maker() as session:
            query = select(Users).where(cls.model.login == login)
            user = await session.execute(query)
            return user

    @classmethod
    async def insert_user(cls, login, password) -> Users or None:
        user = await cls.insert(login=login, password=password)
        return user

    @classmethod
    async def delete_user(cls, user_id) -> bool:
        return await cls.delete(user_id)

    @classmethod
    async def exists_answers_questions(cls, user_id) -> bool:
        async with async_session_maker() as session:
            query = select(exists().where(Questions.user_id == user_id))
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def exists_user(cls, user_id) -> bool:
        exists_user = cls.find_by_id(user_id)
        if exists_user:
            return True
        return False


    """Поиск пользователя по логину (существует или нет)"""
    @classmethod
    async def find_user_by_login(cls, login) -> UserSchema:
        async with async_session_maker() as session:
            query = select(Users).where(Users.login == login)
            result = await session.execute(query)
            return result.scalar_one_or_none()