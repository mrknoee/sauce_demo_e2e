import logging
import re
from typing import Optional

from playwright.async_api import Page, TimeoutError, expect

from config.settings import ElementWaits, Settings

logger = logging.getLogger(__name__)


class BasePage:
    """Async Playwright wrapper. Timeouts in seconds, converted to ms by ms()."""

    def __init__(self, page: Page):
        self.page = page

    def ms(self, timeout: Optional[int] = None, default: int = ElementWaits.DEFAULT) -> int:
        return int((default if timeout is None else timeout) * 1000)

    # Navigation
    async def goto(self, url: str, timeout: Optional[int] = None) -> None:
        navigation_timeout = self.ms(timeout, Settings.NAVIGATION_TIMEOUT)
        attempts = max(1, Settings.NAVIGATION_RETRIES + 1)

        for attempt in range(1, attempts + 1):
            try:
                logger.info("Navigating to %s (attempt %s/%s)", url, attempt, attempts)
                await self.page.goto(url, wait_until="commit", timeout=navigation_timeout)
                return
            except TimeoutError:
                if attempt == attempts:
                    raise
                logger.warning(
                    "Navigation to %s timed out after %ss; retrying.",
                    url,
                    navigation_timeout / 1000,
                )
                await self.page.wait_for_timeout(max(0, Settings.NAVIGATION_RETRY_DELAY_MS))

    async def current_url(self) -> str:
        return self.page.url

    # Actions
    async def click(self, locator: str, timeout: Optional[int] = None) -> None:
        logger.debug(f"Clicking: {locator}")
        await self.page.locator(locator).click(timeout=self.ms(timeout))

    async def fill(self, locator: str, value: str, timeout: Optional[int] = None) -> None:
        logger.debug(f"Filling '{value}' into: {locator}")
        await self.page.locator(locator).fill(value, timeout=self.ms(timeout))

    async def select_option(self, locator: str, value: str, timeout: Optional[int] = None) -> None:
        logger.debug(f"Selecting '{value}' in: {locator}")
        await self.page.locator(locator).select_option(label=value, timeout=self.ms(timeout))

    # Reads
    async def get_text(self, locator: str, timeout: Optional[int] = None) -> str:
        text = await self.page.locator(locator).text_content(timeout=self.ms(timeout))
        return (text or "").strip()

    async def get_all_texts(self, locator: str) -> list[str]:
        return [t.strip() for t in await self.page.locator(locator).all_text_contents()]

    async def get_count(self, locator: str) -> int:
        return await self.page.locator(locator).count()

    async def is_visible(self, locator: str, timeout: Optional[int] = None) -> bool:
        try:
            await self.page.locator(locator).first.wait_for(state="visible", timeout=self.ms(timeout, ElementWaits.QUICK))
            return True
        except Exception:
            return False

    # Assertions (auto-waiting via expect)
    async def check_visibility(self, locator: str, timeout: Optional[int] = None) -> None:
        await expect(self.page.locator(locator)).to_be_visible(timeout=self.ms(timeout))

    async def check_hidden(self, locator: str, timeout: Optional[int] = None) -> None:
        await expect(self.page.locator(locator)).to_be_hidden(timeout=self.ms(timeout))

    async def check_text(self, locator: str, expected_text: str, timeout: Optional[int] = None) -> None:
        await expect(self.page.locator(locator)).to_have_text(expected_text, timeout=self.ms(timeout))

    async def check_contains_text(self, locator: str, expected_text: str, timeout: Optional[int] = None) -> None:
        await expect(self.page.locator(locator)).to_contain_text(expected_text, timeout=self.ms(timeout))

    async def check_count(self, locator: str, expected_count: int, timeout: Optional[int] = None) -> None:
        await expect(self.page.locator(locator)).to_have_count(expected_count, timeout=self.ms(timeout))

    async def check_url_contains(self, fragment: str, timeout: Optional[int] = None) -> None:
        await expect(self.page).to_have_url(re.compile(re.escape(fragment)), timeout=self.ms(timeout))
