from typing import List
from uuid import UUID

from app.redis_client import redis_client
from app.answers.schemas import AnswerSchema
from app.answers.repository import AnswerRepository


class AnswerService:

    @staticmethod
    async def get_all_answers() -> List[AnswerSchema]:
        answers = await AnswerRepository.find_all_answers()
        return answers

    @staticmethod
    async def create_one_answer(question_id: int, user_id: int, text: str) -> AnswerSchema:
        answer = await AnswerRepository.add_one_answer(question_id, user_id, text)
        return answer

    @staticmethod
    async def get_one_answer(answer_id: int) -> AnswerSchema:
        cached_key = f"answer:{answer_id}"
        cached_data = await redis_client.get(cached_key)

        if cached_data:
            answer_json = AnswerSchema.model_validate_json(cached_data)
            return answer_json

        answer = await AnswerRepository.find_one_answer(answer_id)

        if answer:
            answer_schema = AnswerSchema.model_validate(answer)
            answer_json = answer_schema.model_dump_json()
            await redis_client.setex(cached_key, 10, answer_json)
            return answer

    @staticmethod
    async def delete_one_answer(answer_id: int) -> None:
        await AnswerRepository.delete_one_answer(answer_id)

    @staticmethod
    async def change_one_answer(answer_id: int, text: str):
        return await AnswerRepository.update_one_answer(answer_id, text)
