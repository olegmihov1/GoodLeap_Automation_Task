"""
Inventory/Products page tests for Swag Labs.

Test Coverage:
- Product listing display
- Product sorting functionality
- Add to cart from inventory
- Remove from cart on inventory page
- Cart badge updates
"""
import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


class TestInventory:
    """Test suite for inventory/products page functionality."""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page, valid_user):
        """Setup: Login before each test."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(valid_user["username"], valid_user["password"])
        self.inventory_page = InventoryPage(page)
        yield
    
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_inventory_page_displays_products(self, page: Page):
        """
        Test: Inventory page displays all products.
        
        Expected: All 6 products are displayed on the page.
        """
        assert self.inventory_page.is_inventory_page_displayed()
        assert self.inventory_page.get_product_count() == 6, "Should display 6 products"
    
    @pytest.mark.ui
    def test_inventory_page_title(self, page: Page):
        """
        Test: Inventory page has correct title.
        
        Expected: Page title is "Products".
        """
        title = self.inventory_page.get_page_title()
        assert title == "Products", f"Expected 'Products', got '{title}'"
    
    @pytest.mark.ui
    def test_all_products_have_names(self, page: Page):
        """
        Test: All products have names displayed.
        
        Expected: 6 product names are present and non-empty.
        """
        names = self.inventory_page.get_all_product_names()
        assert len(names) == 6, "Should have 6 product names"
        for name in names:
            assert name and len(name) > 0, "Product name should not be empty"
    
    @pytest.mark.ui
    def test_all_products_have_prices(self, page: Page):
        """
        Test: All products have prices displayed.
        
        Expected: 6 product prices are present and formatted correctly.
        """
        prices = self.inventory_page.get_all_product_prices()
        assert len(prices) == 6, "Should have 6 product prices"
        for price in prices:
            assert price.startswith("$"), f"Price should start with $, got '{price}'"
    
    @pytest.mark.ui
    @pytest.mark.critical
    def test_sort_products_by_name_az(self, page: Page):
        """
        Test: Sort products by name A to Z.
        
        Steps:
        1. Select 'Name (A to Z)' from sort dropdown
        
        Expected: Products are sorted alphabetically ascending.
        """
        self.inventory_page.sort_products("az")
        names = self.inventory_page.get_all_product_names()
        sorted_names = sorted(names)
        assert names == sorted_names, "Products should be sorted A to Z"
    
    @pytest.mark.ui
    @pytest.mark.critical
    def test_sort_products_by_name_za(self, page: Page):
        """
        Test: Sort products by name Z to A.
        
        Steps:
        1. Select 'Name (Z to A)' from sort dropdown
        
        Expected: Products are sorted alphabetically descending.
        """
        self.inventory_page.sort_products("za")
        names = self.inventory_page.get_all_product_names()
        sorted_names = sorted(names, reverse=True)
        assert names == sorted_names, "Products should be sorted Z to A"
    
    @pytest.mark.ui
    @pytest.mark.critical
    def test_sort_products_by_price_low_to_high(self, page: Page):
        """
        Test: Sort products by price low to high.
        
        Steps:
        1. Select 'Price (low to high)' from sort dropdown
        
        Expected: Products are sorted by price ascending.
        """
        self.inventory_page.sort_products("lohi")
        prices = self.inventory_page.get_all_product_prices()
        # Convert prices to float for comparison
        numeric_prices = [float(p.replace("$", "")) for p in prices]
        assert numeric_prices == sorted(numeric_prices), "Products should be sorted by price low to high"
    
    @pytest.mark.ui
    @pytest.mark.critical
    def test_sort_products_by_price_high_to_low(self, page: Page):
        """
        Test: Sort products by price high to low.
        
        Steps:
        1. Select 'Price (high to low)' from sort dropdown
        
        Expected: Products are sorted by price descending.
        """
        self.inventory_page.sort_products("hilo")
        prices = self.inventory_page.get_all_product_prices()
        # Convert prices to float for comparison
        numeric_prices = [float(p.replace("$", "")) for p in prices]
        assert numeric_prices == sorted(numeric_prices, reverse=True), "Products should be sorted by price high to low"
    
    @pytest.mark.ui
    @pytest.mark.critical
    def test_add_single_product_to_cart(self, page: Page):
        """
        Test: Add a single product to cart.
        
        Steps:
        1. Click 'Add to cart' on Backpack
        
        Expected: Cart badge shows 1.
        """
        assert not self.inventory_page.is_cart_badge_visible(), "Cart should be empty initially"
        
        self.inventory_page.add_backpack_to_cart()
        
        assert self.inventory_page.is_cart_badge_visible(), "Cart badge should be visible"
        assert self.inventory_page.get_cart_badge_count() == 1, "Cart badge should show 1"
    
    @pytest.mark.ui
    @pytest.mark.critical
    def test_add_multiple_products_to_cart(self, page: Page):
        """
        Test: Add multiple products to cart.
        
        Steps:
        1. Add Backpack to cart
        2. Add Bike Light to cart
        3. Add Bolt T-Shirt to cart
        
        Expected: Cart badge shows 3.
        """
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.add_bike_light_to_cart()
        self.inventory_page.add_bolt_shirt_to_cart()
        
        assert self.inventory_page.get_cart_badge_count() == 3, "Cart badge should show 3"
    
    @pytest.mark.ui
    def test_remove_product_from_cart_on_inventory(self, page: Page):
        """
        Test: Remove product from cart while on inventory page.
        
        Steps:
        1. Add Backpack to cart
        2. Click 'Remove' on Backpack
        
        Expected: Cart badge disappears.
        """
        self.inventory_page.add_backpack_to_cart()
        assert self.inventory_page.get_cart_badge_count() == 1
        
        self.inventory_page.remove_product_from_cart("sauce-labs-backpack")
        
        assert not self.inventory_page.is_cart_badge_visible(), "Cart badge should not be visible"
    
    @pytest.mark.ui
    def test_add_to_cart_button_changes_to_remove(self, page: Page):
        """
        Test: 'Add to cart' button changes to 'Remove' after adding.
        
        Steps:
        1. Add Backpack to cart
        
        Expected: Button text changes to 'Remove'.
        """
        self.inventory_page.add_backpack_to_cart()
        
        remove_button = page.locator("[data-test='remove-sauce-labs-backpack']")
        assert remove_button.is_visible(), "Remove button should be visible after adding to cart"
