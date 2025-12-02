from starlette.exceptions import HTTPException

AnswerNotFound = HTTPException(status_code=404, detail="Ответ не найден")
AnswersNotFound = HTTPException(status_code=404, detail="Ответы не найдены")