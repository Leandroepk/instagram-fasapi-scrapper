from fastapi import status, HTTPException


def InvalidToken():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
    )


def InvalidCredentials():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def BadUsername():
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="The user is not correct"
    )


def BadPassword():
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="The password is not correct",
    )


def DisabledUser():
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
    )


def UserAlreadyExists():
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT, detail="User already exists"
    )
