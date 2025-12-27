from datetime import time, datetime
from app.redis_client import redis_client
from sqlalchemy.testing.suite.test_reflection import users
from starlette.exceptions import HTTPException
from sqlalchemy import select, insert, delete, exists
from app.answers.schemas import AnswerSchema
from app.answers.models import Answers
from app.base_repository import BaseRepository
from app.database import async_session_maker


class AnswerRepository(BaseRepository):
    model = Answers

    # def __init__(self):
    #     self.model = Answers
    #     self.db = db
    #     self.redis_client = redis_client

    @classmethod
    async def add_one_answer(cls, question_id, user_id, text):
        from app.questions.repository import QuestionRepository
        created_at = datetime.now()
        question = await QuestionRepository.find_by_id(question_id)
        if not question:
            raise Exception("Question not found")
        answer = await cls.insert(question_id=question_id, user_id=user_id, text=text, created_at=created_at)
        return answer


    @classmethod
    async def find_all_answers(cls):
        answers = await cls.find_all()
        return answers

    @classmethod
    async def find_one_answer(cls, answer_id):
        answer_orm = await cls.find_by_id(answer_id)
        answer_pydantic = AnswerSchema.model_validate(answer_orm)
        answer_json = answer_pydantic.model_dump_json()
        key = f"answer:{answer_id}"
        cached_answer = redis_client.setex(key, 10, answer_json)
        return answer_orm

    @classmethod
    async def delete_one_answer(cls, answer_id):
        await cls.delete(answer_id)

    @classmethod
    async def update_one_answer(cls, answer_id: int, text: str):
        async with async_session_maker() as session:
            result = await session.execute(
                select(cls.model).where(cls.model.id == answer_id)
            )
            answer = result.scalar_one_or_none()
            if not answer:
                raise ValueError("Not found")

            answer.text = text
            await session.commit()
            await session.refresh(answer)
            return answer



