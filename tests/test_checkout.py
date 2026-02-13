"""
Checkout flow tests for Swag Labs.

Test Coverage:
- Complete checkout flow (E2E)
- Customer information validation
- Checkout overview verification
- Order completion
- Cancel checkout flow
"""
import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


class TestCheckout:
    """Test suite for checkout functionality."""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page, valid_user):
        """Setup: Login and add item to cart before each test."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(valid_user["username"], valid_user["password"])
        self.inventory_page = InventoryPage(page)
        self.cart_page = CartPage(page)
        self.checkout_page = CheckoutPage(page)
        yield
    
    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_complete_checkout_flow(self, page: Page):
        """
        Test: Complete end-to-end checkout flow.
        
        Steps:
        1. Add product to cart
        2. Go to cart
        3. Proceed to checkout
        4. Fill customer information
        5. Continue to overview
        6. Finish checkout
        
        Expected: Order is completed successfully.
        """
        # Add item and go to cart
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.go_to_cart()
        
        # Proceed to checkout
        self.cart_page.proceed_to_checkout()
        
        # Fill customer information
        self.checkout_page.fill_customer_info("Oleg", "Mihov", "12345")
        self.checkout_page.click_continue()
        
        # Verify overview page
        assert self.checkout_page.is_overview_page_displayed()
        assert self.checkout_page.get_overview_item_count() == 1
        
        # Complete the order
        self.checkout_page.click_finish()
        
        # Verify completion
        assert self.checkout_page.is_order_complete()
        assert "Thank you for your order" in self.checkout_page.get_complete_header()
    
    @pytest.mark.ui
    @pytest.mark.critical
    def test_checkout_multiple_items(self, page: Page):
        """
        Test: Checkout with multiple items.
        
        Steps:
        1. Add multiple products to cart
        2. Complete checkout flow
        
        Expected: Order with multiple items completes successfully.
        """
        # Add multiple items
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.add_bike_light_to_cart()
        self.inventory_page.add_bolt_shirt_to_cart()
        self.inventory_page.go_to_cart()
        
        # Proceed through checkout
        self.cart_page.proceed_to_checkout()
        self.checkout_page.fill_customer_info("Donald", "Trump", "90210")
        self.checkout_page.click_continue()
        
        # Verify all items in overview
        assert self.checkout_page.get_overview_item_count() == 3
        
        # Complete order
        self.checkout_page.click_finish()
        assert self.checkout_page.is_order_complete()
    
    @pytest.mark.ui
    @pytest.mark.critical
    def test_checkout_required_first_name(self, page: Page):
        """
        Test: First name is required for checkout.
        
        Steps:
        1. Go to checkout
        2. Leave first name empty
        3. Click continue
        
        Expected: Error message about required first name.
        """
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.go_to_cart()
        self.cart_page.proceed_to_checkout()
        
        # Fill only last name and postal code
        self.checkout_page.enter_last_name("Oleg")
        self.checkout_page.enter_postal_code("12345")
        self.checkout_page.click_continue()
        
        assert self.checkout_page.is_error_displayed()
        assert "First Name is required" in self.checkout_page.get_error_message()
    
    @pytest.mark.ui
    @pytest.mark.critical
    def test_checkout_required_last_name(self, page: Page):
        """
        Test: Last name is required for checkout.
        
        Steps:
        1. Go to checkout
        2. Leave last name empty
        3. Click continue
        
        Expected: Error message about required last name.
        """
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.go_to_cart()
        self.cart_page.proceed_to_checkout()
        
        # Fill only first name and postal code
        self.checkout_page.enter_first_name("Oleg")
        self.checkout_page.enter_postal_code("12345")
        self.checkout_page.click_continue()
        
        assert self.checkout_page.is_error_displayed()
        assert "Last Name is required" in self.checkout_page.get_error_message()
    
    @pytest.mark.ui
    @pytest.mark.critical
    def test_checkout_required_postal_code(self, page: Page):
        """
        Test: Postal code is required for checkout.
        
        Steps:
        1. Go to checkout
        2. Leave postal code empty
        3. Click continue
        
        Expected: Error message about required postal code.
        """
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.go_to_cart()
        self.cart_page.proceed_to_checkout()
        
        # Fill only names
        self.checkout_page.enter_first_name("Oleg")
        self.checkout_page.enter_last_name("Mihov")
        self.checkout_page.click_continue()
        
        assert self.checkout_page.is_error_displayed()
        assert "Postal Code is required" in self.checkout_page.get_error_message()
    
    @pytest.mark.ui
    def test_checkout_overview_shows_totals(self, page: Page):
        """
        Test: Checkout overview shows price totals.
        
        Steps:
        1. Add item to cart
        2. Proceed to checkout overview
        
        Expected: Subtotal, tax, and total are displayed.
        """
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.go_to_cart()
        self.cart_page.proceed_to_checkout()
        self.checkout_page.fill_customer_info("Oleg", "Mihov", "12345")
        self.checkout_page.click_continue()
        
        subtotal = self.checkout_page.get_subtotal()
        tax = self.checkout_page.get_tax()
        total = self.checkout_page.get_total()
        
        assert "Item total:" in subtotal
        assert "Tax:" in tax
        assert "Total:" in total
    
    @pytest.mark.ui
    def test_cancel_checkout_step_one(self, page: Page):
        """
        Test: Cancel from checkout step one returns to cart.
        
        Steps:
        1. Go to checkout step one
        2. Click cancel
        
        Expected: User is returned to cart.
        """
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.go_to_cart()
        self.cart_page.proceed_to_checkout()
        
        self.checkout_page.click_cancel()
        
        assert self.cart_page.is_cart_page_displayed()
    
    @pytest.mark.ui
    def test_cancel_checkout_step_two(self, page: Page):
        """
        Test: Cancel from checkout overview returns to inventory.
        
        Steps:
        1. Go to checkout overview
        2. Click cancel
        
        Expected: User is returned to inventory.
        """
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.go_to_cart()
        self.cart_page.proceed_to_checkout()
        self.checkout_page.fill_customer_info("Oleg", "Mihov", "12345")
        self.checkout_page.click_continue()
        
        self.checkout_page.click_cancel()
        
        assert self.inventory_page.is_inventory_page_displayed()
    
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_back_home_after_order_complete(self, page: Page):
        """
        Test: Back Home button returns to inventory.
        
        Steps:
        1. Complete order
        2. Click Back Home
        
        Expected: User is returned to inventory page.
        """
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.go_to_cart()
        self.cart_page.proceed_to_checkout()
        self.checkout_page.fill_customer_info("Oleg", "Mihov", "12345")
        self.checkout_page.click_continue()
        self.checkout_page.click_finish()
        
        assert self.checkout_page.is_order_complete()
        
        self.checkout_page.click_back_home()
        
        assert self.inventory_page.is_inventory_page_displayed()
    
    @pytest.mark.ui
    def test_cart_empty_after_order_complete(self, page: Page):
        """
        Test: Cart is empty after completing order.
        
        Steps:
        1. Complete order
        2. Go back home
        3. Check cart
        
        Expected: Cart is empty after order completion.
        """
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.go_to_cart()
        self.cart_page.proceed_to_checkout()
        self.checkout_page.fill_customer_info("Oleg", "Mihov", "12345")
        self.checkout_page.click_continue()
        self.checkout_page.click_finish()
        self.checkout_page.click_back_home()
        
        assert not self.inventory_page.is_cart_badge_visible(), "Cart should be empty after checkout"
