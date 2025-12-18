from uuid import UUID
from app.database import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.UUID, unique=True, nullable=False)
    login = sa.Column(sa.String, nullable=False)
    password = sa.Column(sa.String, nullable=False)

