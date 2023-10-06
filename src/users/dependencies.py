from fastapi import Depends

from src.auth.dependencies import current_user
from src.users.exceptions import UserNotOwner
from src.users.models import User


async def user_match(
    user_id: str,
    auth: User = Depends(current_user),
) -> User:
    if user_id != auth.id:
        raise UserNotOwner()
    return auth
