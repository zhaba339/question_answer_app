import uvicorn
import logging
import asyncio
from sqlalchemy import text

from app.redis_client import redis_client
from app.database import engine
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.answers.router import router as answer_router
from app.questions.router import router as question_router
from app.users.router import router as user_router
from app.system.router import router as system_router


# Настройка логирования ДО создания логгера
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Запуск приложения...")
    logger.info("Проверка подключения к базе данных...")
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            if result.scalar() == 1:
                logger.info("База данных успешно подключена!")
            else:
                logger.warning("Подключение к базе данных неожиданно вернуло не 1")
    except Exception as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        raise RuntimeError(f"Не удалось подключиться к базе данных: {e}")

    logger.info("Проверка подключения к Redis...")
    try:
        redis_client.ping()
        logger.info("Redis успешно подключен!")
    except Exception as e:
        logger.error(f"Ошибка подключения к Redis: {e}")
        raise RuntimeError(f"Не удалось подключиться к Redis: {e}")
    logger.info("Приложение запущено")
    yield

    logger.info("Закрытие соединений...")
    await engine.dispose()
    redis_client.close()
    logger.info("Приложение остановлено")

app = FastAPI(lifespan=lifespan)


if "__main__" == __name__:
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


app.include_router(question_router)
app.include_router(answer_router)
app.include_router(user_router)
app.include_router(system_router)

