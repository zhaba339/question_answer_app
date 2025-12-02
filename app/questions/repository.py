from datetime import time, datetime
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from starlette.exceptions import HTTPException

from app.answers.exceptions import AnswerNotFound, AnswersNotFound
from app.questions.exceptions import QuestionNotFound
from app.answers.models import Answers
from app.base_repository import BaseRepository
from app.questions.models import Questions
from app.questions.schemas import QuestionSchema, QuestionAnswersSchema
from app.database import async_session_maker


class QuestionRepository(BaseRepository):
    model = Questions

    @classmethod
    async def find_all_questions(cls):
        result = await cls.find_all()
        return result

    @classmethod
    async def find_question_and_answers(cls, question_id) -> QuestionAnswersSchema:
        from app.answers.repository import AnswerRepository
        question = await cls.find_by_id(question_id)
        answers = await AnswerRepository.find_all(question_id=question_id)
        result = QuestionAnswersSchema(
            id=question.id,
            text = question.text,
            created_at = question.created_at,
            answers = answers
        )
        return result

    @classmethod
    async def insert_question(cls, text: str) -> QuestionSchema:
        created_at = datetime.now()
        question = await cls.insert(text=text, created_at=created_at)
        return question

    @classmethod
    async def delete_question(cls, question_id) -> None:
        question = await cls.delete(question_id)
        return question

