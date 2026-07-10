import logging

from playwright.async_api import Page

from locators.cart_locators import CartLocators
from pages.base_page import BasePage
from pages.inventory_page import to_slug

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    async def check_loaded(self) -> None:
        await self.check_text(CartLocators.TITLE, "Your Cart")

    async def get_item_count(self) -> int:
        return await self.get_count(CartLocators.CART_ITEM)

    async def get_item_names(self) -> list[str]:
        return await self.get_all_texts(CartLocators.ITEM_NAME)

    async def remove_item(self, product_name: str) -> None:
        logger.info(f"Removing '{product_name}' from cart")
        await self.click(CartLocators.remove(to_slug(product_name)))

    async def continue_shopping(self) -> None:
        await self.click(CartLocators.CONTINUE_SHOPPING_BUTTON)

    async def checkout(self) -> None:
        logger.info("Proceeding to checkout")
        await self.click(CartLocators.CHECKOUT_BUTTON)
