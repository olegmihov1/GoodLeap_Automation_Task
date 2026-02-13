"""
Base Page class with common functionality for all pages.
"""
from playwright.sync_api import Page, expect


class BasePage:
    """Base class for all page objects."""
    
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "https://www.saucedemo.com"
    
    def navigate_to(self, path: str = ""):
        """Navigate to a specific path."""
        self.page.goto(f"{self.base_url}{path}")
    
    def get_title(self) -> str:
        """Get the page title."""
        return self.page.title()
    
    def get_url(self) -> str:
        """Get the current URL."""
        return self.page.url
    
    def wait_for_element(self, selector: str, timeout: int = 10000):
        """Wait for an element to be visible."""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
    
    def click(self, selector: str):
        """Click on an element."""
        self.page.click(selector)
    
    def fill(self, selector: str, value: str):
        """Fill an input field."""
        self.page.fill(selector, value)
    
    def get_text(self, selector: str) -> str:
        """Get text content of an element."""
        return self.page.text_content(selector) or ""
    
    def is_visible(self, selector: str) -> bool:
        """Check if an element is visible."""
        return self.page.is_visible(selector)
    
    def take_screenshot(self, name: str):
        """Take a screenshot."""
        self.page.screenshot(path=f"screenshots/{name}.png")
