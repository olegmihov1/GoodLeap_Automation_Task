"""
Login Page object for Swag Labs.
"""
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for the Swag Labs login page."""
    
    # Locators
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"
    LOGIN_LOGO = ".login_logo"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def open(self):
        """Navigate to the login page."""
        self.navigate_to("/")
        return self
    
    def enter_username(self, username: str):
        """Enter username in the input field."""
        self.fill(self.USERNAME_INPUT, username)
        return self
    
    def enter_password(self, password: str):
        """Enter password in the input field."""
        self.fill(self.PASSWORD_INPUT, password)
        return self
    
    def click_login(self):
        """Click the login button."""
        self.click(self.LOGIN_BUTTON)
        return self
    
    def login(self, username: str, password: str):
        """Perform complete login flow."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self
    
    def get_error_message(self) -> str:
        """Get the error message text."""
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def is_error_displayed(self) -> bool:
        """Check if error message is displayed."""
        return self.is_visible(self.ERROR_MESSAGE)
    
    def is_login_page_displayed(self) -> bool:
        """Verify login page is displayed."""
        return self.is_visible(self.LOGIN_LOGO) and self.is_visible(self.LOGIN_BUTTON)
