from typing import List, Optional
from starlette.exceptions import HTTPException
from fastapi import APIRouter, Depends
from starlette.status import HTTP_404_NOT_FOUND

from app.questions.repository import QuestionRepository
from app.questions.schemas import QuestionSchema, QuestionAnswersSchema
from app.questions.service import QuestionService
from app.questions.exceptions import QuestionNotFound

router = APIRouter(
    prefix="/questions",
    tags=["Questions"],
)


@router.get("", description="Список всех вопросов", response_model=List[QuestionSchema])
async def read_all_questions(
        service: QuestionService = Depends(QuestionService),
):
    questions = await service.get_all_questions()
    return questions


@router.post("", description="Создать новый вопрос", response_model=QuestionSchema)
async def post_question(
        text: str,
        service: QuestionService = Depends(QuestionService),
):
    return await service.create_one_question(text)


@router.get("/{question_id}", description="Получить вопрос и все ответы на него", response_model=QuestionAnswersSchema)
async def get_question_and_answers(
        question_id: int,
        service: QuestionService = Depends(QuestionService),
):
    try:
        question = await service.get_one_question_and_answers(question_id=question_id)
        return question
    except:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Вопрос не найден")


@router.delete("/{question_id}", description="Удалить вопрос вместе с ответами", response_model=None)
async def delete_question(
        question_id: int,
        service: QuestionService = Depends(QuestionService),
):
    question = await service.delete_one_question(question_id)
    if not question:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Вопрос не найден")
    return question