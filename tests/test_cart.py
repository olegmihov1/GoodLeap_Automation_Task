"""
Shopping Cart tests for Swag Labs.

Test Coverage:
- View cart items
- Remove items from cart
- Continue shopping functionality
- Proceed to checkout
- Cart persistence
"""
import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


class TestCart:
    """Test suite for shopping cart functionality."""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page, valid_user):
        """Setup: Login before each test."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(valid_user["username"], valid_user["password"])
        self.inventory_page = InventoryPage(page)
        self.cart_page = CartPage(page)
        yield
    
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_empty_cart_display(self, page: Page):
        """
        Test: Empty cart page displays correctly.
        
        Steps:
        1. Click on cart icon without adding items
        
        Expected: Cart page shows with no items.
        """
        self.inventory_page.go_to_cart()
        
        assert self.cart_page.is_cart_page_displayed(), "Cart page should be displayed"
        assert self.cart_page.get_page_title() == "Your Cart"
        assert self.cart_page.is_cart_empty(), "Cart should be empty"
    
    @pytest.mark.ui
    @pytest.mark.critical
    def test_single_item_in_cart(self, page: Page):
        """
        Test: Single item appears correctly in cart.
        
        Steps:
        1. Add Backpack to cart
        2. Go to cart
        
        Expected: Cart shows Backpack.
        """
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.go_to_cart()
        
        assert self.cart_page.get_cart_item_count() == 1
        assert self.cart_page.is_item_in_cart("Sauce Labs Backpack")
    
    @pytest.mark.ui
    @pytest.mark.critical
    def test_multiple_items_in_cart(self, page: Page):
        """
        Test: Multiple items appear correctly in cart.
        
        Steps:
        1. Add Backpack to cart
        2. Add Bike Light to cart
        3. Go to cart
        
        Expected: Cart shows both items.
        """
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.add_bike_light_to_cart()
        self.inventory_page.go_to_cart()
        
        assert self.cart_page.get_cart_item_count() == 2
        assert self.cart_page.is_item_in_cart("Sauce Labs Backpack")
        assert self.cart_page.is_item_in_cart("Sauce Labs Bike Light")
    
    @pytest.mark.ui
    @pytest.mark.critical
    def test_remove_item_from_cart(self, page: Page):
        """
        Test: Remove item from cart.
        
        Steps:
        1. Add Backpack and Bike Light to cart
        2. Go to cart
        3. Remove Backpack
        
        Expected: Only Bike Light remains in cart.
        """
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.add_bike_light_to_cart()
        self.inventory_page.go_to_cart()
        
        self.cart_page.remove_item("sauce-labs-backpack")
        
        assert self.cart_page.get_cart_item_count() == 1
        assert not self.cart_page.is_item_in_cart("Sauce Labs Backpack")
        assert self.cart_page.is_item_in_cart("Sauce Labs Bike Light")
    
    @pytest.mark.ui
    def test_remove_all_items_from_cart(self, page: Page):
        """
        Test: Remove all items from cart.
        
        Steps:
        1. Add Backpack to cart
        2. Go to cart
        3. Remove Backpack
        
        Expected: Cart is empty.
        """
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.go_to_cart()
        
        self.cart_page.remove_item("sauce-labs-backpack")
        
        assert self.cart_page.is_cart_empty(), "Cart should be empty after removing all items"
    
    @pytest.mark.ui
    def test_continue_shopping(self, page: Page):
        """
        Test: Continue shopping button returns to inventory.
        
        Steps:
        1. Add item to cart
        2. Go to cart
        3. Click 'Continue Shopping'
        
        Expected: User is redirected to inventory page.
        """
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.go_to_cart()
        
        self.cart_page.continue_shopping()
        
        assert self.inventory_page.is_inventory_page_displayed()
        assert "inventory" in page.url
    
    @pytest.mark.ui
    def test_cart_persists_after_continue_shopping(self, page: Page):
        """
        Test: Cart items persist after continuing shopping.
        
        Steps:
        1. Add Backpack to cart
        2. Go to cart
        3. Continue shopping
        4. Add Bike Light
        5. Go to cart again
        
        Expected: Both items are in cart.
        """
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.go_to_cart()
        self.cart_page.continue_shopping()
        
        self.inventory_page.add_bike_light_to_cart()
        self.inventory_page.go_to_cart()
        
        assert self.cart_page.get_cart_item_count() == 2
        assert self.cart_page.is_item_in_cart("Sauce Labs Backpack")
        assert self.cart_page.is_item_in_cart("Sauce Labs Bike Light")
    
    @pytest.mark.ui
    def test_cart_shows_item_prices(self, page: Page):
        """
        Test: Cart displays item prices.
        
        Steps:
        1. Add Backpack to cart
        2. Go to cart
        
        Expected: Price is displayed for the item.
        """
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.go_to_cart()
        
        prices = self.cart_page.get_cart_item_prices()
        assert len(prices) == 1
        assert prices[0].startswith("$"), "Price should be displayed"
    
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_proceed_to_checkout(self, page: Page):
        """
        Test: Proceed to checkout from cart.
        
        Steps:
        1. Add item to cart
        2. Go to cart
        3. Click checkout
        
        Expected: User is redirected to checkout page.
        """
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.go_to_cart()
        
        self.cart_page.proceed_to_checkout()
        
        assert "checkout-step-one" in page.url
