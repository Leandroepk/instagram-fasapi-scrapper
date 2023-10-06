from time import sleep
import uuid
from fastapi import APIRouter, Depends, status

from src.users.models import User
from src.users.schemas import UserResponse
from src.selenium.service import Driver
from src.instagram.models import Instagram, Item
from src.instagram.dependencies import (
    get_instagram,
    load_or_create_session,
    user_has_instagram,
)
from src.instagram.service import (
    blacklist_exist,
    whitelist_exist,
    search,
    update,
)


router = APIRouter(
    prefix="/instagram",
    tags=["instagram"],
)


@router.get(
    "/ragnarok-test",
    status_code=200,
    responses={
        status.HTTP_200_OK: {
            "model": UserResponse,
        },
    },
)
async def ragnarok_test(user: User = Depends(user_has_instagram)):
    driver = Driver()
    driver.navigate("https://ragnarokscanlation.com/manga/shuumatsu-no-valkyrie")
    element = driver.get_by_xpath('//*[@class="wp-manga-chapter    "]/a')
    string = driver.get_attribute(element, "text")
    string = " ".join(string.split())
    driver.close()
    return string


@router.get(
    "/instagram-test",
    status_code=200,
    responses={
        status.HTTP_200_OK: {
            "model": UserResponse,
        },
    },
)
async def main(
    driver: Driver = Depends(load_or_create_session),
    instagram: Instagram = Depends(get_instagram),
):
    values = instagram.search_values
    for value in values:
        if driver.get_url() != "https://www.instagram.com/":
            driver.navigate("https://www.instagram.com/")
        search(driver, value)
        items = driver.get_by_xpath(
            context=driver.get_by_class_name("xocp1fn"), xpath="./div", multi=True
        )

        urls = []
        if len(list(items)) > 1:
            for i in range(len(list(items))):
                urls.append(
                    driver.get_attribute(
                        driver.get_by_xpath(context=items[i], xpath="./a"),
                        "href",
                    )
                )

        for url in urls:
            item_name = url.split("/")[-2]
            if not whitelist_exist(item_name) and not blacklist_exist(item_name):
                print(url)
                driver.navigate(url)
                screenshot_path = f"static/screenshots/{uuid.uuid4()}.png"
                driver.driver.save_screenshot(screenshot_path)

                instagram.blacklist.append(
                    Item(username=item_name, link=url, screenshot_path=screenshot_path)
                )
                update(instagram)
                sleep(2)

    driver.close()
    return "success"
