from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class BaseAnswerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class AnswerSchema(BaseAnswerSchema):
    id: int
    user_id: int
    question_id: int
    text: str
    created_at: datetime

    class Config:
        from_attributes = True
