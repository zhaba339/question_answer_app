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

    @classmethod
    async def exists_by_user(cls, user_id) -> bool:
        has_answers = select(exists().where.Answer.user_id == user_id)
        has_questions = select(exists().where.Question.user_id == user_id)
        result_has_answers = await has_answers.execute()
        result_has_questions = await has_questions.execute()
        return result_has_answers and result_has_questions

    @classmethod
    async def exists_user(cls, user_id) -> bool:
        exists_user = cls.find_by_id(user_id)
        if exists_user:
            return True
        return False