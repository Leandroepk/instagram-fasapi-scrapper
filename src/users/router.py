from fastapi import APIRouter, Body, Depends, status

from src.auth.dependencies import current_user
from src.users.models import User
from src.users import service
from src.users.schemas import UserRequest, UserResponse
from src.users.dependencies import user_match


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get(
    "/me",
    status_code=200,
    responses={
        status.HTTP_200_OK: {
            "model": UserResponse,
        },
    },
)
async def me(user: User = Depends(current_user)):
    print(user)
    return UserResponse.parse_obj(user)


@router.get(
    "/",
    status_code=200,
    responses={
        status.HTTP_200_OK: {
            "model": list[UserResponse],
        },
    },
)
async def index(user: User = Depends(current_user)):
    users = service.index()
    return [UserResponse.parse_obj(user) for user in users]


@router.put(
    "/{user_id}",
    status_code=200,
    responses={
        status.HTTP_200_OK: {
            "model": UserResponse,
        },
    },
)
async def update(
    auth_user: User = Depends(user_match), new_user_data: UserRequest = Body(...)
):
    new_user = auth_user.dict() | new_user_data.dict()
    return service.update(auth_user.id, User.parse_obj(new_user))


@router.delete(
    "/{user_id}",
    status_code=204,
)
async def destroy(auth_user: User = Depends(user_match)):
    return service.delete(auth_user.id)
