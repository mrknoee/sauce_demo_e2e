import logging

from playwright.async_api import Page

from config.settings import Links
from locators.login_locators import LoginLocators
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    async def load(self) -> None:
        await self.goto(Links.BASE_URL)
        await self.check_visibility(LoginLocators.LOGIN_BUTTON)

    async def input_username(self, username: str) -> None:
        await self.fill(LoginLocators.USERNAME_INPUT, username)

    async def input_password(self, password: str) -> None:
        await self.fill(LoginLocators.PASSWORD_INPUT, password)

    async def click_login(self) -> None:
        await self.click(LoginLocators.LOGIN_BUTTON)

    async def login(self, username: str, password: str) -> None:
        logger.info(f"Logging in as '{username}'")
        await self.input_username(username)
        await self.input_password(password)
        await self.click_login()

    async def get_error_message(self) -> str:
        return await self.get_text(LoginLocators.ERROR_MESSAGE)

    async def check_error_message(self, expected_text: str) -> None:
        await self.check_visibility(LoginLocators.ERROR_MESSAGE)
        await self.check_text(LoginLocators.ERROR_MESSAGE, expected_text)

    async def check_login_succeeded(self) -> None:
        await self.check_url_contains("inventory.html")
        await self.check_visibility(LoginLocators.APP_LOGO)

    async def check_on_login_screen(self) -> None:
        await self.check_visibility(LoginLocators.LOGIN_BUTTON)
