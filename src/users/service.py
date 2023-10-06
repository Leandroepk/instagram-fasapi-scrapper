from bson import ObjectId

from src.database import db_client
from src.users.models import User, UserRepository


# DB services

user_repository = UserRepository(database=db_client)


def index() -> list[User]:
    users = user_repository.find_by()
    return [User.parse_obj(user) for user in users]


def find(id: str) -> User | None:
    print(id)
    user = user_repository.find_one_by_id(ObjectId(id))
    return User.parse_obj(user) if user is not None else user


def get_by_username(name: str) -> User | None:
    user = user_repository.find_one_by({"username": name})
    return User.parse_obj(user) if user is not None else user


def insert(user: User) -> User | None:
    user_repository.save(user)
    return find("test")


def update(user_id: str, user: User) -> User | None:
    user_repository.find_one_and_update(
        {"_id": ObjectId(user_id)}, {"$set": user.dict()}
    )
    return find(user_id)


def delete(user_id: str) -> None:
    user_repository.delete_one({"_id": ObjectId(user_id)})
