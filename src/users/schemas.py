from pydantic import BaseModel
from pydantic_mongo import ObjectIdField


class UserResponse(BaseModel):
    id: ObjectIdField = None
    username: str
    disabled: bool
    instragram_enabled: bool
    twitter_enabled: bool


class UserRequest(BaseModel):
    username: str
