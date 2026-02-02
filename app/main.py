import uvicorn
import logging
from app.redis_client import redis_client
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.questions.models import Questions
from app.answers.models import Answers
from app.answers.router import router as answer_router
from app.questions.router import router as question_router
from app.users.router import router as user_router



# Настройка логирования ДО создания логгера
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger()


@asynccontextmanager
async def lifespan(app):
    logger.info("Проверка подключений к БД...")
    await redis_client.ping()
    yield
    await redis_client.close()

app = FastAPI()


if "__main__" == __name__:
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


app.include_router(question_router)
app.include_router(answer_router)
app.include_router(user_router)