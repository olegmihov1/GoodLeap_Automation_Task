"""
Login functionality tests for Swag Labs.

Test Coverage:
- Valid user login
- Invalid credentials handling
- Locked out user handling
- Empty credentials validation
- Logout functionality
"""
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


class TestLogin:
    """Test suite for login functionality."""
    
    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_valid_user_login(self, page: Page, valid_user):
        """
        Test: Successful login with valid credentials.
        
        Steps:
        1. Navigate to login page
        2. Enter valid username and password
        3. Click login button
        
        Expected: User is redirected to inventory page.
        """
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(valid_user["username"], valid_user["password"])
        
        inventory_page = InventoryPage(page)
        assert inventory_page.is_inventory_page_displayed(), "Inventory page should be displayed after login"
        assert "inventory" in page.url, "URL should contain 'inventory'"
    
    @pytest.mark.ui
    @pytest.mark.critical
    def test_invalid_username_login(self, page: Page):
        """
        Test: Login attempt with invalid username.
        
        Steps:
        1. Navigate to login page
        2. Enter invalid username and valid password
        3. Click login button
        
        Expected: Error message is displayed.
        """
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("invalid_user", "secret_sauce")
        
        assert login_page.is_error_displayed(), "Error message should be displayed"
        error_msg = login_page.get_error_message()
        assert "Username and password do not match" in error_msg or "Epic sadface" in error_msg
    
    @pytest.mark.ui
    @pytest.mark.critical
    def test_invalid_password_login(self, page: Page, valid_user):
        """
        Test: Login attempt with invalid password.
        
        Steps:
        1. Navigate to login page
        2. Enter valid username and invalid password
        3. Click login button
        
        Expected: Error message is displayed.
        """
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(valid_user["username"], "wrong_password")
        
        assert login_page.is_error_displayed(), "Error message should be displayed"
        error_msg = login_page.get_error_message()
        assert "Username and password do not match" in error_msg or "Epic sadface" in error_msg
    
    @pytest.mark.ui
    @pytest.mark.critical
    def test_locked_out_user_login(self, page: Page, locked_user):
        """
        Test: Login attempt with locked out user.
        
        Steps:
        1. Navigate to login page
        2. Enter locked out user credentials
        3. Click login button
        
        Expected: Locked out error message is displayed.
        """
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(locked_user["username"], locked_user["password"])
        
        assert login_page.is_error_displayed(), "Error message should be displayed"
        error_msg = login_page.get_error_message()
        assert "locked out" in error_msg.lower(), "Error should mention locked out"
    
    @pytest.mark.ui
    def test_empty_username_login(self, page: Page):
        """
        Test: Login attempt with empty username.
        
        Steps:
        1. Navigate to login page
        2. Leave username empty, enter password
        3. Click login button
        
        Expected: Error message about required username.
        """
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("", "secret_sauce")
        
        assert login_page.is_error_displayed(), "Error message should be displayed"
        error_msg = login_page.get_error_message()
        assert "Username is required" in error_msg
    
    @pytest.mark.ui
    def test_empty_password_login(self, page: Page, valid_user):
        """
        Test: Login attempt with empty password.
        
        Steps:
        1. Navigate to login page
        2. Enter username, leave password empty
        3. Click login button
        
        Expected: Error message about required password.
        """
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(valid_user["username"], "")
        
        assert login_page.is_error_displayed(), "Error message should be displayed"
        error_msg = login_page.get_error_message()
        assert "Password is required" in error_msg
    
    @pytest.mark.ui
    def test_empty_credentials_login(self, page: Page):
        """
        Test: Login attempt with both fields empty.
        
        Steps:
        1. Navigate to login page
        2. Leave both fields empty
        3. Click login button
        
        Expected: Error message about required username.
        """
        login_page = LoginPage(page)
        login_page.open()
        login_page.click_login()
        
        assert login_page.is_error_displayed(), "Error message should be displayed"
        error_msg = login_page.get_error_message()
        assert "Username is required" in error_msg
    
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_logout(self, page: Page, valid_user):
        """
        Test: User can successfully logout.
        
        Steps:
        1. Login with valid credentials
        2. Open burger menu
        3. Click logout
        
        Expected: User is redirected to login page.
        """
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(valid_user["username"], valid_user["password"])
        
        inventory_page = InventoryPage(page)
        assert inventory_page.is_inventory_page_displayed()
        
        inventory_page.logout()
        
        assert login_page.is_login_page_displayed(), "Login page should be displayed after logout"
        assert page.url == "https://www.saucedemo.com/" or "saucedemo.com" in page.url
