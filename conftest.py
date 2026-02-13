"""
Global pytest configuration and fixtures.
"""
import pytest
from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext


# ============== Browser Fixtures ==============

@pytest.fixture(scope="session")
def browser():
    """Create a browser instance for the test session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser):
    """Create a new browser context for each test."""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        ignore_https_errors=True
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """Create a new page for each test."""
    page = context.new_page()
    yield page
    page.close()


# ============== Test Data ==============

@pytest.fixture
def valid_user():
    """Standard user credentials for Swag Labs."""
    return {
        "username": "standard_user",
        "password": "secret_sauce"
    }


@pytest.fixture
def locked_user():
    """Locked out user credentials."""
    return {
        "username": "locked_out_user",
        "password": "secret_sauce"
    }


@pytest.fixture
def problem_user():
    """Problem user credentials."""
    return {
        "username": "problem_user",
        "password": "secret_sauce"
    }


@pytest.fixture
def base_url():
    """Base URL for Swag Labs application."""
    return "https://www.saucedemo.com"
