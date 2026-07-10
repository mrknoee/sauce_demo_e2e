import logging

from playwright.async_api import Page

from locators.inventory_locators import InventoryLocators
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


def to_slug(product_name: str) -> str:
    """'Sauce Labs Backpack' -> 'sauce-labs-backpack' (the add/remove button suffix)."""
    return product_name.strip().lower().replace(" ", "-").replace(".", "").replace("(", "").replace(")", "")


class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    async def check_loaded(self) -> None:
        await self.check_visibility(InventoryLocators.INVENTORY_CONTAINER)
        await self.check_text(InventoryLocators.TITLE, "Products")

    async def get_item_count(self) -> int:
        return await self.get_count(InventoryLocators.INVENTORY_ITEM)

    async def get_item_names(self) -> list[str]:
        return await self.get_all_texts(InventoryLocators.ITEM_NAME)

    async def get_item_prices(self) -> list[float]:
        prices = await self.get_all_texts(InventoryLocators.ITEM_PRICE)
        return [float(p.replace("$", "").strip()) for p in prices]

    async def sort_by(self, option_label: str) -> None:
        logger.info(f"Sorting inventory by '{option_label}'")
        await self.select_option(InventoryLocators.SORT_DROPDOWN, option_label)

    async def add_item_to_cart(self, product_name: str) -> None:
        logger.info(f"Adding '{product_name}' to cart")
        await self.click(InventoryLocators.add_to_cart(to_slug(product_name)))

    async def remove_item_from_cart(self, product_name: str) -> None:
        logger.info(f"Removing '{product_name}' from cart")
        await self.click(InventoryLocators.remove(to_slug(product_name)))

    async def get_cart_badge_count(self) -> int:
        if not await self.is_visible(InventoryLocators.CART_BADGE, timeout=2):
            return 0
        return int(await self.get_text(InventoryLocators.CART_BADGE))

    async def open_cart(self) -> None:
        await self.click(InventoryLocators.CART_LINK)

    async def logout(self) -> None:
        logger.info("Logging out")
        await self.click(InventoryLocators.BURGER_MENU_BUTTON)
        await self.click(InventoryLocators.LOGOUT_LINK)
