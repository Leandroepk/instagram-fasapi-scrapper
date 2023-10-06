from time import sleep
from fastapi import Depends

from src.auth.dependencies import current_user
from src.users.models import User
from src.selenium.service import Driver
from src.instagram.exceptions import UserHasNotInstagram
from src.instagram.service import blacklist_exist, get_by_user_id, update
from src.instagram.models import Instagram


async def user_has_instagram(
    auth: User = Depends(current_user),
) -> User:
    if not auth.instragram_enabled:
        raise UserHasNotInstagram()
    return auth


async def get_instagram(
    auth: User = Depends(user_has_instagram),
) -> Instagram:
    instagram = get_by_user_id(auth.id)
    if instagram is None:
        raise UserHasNotInstagram()
    return instagram


async def load_or_create_session(
    instagram: Instagram = Depends(get_instagram),
) -> User:
    driver = Driver()
    if len(instagram.cookies):
        driver.navigate("https://www.instagram.com/")
        driver.load_cookies(instagram.cookies)
        driver.refresh()
        sleep(1)
    else:
        driver.navigate("https://www.instagram.com/")
        sleep(0.6)
        driver.send_keys(driver.get_by_name("username"), instagram.username)
        driver.send_keys(driver.get_by_name("password"), instagram.password)
        driver.click(driver.get_by_xpath(".//*[@class='_acan _acap _acas _aj1-']"))
        sleep(10)

    if len(driver.get_by_class_name(class_name="_a9_1", multi=True)) > 0:
        driver.click(driver.get_by_class_name(class_name="_a9_1"))

    instagram.cookies = driver.get_cookies()
    update(instagram)
    sleep(1)
    return driver
