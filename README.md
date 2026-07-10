# Sauce Demo E2E Tests

End-to-end tests for [Sauce Demo](https://www.saucedemo.com/) built with Python, Playwright, and pytest.

The suite covers login, inventory sorting, cart behavior, and checkout.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## Run tests

```powershell
# All tests
python -m pytest

# One test group
python -m pytest -m cart

# One file or test
python -m pytest tests/test_checkout_e2e.py
python -m pytest -k test_add_single_item_updates_badge
```

## Configuration

Use `.env` only for the application URL:

```env
BASE_URL=https://www.saucedemo.com/
```

Set browser and test behavior in `config/config.ini`:

- `headless`: run with or without a visible browser window
- `type`: `chromium`, `firefox`, or `webkit`
- `slow_mo`: delay browser actions for local debugging
- `fixture_scope`: browser-context lifetime
- `navigation_timeout`, `navigation_retries`, and `navigation_retry_delay_ms`: navigation resilience for the public demo site

## Reports

- `reports/report.html`: pytest HTML report
- `allure-results/`: raw Allure results
- `allure-report/index.html`: generated when the Allure CLI is installed

## Project Architecture

This project follows a **Page Object Model (POM)** pattern with async/await for efficient test execution:

### Technology Stack
- **Framework**: pytest with pytest-asyncio
- **Browser Automation**: Playwright (async)
- **Reporting**: pytest-html and Allure
- **Language**: Python 3.10+

### Layer Structure

```
┌─────────────────────────────────┐
│  Tests (test_*.py)              │  - Test scenarios and assertions
├─────────────────────────────────┤
│  Page Objects (pages/*.py)      │  - UI interactions and workflows
├─────────────────────────────────┤
│  Locators (locators/*.py)       │  - CSS selectors, centralized
├─────────────────────────────────┤
│  Async Fixtures (conftest.py)   │  - Browser setup, login fixtures
└─────────────────────────────────┘
```

### Key Components

| Component | Purpose |
|-----------|---------|
| **BasePage** | Async wrapper for Playwright actions (click, fill, wait, expect) |
| **Page Objects** | Domain-specific methods that combine locators and actions |
| **Locators** | Centralized selectors preventing duplication and improving maintainability |
| **Fixtures** | Pytest fixtures provide browser context, logged-in state, and page objects |
| **Data** | Test users and constants used across test suites |
| **Config** | Settings for browser, timeouts, and retry behavior |

## Project Layout

```text
config/    Runtime settings (headless, timeouts, retries)
data/      Test data (users, constants)
locators/  Page element selectors (CSS)
pages/     Page object classes with async methods
tests/     Test suites (organized by feature)
```
