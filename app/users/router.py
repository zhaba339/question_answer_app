from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import Users
from app.users.schemas import UserSchema
from app.base_repository import BaseRepository

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("", description="Получить всех пользователей", response_model=list[UserSchema])
async def read_all_users():

    query = await BaseRepository.find_all(Users)
    users = query.scalars().all()
    print(users)
    return users