from logging import getLogger

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from uuid import UUID

from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_409_CONFLICT, \
    HTTP_401_UNAUTHORIZED

from app.users.models import Users
from app.users.schemas import UserSchema, UserRegisterSchema, UserLoginSchema
from app.base_repository import BaseRepository
from app.database import async_session_maker
from app.users.models import Users
from app.users.service import UserService
from app.users.exceptions import EntityNotFoundError, EntityHasDependenciesError
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dependencies import get_current_user
from app.users.dependencies import get_current_admin_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/register", description="Регистрация нового пользователя", response_model=UserSchema)
async def register(
        user: UserRegisterSchema,
        service: UserService = Depends(UserService)
) -> UserSchema:
    exists_user = await service.get_exists_user(login=user.login)
    if exists_user:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail="Пользователь уже существует")
    user_dict = user.dict()
    user_dict['password'] = get_password_hash(user.password)
    new_user = await service.create_one_user(**user_dict)
    return new_user


@router.post("/login", description="Вход в аккаунт пользователя")
async def login(response: Response, user: UserLoginSchema):
    check = await authenticate_user(login=user.login, password=user.password)
    if not check:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль")
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return {"access_token": access_token, "refresh_token": None}


@router.get("/me", description="Получить данные о пользователе")
async def get_me(user_data: Users = Depends(get_current_user)):
    return user_data


@router.post("/logout", description="Выйти из аккаунта пользователя")
async def logout_user(response: Response):
    response.delete_cookie(key="access_token")
    return {'message': 'Пользователь успешно вышел из системы'}


@router.get("/{user_id}", description="Получить пользователя", response_model=UserSchema)
async def read_user(
        user_id: int,
        service: UserService = Depends(UserService)
) -> UserSchema:
    try:
        user = await service.get_one_user_by_id(user_id=user_id)
        return user
    except:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Пользователь не найден")


@router.post("", description="Создать пользователя", response_model=UserSchema)
async def post_user(
        login: str,
        password: str,
        service: UserService = Depends(UserService),
        user_data: UserSchema = Depends(get_current_admin_user)
) -> UserSchema:
    try:
        user = await service.create_one_user(login=login, password=password)
        return user
    except:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Пользователь не найден")


@router.delete("/{user_id}", description="Удалить пользователя", status_code=HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int,
        service: UserService = Depends(UserService),
        user_data: UserSchema = Depends(get_current_admin_user)
):
    try:
        await service.delete_one_user(user_id)
    except EntityNotFoundError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    except EntityHasDependenciesError:
        raise HTTPException(status_code=HTTP_409_CONFLICT,
                            detail="Невозможно удалить пользователя, так как у него есть ответы или вопросы")


@router.get("", description="Получить всех пользователей", response_model=list[UserSchema])
async def read_user(
        service: UserService = Depends(UserService),
        user_data: UserSchema = Depends(get_current_admin_user)
) -> list[UserSchema]:
    try:
        users = await service.get_all_users()
        return users
    except:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Пользователи не найдены")


@router.patch("", description="Изменить роль пользователя", response_model=UserSchema)
async def edit_role_user(
        user_id: int,
        is_admin_user: bool,
        service: UserService = Depends(UserService),
        user_data: UserSchema = Depends(get_current_admin_user)
) -> UserSchema:
    try:
        updated_user = await service.update_role_user(user_id=user_id, is_admin_user=is_admin_user)
    except EntityNotFoundError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return updated_user