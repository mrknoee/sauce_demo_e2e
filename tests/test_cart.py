import allure
import pytest

from data import products

pytestmark = pytest.mark.cart


@allure.severity(allure.severity_level.CRITICAL)
@allure.story("Cart")
@allure.id("CART-001")
async def test_add_single_item_updates_badge(logged_in_inventory):
    await logged_in_inventory.add_item_to_cart(products.BACKPACK)

    assert await logged_in_inventory.get_cart_badge_count() == 1


@allure.severity(allure.severity_level.NORMAL)
@allure.story("Cart")
@allure.id("CART-002")
async def test_add_multiple_items_updates_badge(logged_in_inventory):
    await logged_in_inventory.add_item_to_cart(products.BACKPACK)
    await logged_in_inventory.add_item_to_cart(products.BIKE_LIGHT)
    await logged_in_inventory.add_item_to_cart(products.BOLT_T_SHIRT)

    assert await logged_in_inventory.get_cart_badge_count() == 3


@allure.severity(allure.severity_level.NORMAL)
@allure.story("Cart")
@allure.id("CART-003")
async def test_remove_item_from_inventory_decrements_badge(logged_in_inventory):
    await logged_in_inventory.add_item_to_cart(products.BACKPACK)
    await logged_in_inventory.add_item_to_cart(products.BIKE_LIGHT)

    await logged_in_inventory.remove_item_from_cart(products.BACKPACK)

    assert await logged_in_inventory.get_cart_badge_count() == 1


@allure.severity(allure.severity_level.CRITICAL)
@allure.story("Cart")
@allure.id("CART-004")
async def test_added_items_appear_on_cart_page(logged_in_inventory, cart_page):
    await logged_in_inventory.add_item_to_cart(products.BACKPACK)
    await logged_in_inventory.add_item_to_cart(products.FLEECE_JACKET)
    await logged_in_inventory.open_cart()

    await cart_page.check_loaded()
    assert await cart_page.get_item_count() == 2

    names = await cart_page.get_item_names()
    assert products.BACKPACK in names and products.FLEECE_JACKET in names, f"Cart missing an item: {names}"


@allure.severity(allure.severity_level.NORMAL)
@allure.story("Cart")
@allure.id("CART-005")
async def test_remove_item_on_cart_page(logged_in_inventory, cart_page):
    await logged_in_inventory.add_item_to_cart(products.BACKPACK)
    await logged_in_inventory.add_item_to_cart(products.BIKE_LIGHT)
    await logged_in_inventory.open_cart()
    await cart_page.check_loaded()

    await cart_page.remove_item(products.BACKPACK)

    assert await cart_page.get_item_count() == 1
    names = await cart_page.get_item_names()
    assert products.BACKPACK not in names, f"Removed item still in cart: {names}"


@allure.severity(allure.severity_level.NORMAL)
@allure.story("Cart")
@allure.id("CART-006")
async def test_reset_app_state_clears_cart(logged_in_inventory):
    await logged_in_inventory.add_item_to_cart(products.BACKPACK)
    await logged_in_inventory.open_menu()
    await logged_in_inventory.reset_app_state()

    assert await logged_in_inventory.get_cart_badge_count() == 0
