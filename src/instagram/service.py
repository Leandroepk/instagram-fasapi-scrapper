from time import sleep
from bson import ObjectId

from src.database import db_client
from src.selenium.service import Driver
from src.instagram.models import Instagram, InstagramRepository


# DB services

instagram_repository = InstagramRepository(database=db_client)


def get_by_user_id(user_id: str) -> Instagram | None:
    instagram = instagram_repository.find_one({"user_id": user_id})
    return Instagram.parse_obj(instagram) if instagram is not None else None


def update(instagram: Instagram) -> None:
    instagram_repository.find_one_and_update(
        {"_id": ObjectId(instagram.id)}, {"$set": instagram.dict()}
    )


def whitelist_exist(name: str) -> bool | None:
    item = instagram_repository.find_one({"whitelist.username": name})
    return item is not None


def blacklist_exist(name: str) -> bool | None:
    item = instagram_repository.find_one({"blacklist.username": name})
    return item is not None


# SELENIUM services


def open_searcher(driver: Driver):
    is_open = driver.get_by_class_name(class_name="_aaw6", multi=True)
    if len(list(is_open)) == 0:
        driver.click(
            driver.get_by_xpath(
                context=driver.get_by_class_name("x1iyjqo2"), xpath="./div[2]"
            )
        )
    sleep(1)


def search(driver: Driver, search_value):
    is_open = driver.get_by_xpath(
        xpath="_aauy",
        multi=True,
    )
    if len(list(is_open)) == 0:
        open_searcher(driver)

    element = driver.get_by_class_name("_aauy")
    input_value = driver.get_attribute(element, "value")

    if input_value != search_value:
        driver.clear(element)
        driver.send_keys(element, search_value)
        sleep(2)
