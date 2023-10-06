from fastapi import status, HTTPException


def UserNotOwner():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="User not owner"
    )


def UserNotFound():
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
