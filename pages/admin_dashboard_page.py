from selenium.webdriver.common.by import By
from utils.base_page import BaseAdminPage


class AdminDashboardPage(BaseAdminPage):
    """
    Page Object Model for the Admin Dashboard Page.
    Handles navigation to main admin sections.
    """

    # --- Menu Locators ---
    CATALOG_MENU = (By.ID, "menu-catalog")
    PRODUCTS_SUBMENU = (By.LINK_TEXT, "Products")
    SALES_MENU = (By.ID, "menu-sale")
    ORDERS_SUBMENU = (By.LINK_TEXT, "Orders")

    # --- Navigation ---
    def go_to_products_page(self):
        """Navigate to Product Management page."""

        self.click(self.CATALOG_MENU)
        self.click(self.PRODUCTS_SUBMENU)

    def go_to_orders_page(self):
        """Navigate to Order Management page."""

        self.click(self.SALES_MENU)
        self.click(self.ORDERS_SUBMENU)
