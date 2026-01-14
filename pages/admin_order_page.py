from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from utils.base_page import BaseAdminPage


class AdminOrderPage(BaseAdminPage):
    """
    Page Object Model for the Admin -> Sales -> Orders page.
    Provides actions for filtering orders, viewing order details,
    and updating order status.
    """

    """
    Locators used on the Admin Order Management page.
    """

    # -------------------------
    # List page filters & table
    # -------------------------
    ORDER_ID_FIELD = (By.ID, "input-order-id")
    """Input field used to filter orders by Order ID."""

    FILTER_BUTTON = (By.ID, "button-filter")
    """Button used to apply order filters."""

    ORDER_ROWS = (By.CSS_SELECTOR, "table tbody tr")
    """All rows displayed in the orders table."""

    LOADER = (By.CSS_SELECTOR, ".loader")
    """Loading indicator shown while order list is refreshing."""

    # -------------------------
    # Order view page elements
    # -------------------------
    CUSTOMER_NAME_CONTAINER = (By.ID, "customer-value")
    """Container displaying the customer name on the order view page."""

    PAYMENT_METHOD = (By.ID, "input-payment-method")
    """Field displaying the selected payment method."""

    ORDER_STATUS_SELECT = (By.ID, "input-order-status")
    """Dropdown used to select a new order status."""

    ADD_HISTORY_BUTTON = (By.ID, "button-history")
    """Button used to add order history and save status changes."""

    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert.alert-success")
    """Success alert shown after updating order status."""

    # -------------------------
    # Dynamic locators
    # -------------------------
    def _view_button_for_order(self, order_id):
        """Return locator for the View button of a specific order ID."""
        return (
            By.XPATH,
            f"//tr[td[contains(normalize-space(.), '{order_id}')]]//a[@title='View']",
        )

    def _status_cell_for_order(self, order_id):
        """Return locator for the status cell of a specific order row."""
        return (By.XPATH, f"//tr[td[text()='{order_id}']]/td[5]")

    # -------------------------
    # List page actions
    # -------------------------
    def filter_by_order_id(self, order_id):
        """Filter the order list using a specific Order ID."""
        self.type(self.ORDER_ID_FIELD, str(order_id))
        self.click(self.FILTER_BUTTON, scroll=False)
        if self.is_present(self.LOADER, timeout=1):
            self.wait_invisible(self.LOADER, timeout=10)
        self.get_all(self.ORDER_ROWS, timeout=10)

    def is_order_displayed(self):
        """Return True if at least one order is displayed in the table."""
        return self.is_present(self.ORDER_ROWS, timeout=2)

    def get_first_order_id(self):
        """Return the Order ID from the first row in the table."""
        first_id_cell = (By.CSS_SELECTOR, "table tbody tr td:nth-child(2)")
        return self.text_of(first_id_cell, timeout=10)

    def get_order_status(self, order_id):
        """Return the status text for a specific order."""
        return self.text_of(self._status_cell_for_order(order_id), timeout=10)

    def click_view_order(self, order_id):
        """Open the order details page for a specific Order ID."""
        self.scroll_to_top()
        self.js_click(self._view_button_for_order(order_id), timeout=10)
        self.wait_visible(self.CUSTOMER_NAME_CONTAINER, timeout=10)

    # -------------------------
    # Order view getters
    # -------------------------
    def get_customer_name(self):
        """Return the customer name from the order details page."""
        return self.text_of(self.CUSTOMER_NAME_CONTAINER, timeout=10)

    def get_payment_method(self):
        """Return the payment method used for the order."""
        return self.text_of(self.PAYMENT_METHOD, timeout=10)

    # -------------------------
    # Order status update
    # -------------------------
    def select_order_status(self, status_text):
        """Select a new order status from the status dropdown."""
        select_el = self.wait_visible(self.ORDER_STATUS_SELECT, timeout=10)
        Select(select_el).select_by_visible_text(status_text)

    def click_add_history(self):
        """Save the selected order status by adding order history."""
        self.click(self.ADD_HISTORY_BUTTON, timeout=10)

    def is_success_alert_displayed(self, timeout=5):
        """Return True if the success alert is visible."""
        return self.is_visible(self.SUCCESS_ALERT, timeout=timeout)
