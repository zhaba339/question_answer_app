from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from uuid import UUID
from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.users.models import Users
from app.users.schemas import UserSchema
from app.base_repository import BaseRepository
from app.database import async_session_maker
from app.users.service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("", description="Получить всех пользователей", response_model=List[UserSchema])
async def read_all_users(
    service: UserService = Depends(UserService)
) -> List[UserSchema]:
    try:
        users = await service.get_all_users()
        return users
    except:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Пользователи не найдены")


@router.get("/{user_id}", description="Получить пользователя", response_model=UserSchema)
async def read_user(
    user_id: int,
    service: UserService = Depends(UserService)
) -> UserSchema:
    try:
        user = await service.get_one_user(user_id=user_id)
        return user
    except:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Пользователь не найден")


@router.post("", description="Создать пользователя", response_model=UserSchema)
async def post_user(
    login: str,
    password: str,
    service: UserService = Depends(UserService)
) -> UserSchema:
    try:
        user = await service.create_one_user(login=login, password=password)
        return user
    except:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Пользователь не найден")


@router.delete("/{user_id}", description="Удалить пользователя", status_code=HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    service: UserService = Depends(UserService)
):
    deleted_user = await service.delete_one_user(user_id=user_id)
    if not deleted_user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Пользователь не найден")



