from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
import jwt

from src.auth.exceptions import DisabledUser, InvalidToken
from src.auth.config import SECRET, ALGORITHM
from src.users.models import User
from src.users.service import find
from src.users.exceptions import UserNotFound


async def parse_jwt_data(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="auth/login")),
) -> str:
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    except JWTError:
        raise InvalidToken()

    return payload["id"]


async def auth_user(id: str = Depends(parse_jwt_data)):
    user = find(id)
    if user is None:
        raise UserNotFound()
    return user


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise DisabledUser()

    return user
