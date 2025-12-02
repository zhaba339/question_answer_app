from linecache import cache
from uuid import UUID
from typing import List
from fastapi import APIRouter, Path, Query
from fastapi.params import Depends
from starlette.exceptions import HTTPException
from app.answers.service import AnswerService
from app.answers.schemas import AnswerSchema
from app.answers.repository import AnswerRepository
from app.users.models import Users

router = APIRouter(
    prefix="/answers",
    tags=["Ответы"],
)

@router.get("", description="Получить все ответы", response_model=List[AnswerSchema])
async def get_answers(service: AnswerService = Depends(AnswerService)) -> List[AnswerSchema]:
    answers =  await service.get_all_answers()
    if not answers:
        raise HTTPException(status_code=404, detail="Ответы не найдены")
    return answers


@router.get("/{answer_id}", description="Получить конкретный ответ", response_model=AnswerSchema)
async def get_answer(answer_id: int, service: AnswerService = Depends(AnswerService)) -> AnswerSchema:
    answer =  await service.get_one_answer(answer_id=answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Ответ не найден")
    return answer


@router.post("/questions/{question_id}/answers", description="Добавить ответ к вопросу", response_model=AnswerSchema)
async def post_answer(
        question_id: int = Path(..., description="ID вопроса из базы данных", example=1),
        user_id: UUID = UUID("d8722f82-7567-438a-8613-f315ec177d09"),
        text: str = Query(..., description="Текст ответа"),
        service: AnswerService = Depends(AnswerService),
):
    answer = await service.create_one_answer(question_id=question_id, user_id=user_id, text=text)
    return answer


@router.delete("/{answer_id}", description="Удалить ответ", response_model=None)
async def delete_answer(answer_id: int, service: AnswerService = Depends(AnswerService)) -> None:
    answer = await service.delete_one_answer(answer_id=answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Ответ не найден")
    return answer


@router.put("/{answer_id}", response_model=AnswerSchema)
async def change_answer(
    answer_id: int,
    text: str,
    service: AnswerService = Depends()
):
    try:
        answer = await service.change_one_answer(answer_id, text)
        return answer
    except ValueError:
        raise HTTPException(status_code=404, detail="Ответ не найден")