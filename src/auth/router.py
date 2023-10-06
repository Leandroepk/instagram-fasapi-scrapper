import jwt
from passlib.context import CryptContext
from fastapi import APIRouter, Body, status

from src.auth.schemas import (
    AuthRequest,
    AuthResponse,
    RegisterRequest,
    RegisterResponse,
)
from src.auth.exceptions import BadPassword, BadUsername, UserAlreadyExists
from src.users.service import get_by_username, insert
from src.auth.config import SECRET, ALGORITHM
from src.users.models import User


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


crypt = CryptContext(schemes=["bcrypt"])


@router.post(
    "/register",
    status_code=201,
    responses={
        status.HTTP_201_CREATED: {
            "model": RegisterResponse,
        },
    },
)
async def register(form: RegisterRequest = Body(...)):
    db_user = get_by_username(form.username)
    if db_user is not None:
        raise UserAlreadyExists()
    form.password = crypt.encrypt(form.password)
    user = insert(User.parse_obj(form))
    user.id = str(user.id)

    return RegisterResponse.parse_obj(user)


@router.post(
    "/login",
    status_code=200,
    responses={
        status.HTTP_200_OK: {
            "model": AuthResponse,
        },
    },
)
async def login(form: AuthRequest = Body(...)):
    user = get_by_username(form.username)
    if not user:
        raise BadUsername()

    if not crypt.verify(form.password, user.password):
        raise BadPassword()

    access_token = {"id": str(user.id)}

    return {
        "access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM),
        "token_type": "bearer",
    }
