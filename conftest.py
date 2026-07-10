import logging
import shutil
import subprocess
from pathlib import Path

import allure
import pytest
import pytest_asyncio
from playwright.async_api import async_playwright

from config.settings import Settings
from data.users import STANDARD_USER
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

logger = logging.getLogger(__name__)

TEST_FAILED = pytest.StashKey[bool]()

RESULTS_DIR = "allure-results"
REPORT_DIR = "allure-report"


# Browser / page fixtures
@pytest_asyncio.fixture(scope="session")
async def playwright():
    async with async_playwright() as pw:
        yield pw


@pytest_asyncio.fixture(scope="session")
async def browser(playwright):
    browser_type = getattr(playwright, Settings.BROWSER)
    logger.info(f"Launching {Settings.BROWSER} (headless={Settings.HEADLESS})")
    instance = await browser_type.launch(headless=Settings.HEADLESS, slow_mo=Settings.SLOW_MO)
    try:
        yield instance
    finally:
        await instance.close()


@pytest_asyncio.fixture(scope=Settings.BROWSER_SCOPE)
async def context(browser):
    ctx = await browser.new_context(viewport=Settings.VIEWPORT)
    try:
        yield ctx
    finally:
        await ctx.close()


@pytest_asyncio.fixture
async def page(context):
    p = await context.new_page()
    yield p
    await p.close()


# Page objects
@pytest_asyncio.fixture
async def login_page(page) -> LoginPage:
    return LoginPage(page)


@pytest_asyncio.fixture
async def inventory_page(page) -> InventoryPage:
    return InventoryPage(page)


@pytest_asyncio.fixture
async def cart_page(page) -> CartPage:
    return CartPage(page)


@pytest_asyncio.fixture
async def checkout_page(page) -> CheckoutPage:
    return CheckoutPage(page)


@pytest_asyncio.fixture
async def logged_in_inventory(login_page, inventory_page) -> InventoryPage:
    """Log in and return inventory page."""
    await login_page.load()
    await login_page.login(STANDARD_USER["username"], STANDARD_USER["password"])
    await inventory_page.check_loaded()
    return inventory_page


# Attach a screenshot to Allure when a test fails
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when in ("setup", "call") and report.failed:
        item.stash[TEST_FAILED] = True


@pytest_asyncio.fixture(autouse=True)
async def screenshot_on_failure(request, page):
    yield
    if request.node.stash.get(TEST_FAILED, False):
        try:
            png = await page.screenshot(full_page=True)
            allure.attach(png, name=request.node.name, attachment_type=allure.attachment_type.PNG)
        except Exception as exc:
            logger.warning(f"Could not capture failure screenshot: {exc}")


# Generate Allure report after test run
def pytest_sessionfinish(session, exitstatus):
    if not Path(RESULTS_DIR).exists() or not any(Path(RESULTS_DIR).iterdir()):
        return
    if shutil.which("allure") is None:
        logger.info("Allure CLI not installed; skipping report")
        return
    try:
        subprocess.run(
            ["allure", "generate", RESULTS_DIR, "-o", REPORT_DIR, "--clean", "--single-file"],
            check=True,
            capture_output=True,
        )
        logger.info(f"Allure report: {REPORT_DIR}/index.html")
    except (subprocess.CalledProcessError, OSError) as exc:
        logger.warning(f"Could not generate Allure report: {exc}")
