from app.questions.repository import QuestionRepository
from app.questions.schemas import QuestionSchema, QuestionAnswersSchema
from typing import List

from app.questions.exceptions import QuestionNotFound


class QuestionService:
    @staticmethod
    async def get_all_questions() -> List[QuestionSchema]:
        questions = await QuestionRepository.find_all_questions()
        return questions

    @staticmethod
    async def get_one_question_and_answers(question_id: int) -> QuestionAnswersSchema:
        question = await QuestionRepository.find_question_and_answers(question_id)
        return question

    @staticmethod
    async def create_one_question(text) -> QuestionSchema:
        questions = await QuestionRepository.insert_question(text)
        return questions

    @staticmethod
    async def delete_one_question(question_id) -> None:
        await QuestionRepository.delete_question(question_id)


