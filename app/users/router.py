from fastapi import APIRouter, Depends, Response

from app.exceptions import NotUserException, UserExistsException
from app.users.auth import (
    authenticated,
    create_access_token,
    get_password_hash,
)
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.shemas import SUserAuth

router = APIRouter(prefix="/auth", tags=["auth & Пользователи"])


@router.get("/users")
async def list_users():
    result = await UserDAO.find_all()
    return result


@router.post("/sign_up")
async def sign_up(user_data: SUserAuth):
    if user := await UserDAO.find_one_or_none(email=user_data.email):
        raise UserExistsException()
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.create(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def sign_in(response: Response, user_data: SUserAuth):
    user = await authenticated(user_data.email, user_data.password)
    if not user:
        raise NotUserException()
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token


@router.post("/logout")
async def logout(responce: Response):
    responce.delete_cookie("booking_access_token")
    return {"message": "logout"}


@router.get("/profile")
async def profile(user: Users = Depends(get_current_user)):
    return user
