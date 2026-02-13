"""
Cart Page object for Swag Labs.
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class CartPage(BasePage):
    """Page object for the Swag Labs shopping cart page."""
    
    # Locators
    CART_LIST = ".cart_list"
    CART_ITEM = ".cart_item"
    CART_ITEM_NAME = ".inventory_item_name"
    CART_ITEM_PRICE = ".inventory_item_price"
    CART_ITEM_QUANTITY = ".cart_quantity"
    REMOVE_BUTTON = "[data-test^='remove']"
    CONTINUE_SHOPPING_BUTTON = "[data-test='continue-shopping']"
    CHECKOUT_BUTTON = "[data-test='checkout']"
    PAGE_TITLE = ".title"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def is_cart_page_displayed(self) -> bool:
        """Verify cart page is displayed."""
        return self.is_visible(self.CART_LIST)
    
    def get_page_title(self) -> str:
        """Get the page title."""
        return self.get_text(self.PAGE_TITLE)
    
    def get_cart_item_count(self) -> int:
        """Get the number of items in cart."""
        return self.page.locator(self.CART_ITEM).count()
    
    def get_cart_item_names(self) -> list:
        """Get list of all item names in cart."""
        elements = self.page.locator(self.CART_ITEM_NAME).all()
        return [el.text_content() for el in elements]
    
    def get_cart_item_prices(self) -> list:
        """Get list of all item prices in cart."""
        elements = self.page.locator(self.CART_ITEM_PRICE).all()
        return [el.text_content() for el in elements]
    
    def remove_item(self, product_name: str):
        """Remove a specific item from cart."""
        formatted_name = product_name.lower().replace(" ", "-")
        selector = f"[data-test='remove-{formatted_name}']"
        self.click(selector)
        return self
    
    def continue_shopping(self):
        """Click continue shopping button."""
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        return self
    
    def proceed_to_checkout(self):
        """Click checkout button."""
        self.click(self.CHECKOUT_BUTTON)
        return self
    
    def is_item_in_cart(self, product_name: str) -> bool:
        """Check if a specific item is in the cart."""
        items = self.get_cart_item_names()
        return product_name in items
    
    def is_cart_empty(self) -> bool:
        """Check if the cart is empty."""
        return self.get_cart_item_count() == 0
