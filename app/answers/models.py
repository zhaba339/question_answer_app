from enum import Enum

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.database import Base


class Answers(Base):
    __tablename__ = 'answers'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    question_id = sa.Column(sa.Integer, sa.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    user_id = sa.Column(sa.Uuid, nullable=False)
    text = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False)

    question = relationship("Questions", back_populates="answers")