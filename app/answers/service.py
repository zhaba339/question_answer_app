from typing import List
from uuid import UUID
from app.answers.schemas import AnswerSchema
from app.answers.repository import AnswerRepository


class AnswerService:

    @staticmethod
    async def get_all_answers() -> List[AnswerSchema]:
        answers = await AnswerRepository.find_all_answers()
        return answers

    @staticmethod
    async def create_one_answer(question_id: int, user_id: UUID, text: str) -> AnswerSchema:
        answer = await AnswerRepository.add_one_answer(question_id, user_id, text)
        return answer

    @staticmethod
    async def get_one_answer(answer_id: int) -> AnswerSchema:
        answer = await AnswerRepository.find_one_answer(answer_id)
        return answer

    @staticmethod
    async def delete_one_answer(answer_id: int) -> None:
        await AnswerRepository.delete_one_answer(answer_id)

    @staticmethod
    async def change_one_answer(answer_id: int, text: str):
        return await AnswerRepository.update_one_answer(answer_id, text)