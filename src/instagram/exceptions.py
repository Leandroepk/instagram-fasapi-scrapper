from fastapi import status, HTTPException


def UserHasNotInstagram():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User does not have instagram enabled",
    )
