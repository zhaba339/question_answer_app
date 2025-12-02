from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.questions.models import Questions
from app.answers.models import Answers
from app.answers.router import router as answer_router
from app.questions.router import router as question_router

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Теперь SQLAlchemy "знает" о всех таблицах
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield

app = FastAPI()
app.include_router(question_router)
app.include_router(answer_router)