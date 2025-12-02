
from typing import List, Any, Optional
from sqlalchemy import select, insert, delete
from sqlalchemy.orm.sync import update
from starlette.exceptions import HTTPException

from app.database import async_session_maker


class BaseRepository:

    @classmethod
    async def find_all(cls, **filters):
        async with async_session_maker() as session:
            try:
                query = select(cls.model)
                if filters:
                    query = query.filter_by(**filters)
                result = await session.execute(query)
                return result.scalars().all()
            except Exception as e:
                raise e

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            try:
                query = select(cls.model).where(cls.model.id == model_id)
                result = await session.execute(query)
                return result.scalar_one_or_none()
            except Exception as e:
                raise e

    @classmethod
    async def insert(cls, **data):
        async with async_session_maker() as session:
            try:
                query = insert(cls.model).values(**data).returning(cls.model)
                result = await session.execute(query)
                await session.commit()
                return result.scalar_one_or_none()
            except Exception as e:
                await session.rollback()
                raise e

    @classmethod
    async def delete(cls, model_id: int):
        async with async_session_maker() as session:
            try:
                obj = await cls.find_by_id(model_id)
                query = delete(cls.model).where(cls.model.id == model_id)
                await session.execute(query)
                await session.commit()
                return obj
            except Exception as e:
                await session.rollback()
                raise e

    # @classmethod
    # async def update(cls, model_id: int):
    #     async with async_session_maker() as session:
    #         try:
    #             query = session.query(cls.model).filter(cls.model.id == model_id).first()
    #             query = update(cls.model).where(cls.model.id == model_id)
    #             await session.execute(query)
    #             await session.commit()
    #             return obj
    #         except Exception as e:
    #             await session.rollback()
    #             raise e
