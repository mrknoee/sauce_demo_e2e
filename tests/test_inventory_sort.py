import allure
import pytest

import data.sort_options as sort_options

pytestmark = pytest.mark.inventory


@allure.severity(allure.severity_level.NORMAL)
@allure.story("Inventory sorting")
@allure.id("INV-001")
async def test_inventory_loads_with_products(logged_in_inventory):
    count = await logged_in_inventory.get_item_count()
    assert count == 6, f"Expected 6 products, found {count}"


@allure.severity(allure.severity_level.NORMAL)
@allure.story("Inventory sorting")
@allure.id("INV-002")
async def test_sort_by_price_low_to_high(logged_in_inventory):
    await logged_in_inventory.sort_by(sort_options.PRICE_LOW_TO_HIGH)

    prices = await logged_in_inventory.get_item_prices()
    assert prices == sorted(prices), f"Prices not ascending: {prices}"


@allure.severity(allure.severity_level.NORMAL)
@allure.story("Inventory sorting")
@allure.id("INV-003")
async def test_sort_by_price_high_to_low(logged_in_inventory):
    await logged_in_inventory.sort_by(sort_options.PRICE_HIGH_TO_LOW)

    prices = await logged_in_inventory.get_item_prices()
    assert prices == sorted(prices, reverse=True), f"Prices not descending: {prices}"


@allure.severity(allure.severity_level.NORMAL)
@allure.story("Inventory sorting")
@allure.id("INV-004")
async def test_sort_by_name_a_to_z(logged_in_inventory):
    await logged_in_inventory.sort_by(sort_options.NAME_A_TO_Z)

    names = await logged_in_inventory.get_item_names()
    assert names == sorted(names), f"Names not A->Z: {names}"


@allure.severity(allure.severity_level.NORMAL)
@allure.story("Inventory sorting")
@allure.id("INV-005")
async def test_sort_by_name_z_to_a(logged_in_inventory):
    await logged_in_inventory.sort_by(sort_options.NAME_Z_TO_A)

    names = await logged_in_inventory.get_item_names()
    assert names == sorted(names, reverse=True), f"Names not Z->A: {names}"
