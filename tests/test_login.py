import allure
import pytest

from data.users import LOGIN_CASES, LOCKED_OUT_USER, STANDARD_USER, INVALID_CREDENTIALS_ERROR

pytestmark = pytest.mark.login


@allure.severity(allure.severity_level.CRITICAL)
@allure.story("Login")
@pytest.mark.parametrize("username, profile", LOGIN_CASES, ids=[case[0] for case in LOGIN_CASES])
async def test_login_per_user(login_page, username, profile):
    await login_page.load()
    await login_page.login(profile["username"], profile["password"])

    if profile["should_login"]:
        await login_page.check_login_succeeded()
    else:
        await login_page.check_error_message(profile["expected_error"])


@allure.severity(allure.severity_level.CRITICAL)
@allure.story("Login")
async def test_locked_out_user_shows_error_banner(login_page):
    await login_page.load()
    await login_page.login(LOCKED_OUT_USER["username"], LOCKED_OUT_USER["password"])

    await login_page.check_error_message(LOCKED_OUT_USER["expected_error"])
    assert "inventory.html" not in await login_page.current_url(), (
        "Locked-out user must not reach the inventory page"
    )


@allure.severity(allure.severity_level.NORMAL)
@allure.story("Login")
async def test_login_with_wrong_password_is_rejected(login_page):
    await login_page.load()
    await login_page.login(STANDARD_USER["username"], "wrong_password")

    await login_page.check_error_message(INVALID_CREDENTIALS_ERROR)


@allure.severity(allure.severity_level.NORMAL)
@allure.story("Login")
async def test_login_with_empty_username_is_rejected(login_page):
    await login_page.load()
    await login_page.login("", STANDARD_USER["password"])

    await login_page.check_error_message(INVALID_CREDENTIALS_ERROR)


@allure.severity(allure.severity_level.NORMAL)
@allure.story("Login")
async def test_login_with_empty_password_is_rejected(login_page):
    await login_page.load()
    await login_page.login(STANDARD_USER["username"], "")

    await login_page.check_error_message(INVALID_CREDENTIALS_ERROR)


@allure.severity(allure.severity_level.NORMAL)
@allure.story("Login")
async def test_login_with_empty_credentials_is_rejected(login_page):
    await login_page.load()
    await login_page.login("", "")

    await login_page.check_error_message(INVALID_CREDENTIALS_ERROR)


@allure.severity(allure.severity_level.NORMAL)
@allure.story("Login")
async def test_standard_user_can_log_out(login_page, inventory_page):
    await login_page.load()
    await login_page.login(STANDARD_USER["username"], STANDARD_USER["password"])
    await inventory_page.check_loaded()

    await inventory_page.logout()

    await login_page.check_on_login_screen()
