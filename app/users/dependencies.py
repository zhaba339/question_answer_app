from datetime import datetime, timezone

from fastapi import Request, HTTPException, status, Depends
from app.config import settings
from jose import jwt, JWTError

from users.repository import UserRepository


def get_token(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не найден')
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = settings.get_auth_data()
        payload = jwt.decode(token, auth_data['secret'], algorithms=[auth_data['algorithm']])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валиден')

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек")

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не найден ID пользователя")

    user = await UserRepository.find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")

    return user