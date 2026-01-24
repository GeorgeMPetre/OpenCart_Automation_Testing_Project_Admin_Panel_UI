from selenium.webdriver.common.by import By
from utils.base_page import BaseAdminPage


class AdminDashboardPage(BaseAdminPage):
    """Provides access to main admin sections like Products and Orders."""

    # ---------------------------
    # Menu locators
    # ---------------------------
    MENU_CATALOG = (By.ID, "menu-catalog")
    MENU_SALES = (By.ID, "menu-sale")

    PRODUCTS = (By.LINK_TEXT, "Products")
    ORDERS = (By.LINK_TEXT, "Orders")

    # ---------------------------
    # Navigation actions
    # ---------------------------
    def open_products(self) -> None:
        """Opens the Products management page from the admin menu."""
        self._open_menu(self.MENU_CATALOG)
        self.click(self.PRODUCTS)

    def open_orders(self) -> None:
        """Opens the Orders management page from the admin menu."""
        self._open_menu(self.MENU_SALES)
        self.click(self.ORDERS)

    # ---------------------------
    # Internal helpers
    # ---------------------------
    def _open_menu(self, menu_locator) -> None:
        """Expands a left-side admin menu section."""
        self.click(menu_locator)
