from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic_mongo import AbstractRepository, ObjectIdField


class User(BaseModel):
    id: ObjectIdField = None
    username: str
    password: str
    disabled: bool = Field(default=False)
    instragram_enabled: bool = Field(default=False)
    twitter_enabled: bool = Field(default=False)

    class Config:
        json_encoders = {ObjectId: str}


class UserRepository(AbstractRepository[User]):
    class Meta:
        collection_name = 'spams'