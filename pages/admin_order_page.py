from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from utils.base_page import BaseAdminPage


class AdminOrderPage(BaseAdminPage):
    """Admin Orders page: filter orders, open an order, read details, and update status."""

    # -------------------------
    # List page
    # -------------------------
    ORDER_ID = (By.ID, "input-order-id")
    FILTER = (By.ID, "button-filter")
    ROWS = (By.CSS_SELECTOR, "table tbody tr")
    LOADER = (By.CSS_SELECTOR, ".loader")

    FIRST_ROW_ORDER_ID = (By.CSS_SELECTOR, "table tbody tr td:nth-child(2)")

    # -------------------------
    # View page
    # -------------------------
    CUSTOMER_NAME = (By.ID, "customer-value")
    PAYMENT_METHOD = (By.ID, "input-payment-method")

    ORDER_STATUS = (By.ID, "input-order-status")
    ADD_HISTORY = (By.ID, "button-history")
    ALERT_SUCCESS = (By.CSS_SELECTOR, ".alert.alert-success")

    # -------------------------
    # Dynamic locators
    # -------------------------
    @staticmethod
    def view_button(order_id: str) -> tuple:
        """Locator for the View button in the row that contains the given order id."""
        return (
            By.XPATH,
            f"//tr[td[contains(normalize-space(.), '{order_id}')]]//a[@title='View']",
        )

    @staticmethod
    def status_cell(order_id: str) -> tuple:
        """Locator for the Status cell in the row for the given order id."""
        return (By.XPATH, f"//tr[td[text()='{order_id}']]/td[5]")

    # -------------------------
    # List actions
    # -------------------------
    def filter_by_order_id(self, order_id: str | int) -> None:
        """Filters the orders list by order id."""
        self.type(self.ORDER_ID, str(order_id))
        self.click(self.FILTER, scroll=False)
        self._wait_for_list_refresh()

    def is_order_displayed(self) -> bool:
        """True when the list shows at least one result row."""
        return self.is_present(self.ROWS, timeout=2)

    def get_first_order_id(self) -> str:
        """Returns the order id from the first row in the current list."""
        return self.text_of(self.FIRST_ROW_ORDER_ID, timeout=10)

    def get_order_status(self, order_id: str | int) -> str:
        """Returns the status shown in the list for a given order id."""
        return self.text_of(self.status_cell(str(order_id)), timeout=10)

    def open_order(self, order_id: str | int) -> None:
        """Opens the order view page for the given order id."""
        self.scroll_to_top()
        self.js_click(self.view_button(str(order_id)), timeout=10)
        self.wait_visible(self.CUSTOMER_NAME, timeout=10)

    # -------------------------
    # View getters
    # -------------------------
    def get_customer_name(self) -> str:
        """Returns the customer name shown on the order view page."""
        return self.text_of(self.CUSTOMER_NAME, timeout=10)

    def get_payment_method(self) -> str:
        """Returns the payment method shown on the order view page."""
        return self.text_of(self.PAYMENT_METHOD, timeout=10)

    # -------------------------
    # Status update
    # -------------------------
    def set_order_status(self, status_text: str) -> None:
        """Selects a new status in the order status dropdown."""
        select_el = self.wait_visible(self.ORDER_STATUS, timeout=10)
        Select(select_el).select_by_visible_text(status_text)

    def save_history(self) -> None:
        """Clicks Add History to save the current status change."""
        self.click(self.ADD_HISTORY, timeout=10)

    def is_success_alert_displayed(self, timeout: int = 5) -> bool:
        """True when the success alert is visible."""
        return self.is_visible(self.ALERT_SUCCESS, timeout=timeout)

    # -------------------------
    # Internal helpers
    # -------------------------
    def _wait_for_list_refresh(self) -> None:
        """Waits for the loader to disappear and the rows to be available."""
        if self.is_present(self.LOADER, timeout=1):
            self.wait_invisible(self.LOADER, timeout=10)
        self.get_all(self.ROWS, timeout=10)
