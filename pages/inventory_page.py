"""
Inventory Page object for Swag Labs.
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Page object for the Swag Labs inventory/products page."""
    
    # Locators
    INVENTORY_CONTAINER = "#inventory_container"
    INVENTORY_ITEM = ".inventory_item"
    INVENTORY_ITEM_NAME = ".inventory_item_name"
    INVENTORY_ITEM_PRICE = ".inventory_item_price"
    ADD_TO_CART_BUTTON = "[data-test^='add-to-cart']"
    REMOVE_BUTTON = "[data-test^='remove']"
    SHOPPING_CART_BADGE = ".shopping_cart_badge"
    SHOPPING_CART_LINK = ".shopping_cart_link"
    SORT_DROPDOWN = "[data-test='product-sort-container']"
    BURGER_MENU = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"
    PAGE_TITLE = ".title"
    
    # Specific product buttons
    BACKPACK_ADD = "[data-test='add-to-cart-sauce-labs-backpack']"
    BIKE_LIGHT_ADD = "[data-test='add-to-cart-sauce-labs-bike-light']"
    BOLT_SHIRT_ADD = "[data-test='add-to-cart-sauce-labs-bolt-t-shirt']"
    FLEECE_JACKET_ADD = "[data-test='add-to-cart-sauce-labs-fleece-jacket']"
    ONESIE_ADD = "[data-test='add-to-cart-sauce-labs-onesie']"
    RED_SHIRT_ADD = "[data-test='add-to-cart-test.allthethings()-t-shirt-(red)']"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def is_inventory_page_displayed(self) -> bool:
        """Verify inventory page is displayed."""
        return self.is_visible(self.INVENTORY_CONTAINER)
    
    def get_page_title(self) -> str:
        """Get the page title text."""
        return self.get_text(self.PAGE_TITLE)
    
    def get_product_count(self) -> int:
        """Get the number of products displayed."""
        return self.page.locator(self.INVENTORY_ITEM).count()
    
    def get_all_product_names(self) -> list:
        """Get list of all product names."""
        elements = self.page.locator(self.INVENTORY_ITEM_NAME).all()
        return [el.text_content() for el in elements]
    
    def get_all_product_prices(self) -> list:
        """Get list of all product prices."""
        elements = self.page.locator(self.INVENTORY_ITEM_PRICE).all()
        return [el.text_content() for el in elements]
    
    def add_product_to_cart(self, product_name: str):
        """Add a specific product to cart by name."""
        # Format product name for data-test attribute
        formatted_name = product_name.lower().replace(" ", "-")
        selector = f"[data-test='add-to-cart-{formatted_name}']"
        self.click(selector)
        return self
    
    def add_backpack_to_cart(self):
        """Add Sauce Labs Backpack to cart."""
        self.click(self.BACKPACK_ADD)
        return self
    
    def add_bike_light_to_cart(self):
        """Add Sauce Labs Bike Light to cart."""
        self.click(self.BIKE_LIGHT_ADD)
        return self
    
    def add_bolt_shirt_to_cart(self):
        """Add Sauce Labs Bolt T-Shirt to cart."""
        self.click(self.BOLT_SHIRT_ADD)
        return self
    
    def remove_product_from_cart(self, product_name: str):
        """Remove a specific product from cart."""
        formatted_name = product_name.lower().replace(" ", "-")
        selector = f"[data-test='remove-{formatted_name}']"
        self.click(selector)
        return self
    
    def get_cart_badge_count(self) -> int:
        """Get the number shown on cart badge."""
        if self.is_visible(self.SHOPPING_CART_BADGE):
            text = self.get_text(self.SHOPPING_CART_BADGE)
            return int(text) if text else 0
        return 0
    
    def is_cart_badge_visible(self) -> bool:
        """Check if cart badge is visible."""
        return self.is_visible(self.SHOPPING_CART_BADGE)
    
    def go_to_cart(self):
        """Navigate to the shopping cart."""
        self.click(self.SHOPPING_CART_LINK)
        return self
    
    def sort_products(self, option: str):
        """Sort products by given option.
        
        Options:
        - 'az': Name (A to Z)
        - 'za': Name (Z to A)
        - 'lohi': Price (low to high)
        - 'hilo': Price (high to low)
        """
        self.page.select_option(self.SORT_DROPDOWN, option)
        return self
    
    def open_burger_menu(self):
        """Open the burger menu."""
        self.click(self.BURGER_MENU)
        return self
    
    def logout(self):
        """Logout from the application."""
        self.open_burger_menu()
        self.page.wait_for_selector(self.LOGOUT_LINK, state="visible")
        self.click(self.LOGOUT_LINK)
        return self
    
    def click_product_name(self, product_name: str):
        """Click on a product name to view details."""
        self.page.locator(self.INVENTORY_ITEM_NAME).filter(has_text=product_name).click()
        return self
