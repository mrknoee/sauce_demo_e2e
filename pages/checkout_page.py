import logging

from playwright.async_api import Page

from locators.checkout_locators import CheckoutLocators
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    # Step one: your information
    async def fill_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        logger.info(f"Filling checkout info: {first_name} {last_name}, {postal_code}")
        await self.fill(CheckoutLocators.FIRST_NAME_INPUT, first_name)
        await self.fill(CheckoutLocators.LAST_NAME_INPUT, last_name)
        await self.fill(CheckoutLocators.POSTAL_CODE_INPUT, postal_code)

    async def click_continue(self) -> None:
        await self.click(CheckoutLocators.CONTINUE_BUTTON)

    async def click_cancel(self) -> None:
        await self.click(CheckoutLocators.CANCEL_BUTTON)

    async def check_error_message(self, expected_text: str) -> None:
        await self.check_visibility(CheckoutLocators.ERROR_MESSAGE)
        await self.check_contains_text(CheckoutLocators.ERROR_MESSAGE, expected_text)

    # Step two: overview
    async def check_payment_info(self) -> None:
        await self.check_text(CheckoutLocators.PAYMENT_INFO, "SauceCard #31337")

    async def check_shipping_info(self) -> None:
        await self.check_text(CheckoutLocators.SHIPPING_INFO, "Free Pony Express Delivery!")

    async def check_overview_loaded(self) -> None:
        await self.check_text(CheckoutLocators.TITLE, "Checkout: Overview")

    async def get_item_names(self) -> list[str]:
        return await self.get_all_texts(CheckoutLocators.ITEM_NAME)

    async def get_item_total(self) -> float:
        return self.parse_money(await self.get_text(CheckoutLocators.SUBTOTAL_LABEL))

    async def get_tax(self) -> float:
        return self.parse_money(await self.get_text(CheckoutLocators.TAX_LABEL))

    async def get_total(self) -> float:
        return self.parse_money(await self.get_text(CheckoutLocators.TOTAL_LABEL))

    async def click_finish(self) -> None:
        logger.info("Finishing the order")
        await self.click(CheckoutLocators.FINISH_BUTTON)

    async def click_back_home(self) -> None:
        await self.click(CheckoutLocators.BACK_TO_PRODUCTS_BUTTON)

    # Step three: complete
    async def check_order_complete(self) -> None:
        await self.check_url_contains("checkout-complete.html")
        await self.check_text(CheckoutLocators.COMPLETE_HEADER, "Thank you for your order!")

    @staticmethod
    def parse_money(label_text: str) -> float:
        """'Total: $32.39' -> 32.39"""
        return float(label_text.split("$")[-1].strip())
