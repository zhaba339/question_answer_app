from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

Base = declarative_base()

engine = create_async_engine(settings.get_database_url_async())

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
