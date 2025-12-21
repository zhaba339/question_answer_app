import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.database import Base


class Questions(Base):
    __tablename__ = 'questions'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    text = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False)
    answers = relationship("Answers", back_populates="question", cascade="all, delete-orphan")
