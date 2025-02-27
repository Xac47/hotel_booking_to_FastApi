from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserExistsException(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class NotUserException(UserExistsException):
    detail = "Такого пользователя нету"


class IncorrectEmailOrPasswordException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный пароль или email"


class TokenExpiredException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истёк"


class TokenAbsentException(TokenExpiredException):
    detail = "Токен отсутсвует"


class IncorrentTokenFormatException(TokenExpiredException):
    detail = "Неверный формат токена"


class RoomCannotBeBooked(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "He осталось свободных номеров"
