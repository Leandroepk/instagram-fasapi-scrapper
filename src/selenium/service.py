from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from src.selenium.models import Cookie
from src.config import is_prod


class Driver:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("--start-maximized")
        if is_prod:
            options.add_argument("--headless")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

    def get_cookies(self):
        return self.driver.get_cookies()

    def load_cookies(self, cookies: list[Cookie]):
        for cookie in cookies:
            cookie = dict(cookie)
            if cookie["expiry"] is None:
                del cookie["expiry"]
            self.driver.add_cookie(cookie)

    def refresh(self):
        self.driver.refresh()

    def navigate(self, route: str):
        self.driver.get(route)

    def get_by_xpath(self, xpath: str, context=None, multi=False):
        base = context if context is not None else self.driver
        if multi:
            return base.find_elements(By.XPATH, xpath)
        return base.find_element(By.XPATH, xpath)

    def get_by_name(self, name: str, context=None, multi=False):
        base = context if context is not None else self.driver
        if multi:
            return base.find_elements(By.NAME, name)
        return base.find_element(By.NAME, name)

    def get_by_class_name(self, class_name: str, context=None, multi=False):
        base = context if context is not None else self.driver
        if multi:
            return base.find_elements(By.CLASS_NAME, class_name)
        return base.find_element(By.CLASS_NAME, class_name)

    def get_by_link_text(self, link_text: str, context=None, multi=False):
        base = context if context is not None else self.driver
        if multi:
            return base.find_elements(By.LINK_TEXT, link_text)
        return base.find_element(By.LINK_TEXT, link_text)

    def clear(self, element):
        element.clear()

    def send_keys(self, element, value: str):
        element.send_keys(value)

    def click(self, element):
        element.click()

    def get_attribute(self, element, attribute: str):
        return element.get_attribute(attribute)

    def get_url(self) -> str:
        return self.driver.current_url

    def close(self):
        self.driver.close()

    def get_cookie(self):
        return self.driver.get_cookies()
