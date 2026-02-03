from fastapi.params import Depends
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.config import settings
from users.repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


"""Получить хэш-пароль"""
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


"""Проверка на соответствие хеш-пароля и обычного пароля"""
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


"""Получить JWT-токен"""
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = settings.get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt


"""Аутентификация пользователя (проверка на наличие пользователя в базе данных)"""
async def authenticate_user(login: str, password: str):
    user = await UserRepository.find_user_by_login(login=login)
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user