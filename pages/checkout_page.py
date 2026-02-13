"""
Checkout Page objects for Swag Labs.
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page object for the Swag Labs checkout pages."""
    
    # Step One - Customer Information
    FIRST_NAME_INPUT = "[data-test='firstName']"
    LAST_NAME_INPUT = "[data-test='lastName']"
    POSTAL_CODE_INPUT = "[data-test='postalCode']"
    CONTINUE_BUTTON = "[data-test='continue']"
    CANCEL_BUTTON = "[data-test='cancel']"
    ERROR_MESSAGE = "[data-test='error']"
    
    # Step Two - Overview
    SUMMARY_INFO = ".summary_info"
    SUMMARY_SUBTOTAL = ".summary_subtotal_label"
    SUMMARY_TAX = ".summary_tax_label"
    SUMMARY_TOTAL = ".summary_total_label"
    FINISH_BUTTON = "[data-test='finish']"
    CART_ITEM = ".cart_item"
    ITEM_TOTAL_LABEL = ".summary_subtotal_label"
    
    # Complete
    COMPLETE_HEADER = ".complete-header"
    COMPLETE_TEXT = ".complete-text"
    BACK_HOME_BUTTON = "[data-test='back-to-products']"
    PONY_EXPRESS_IMAGE = ".pony_express"
    
    PAGE_TITLE = ".title"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def get_page_title(self) -> str:
        """Get the page title."""
        return self.get_text(self.PAGE_TITLE)
    
    # ============== Step One Methods ==============
    
    def enter_first_name(self, first_name: str):
        """Enter first name."""
        self.fill(self.FIRST_NAME_INPUT, first_name)
        return self
    
    def enter_last_name(self, last_name: str):
        """Enter last name."""
        self.fill(self.LAST_NAME_INPUT, last_name)
        return self
    
    def enter_postal_code(self, postal_code: str):
        """Enter postal code."""
        self.fill(self.POSTAL_CODE_INPUT, postal_code)
        return self
    
    def fill_customer_info(self, first_name: str, last_name: str, postal_code: str):
        """Fill all customer information fields."""
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
        return self
    
    def click_continue(self):
        """Click continue button."""
        self.click(self.CONTINUE_BUTTON)
        return self
    
    def click_cancel(self):
        """Click cancel button."""
        self.click(self.CANCEL_BUTTON)
        return self
    
    def get_error_message(self) -> str:
        """Get error message if displayed."""
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def is_error_displayed(self) -> bool:
        """Check if error message is displayed."""
        return self.is_visible(self.ERROR_MESSAGE)
    
    # ============== Step Two (Overview) Methods ==============
    
    def is_overview_page_displayed(self) -> bool:
        """Check if checkout overview page is displayed."""
        return self.is_visible(self.SUMMARY_INFO)
    
    def get_subtotal(self) -> str:
        """Get the subtotal text."""
        return self.get_text(self.SUMMARY_SUBTOTAL)
    
    def get_tax(self) -> str:
        """Get the tax text."""
        return self.get_text(self.SUMMARY_TAX)
    
    def get_total(self) -> str:
        """Get the total text."""
        return self.get_text(self.SUMMARY_TOTAL)
    
    def get_overview_item_count(self) -> int:
        """Get the number of items in checkout overview."""
        return self.page.locator(self.CART_ITEM).count()
    
    def click_finish(self):
        """Click finish button to complete the order."""
        self.click(self.FINISH_BUTTON)
        return self
    
    # ============== Complete Page Methods ==============
    
    def is_order_complete(self) -> bool:
        """Check if order completion page is displayed."""
        return self.is_visible(self.COMPLETE_HEADER)
    
    def get_complete_header(self) -> str:
        """Get the completion header text."""
        return self.get_text(self.COMPLETE_HEADER)
    
    def get_complete_text(self) -> str:
        """Get the completion message text."""
        return self.get_text(self.COMPLETE_TEXT)
    
    def click_back_home(self):
        """Click back home button."""
        self.click(self.BACK_HOME_BUTTON)
        return self
