import allure
import pytest

from data import products
from data.checkout import CUSTOMER

pytestmark = pytest.mark.checkout


@allure.severity(allure.severity_level.BLOCKER)
@allure.story("Checkout end-to-end")
@allure.title("Complete purchase: login -> cart -> checkout -> confirmation")
async def test_full_checkout_flow(logged_in_inventory, cart_page, checkout_page):
    with allure.step("Add two products to the cart"):
        await logged_in_inventory.add_item_to_cart(products.BACKPACK)
        await logged_in_inventory.add_item_to_cart(products.BOLT_T_SHIRT)
        assert await logged_in_inventory.get_cart_badge_count() == 2

    with allure.step("Open the cart and proceed to checkout"):
        await logged_in_inventory.open_cart()
        await cart_page.check_loaded()
        assert await cart_page.get_item_count() == 2
        await cart_page.checkout()

    with allure.step("Fill in customer information"):
        await checkout_page.fill_information(**CUSTOMER)
        await checkout_page.click_continue()

    with allure.step("Verify the overview and totals"):
        await checkout_page.check_overview_loaded()
        items = await checkout_page.get_item_names()
        assert products.BACKPACK in items and products.BOLT_T_SHIRT in items, f"Overview missing an item: {items}"

        subtotal = await checkout_page.get_item_total()
        tax = await checkout_page.get_tax()
        total = await checkout_page.get_total()
        assert round(subtotal + tax, 2) == total, f"total {total} != subtotal {subtotal} + tax {tax}"

    with allure.step("Finish the order and confirm success"):
        await checkout_page.click_finish()
        await checkout_page.check_order_complete()


@allure.severity(allure.severity_level.NORMAL)
@allure.story("Checkout end-to-end")
async def test_checkout_requires_customer_information(logged_in_inventory, cart_page, checkout_page):
    await logged_in_inventory.add_item_to_cart(products.BACKPACK)
    await logged_in_inventory.open_cart()
    await cart_page.check_loaded()
    await cart_page.checkout()

    await checkout_page.fill_information(first_name="", last_name="Tester", postal_code="1000")
    await checkout_page.click_continue()

    await checkout_page.check_error_message("First Name is required")


@allure.severity(allure.severity_level.NORMAL)
@allure.story("Checkout end-to-end")
async def test_checkout_requires_last_name(logged_in_inventory, cart_page, checkout_page):
    await logged_in_inventory.add_item_to_cart(products.BACKPACK)
    await logged_in_inventory.open_cart()
    await cart_page.check_loaded()
    await cart_page.checkout()

    await checkout_page.fill_information(first_name="Jethro", last_name="", postal_code="1000")
    await checkout_page.click_continue()

    await checkout_page.check_error_message("Last Name is required")


@allure.severity(allure.severity_level.NORMAL)
@allure.story("Checkout end-to-end")
async def test_checkout_requires_postal_code(logged_in_inventory, cart_page, checkout_page):
    await logged_in_inventory.add_item_to_cart(products.BACKPACK)
    await logged_in_inventory.open_cart()
    await cart_page.check_loaded()
    await cart_page.checkout()

    await checkout_page.fill_information(first_name="Jethro", last_name="Tester", postal_code="")
    await checkout_page.click_continue()

    await checkout_page.check_error_message("Postal Code is required")


@allure.severity(allure.severity_level.NORMAL)
@allure.story("Checkout end-to-end")
async def test_checkout_requires_all_fields(logged_in_inventory, cart_page, checkout_page):
    await logged_in_inventory.add_item_to_cart(products.BACKPACK)
    await logged_in_inventory.open_cart()
    await cart_page.check_loaded()
    await cart_page.checkout()

    await checkout_page.fill_information(first_name="", last_name="", postal_code="")
    await checkout_page.click_continue()

    await checkout_page.check_error_message("First Name is required")


@allure.severity(allure.severity_level.NORMAL)
@allure.story("Checkout end-to-end")
async def test_checkout_step_one_cancel_returns_to_cart(logged_in_inventory, cart_page, checkout_page):
    await logged_in_inventory.add_item_to_cart(products.BACKPACK)
    await logged_in_inventory.open_cart()
    await cart_page.check_loaded()
    await cart_page.checkout()

    await checkout_page.click_cancel()
    await cart_page.check_loaded()
    assert await cart_page.get_item_count() == 1


@allure.severity(allure.severity_level.NORMAL)
@allure.story("Checkout end-to-end")
async def test_checkout_overview_cancel_returns_to_inventory(logged_in_inventory, cart_page, checkout_page, inventory_page):
    await logged_in_inventory.add_item_to_cart(products.BACKPACK)
    await logged_in_inventory.open_cart()
    await cart_page.check_loaded()
    await cart_page.checkout()

    await checkout_page.fill_information(**CUSTOMER)
    await checkout_page.click_continue()
    await checkout_page.check_overview_loaded()

    await checkout_page.click_cancel()
    await inventory_page.check_loaded()
    assert await logged_in_inventory.get_cart_badge_count() == 1


@allure.severity(allure.severity_level.NORMAL)
@allure.story("Checkout end-to-end")
async def test_checkout_overview_displays_payment_and_shipping_info(logged_in_inventory, cart_page, checkout_page):
    await logged_in_inventory.add_item_to_cart(products.BACKPACK)
    await logged_in_inventory.open_cart()
    await cart_page.check_loaded()
    await cart_page.checkout()

    await checkout_page.fill_information(**CUSTOMER)
    await checkout_page.click_continue()
    await checkout_page.check_overview_loaded()

    await checkout_page.check_payment_info()
    await checkout_page.check_shipping_info()


@allure.severity(allure.severity_level.NORMAL)
@allure.story("Checkout end-to-end")
async def test_complete_order_back_home_clears_cart(logged_in_inventory, cart_page, checkout_page):
    await logged_in_inventory.add_item_to_cart(products.BACKPACK)
    await logged_in_inventory.open_cart()
    await cart_page.check_loaded()
    await cart_page.checkout()

    await checkout_page.fill_information(**CUSTOMER)
    await checkout_page.click_continue()
    await checkout_page.check_overview_loaded()

    await checkout_page.click_finish()
    await checkout_page.check_order_complete()

    await checkout_page.click_back_home()
    await logged_in_inventory.check_loaded()
    assert await logged_in_inventory.get_cart_badge_count() == 0


@allure.severity(allure.severity_level.NORMAL)
@allure.story("Checkout end-to-end")
async def test_single_item_totals_are_consistent(logged_in_inventory, cart_page, checkout_page):
    await logged_in_inventory.add_item_to_cart(products.FLEECE_JACKET)
    await logged_in_inventory.open_cart()
    await cart_page.check_loaded()
    await cart_page.checkout()

    await checkout_page.fill_information(**CUSTOMER)
    await checkout_page.click_continue()
    await checkout_page.check_overview_loaded()

    subtotal = await checkout_page.get_item_total()
    tax = await checkout_page.get_tax()
    total = await checkout_page.get_total()
    assert round(subtotal + tax, 2) == total, f"total {total} != subtotal {subtotal} + tax {tax}"
