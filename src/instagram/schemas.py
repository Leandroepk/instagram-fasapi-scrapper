from pydantic import BaseModel


class UserResponse(BaseModel):
    id: str
    username: str
    disabled: bool


class UserRequest(BaseModel):
    username: str
