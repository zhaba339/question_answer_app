import uvicorn

from app.redis_client import redis_client
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.questions.models import Questions
from app.answers.models import Answers
from app.auth.router import router as auth_router
from app.answers.router import router as answer_router
from app.questions.router import router as question_router
from app.users.router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Проверяем подключение к Redis
    await redis_client.ping()
    yield
    # Закрываем соединение при завершении
    await redis_client.close()


app = FastAPI()

if "__main__" == __name__:
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)


app.include_router(auth_router)
app.include_router(question_router)
app.include_router(answer_router)
app.include_router(user_router)