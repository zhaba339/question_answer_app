from datetime import datetime
from typing import List

from alembic.config import Config
from pydantic import BaseModel, ConfigDict
from sqlalchemy.sql.operators import from_

from app.answers.schemas import AnswerSchema


class BaseQuestionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class QuestionSchema(BaseQuestionSchema):
    id: int
    user_id: int
    text: str
    created_at: datetime


class QuestionAnswersSchema(QuestionSchema):
    answers: List[AnswerSchema]

