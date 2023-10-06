from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic_mongo import AbstractRepository, ObjectIdField

from src.selenium.models import Cookie


class Item(BaseModel):
    username: str
    link: str
    screenshot_path: str
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)


class Instagram(BaseModel):
    id: ObjectIdField = None
    user_id: str
    username: str
    password: str
    cookies: list[Cookie]
    search_values: list[str] = Field(default=[])
    whitelist: list[Item] = Field(default=[])
    blacklist: list[Item] = Field(default=[])

    class Config:
        json_encoders = {ObjectId: str}


class InstagramRepository(AbstractRepository[Instagram]):
    class Meta:
        collection_name = "instagram"
