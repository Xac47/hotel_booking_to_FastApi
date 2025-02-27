from datetime import datetime

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import *
from app.users.dao import UserDAO
from app.users.models import Users


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException()
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise IncorrentTokenFormatException()

    expire: str = payload.get("exp")

    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException()

    user_id: str = payload.get("sub")

    if not user_id:
        raise NotUserException(detail="с таким id пользователя нету")

    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise NotUserException()

    return user


async def get_current_admin_user(user: Users = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user
