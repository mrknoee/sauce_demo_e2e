
import os
from configparser import ConfigParser
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent

# Real environment values win over .env, so CI can override without a file.
load_dotenv(ROOT / ".env")

_ini = ConfigParser()
_ini.read(ROOT / "config" / "config.ini")


def get_bool(key: str, default: bool) -> bool:
    return os.getenv(key, str(default)).strip().lower() in ("1", "true", "yes", "on")


def get_int(key: str, default: int) -> int:
    try:
        return int(os.getenv(key, default))
    except (TypeError, ValueError):
        return default


def ini_get(section: str, key: str, fallback: str) -> str:
    return os.getenv(key.upper(), _ini.get(section, key, fallback=fallback))


class Links:
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/").rstrip("/") + "/"


class Settings:
    BROWSER = ini_get("BROWSER", "type", "chromium").strip().lower()
    HEADLESS = get_bool("HEADLESS", _ini.getboolean("BROWSER", "headless", fallback=True))
    SLOW_MO = get_int("SLOW_MO", _ini.getint("BROWSER", "slow_mo", fallback=0))
    VIEWPORT = {"width": 1920, "height": 1080}
    BROWSER_SCOPE = ini_get("PYTEST", "fixture_scope", "session").strip().lower()
    NAVIGATION_TIMEOUT = _ini.getint("PYTEST", "navigation_timeout", fallback=30)
    NAVIGATION_RETRIES = _ini.getint("PYTEST", "navigation_retries", fallback=1)
    NAVIGATION_RETRY_DELAY_MS = _ini.getint("PYTEST", "navigation_retry_delay_ms", fallback=500)


class ElementWaits:
    """Default interaction waits, in seconds (BasePage.ms converts to milliseconds)."""
    DEFAULT = 10
    QUICK = 5
    MEDIUM = 15
    EXTENDED = 30

