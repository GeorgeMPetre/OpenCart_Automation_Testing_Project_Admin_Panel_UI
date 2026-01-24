import pytest
from pages.admin_dashboard_page import AdminDashboardPage
from pages.admin_login_page import AdminLoginPage
from pages.admin_order_page import AdminOrderPage
from pages.admin_product_page import AdminProductPage
from utils.soft_assert import SoftAssert


@pytest.mark.admin
@pytest.mark.orders
@pytest.mark.ui
@pytest.mark.regression
class TestAdminOrderManagement:
    """Admin orders E2E tests: view order details, update status, and confirm it stays saved."""

    ADMIN_URL = "http://localhost/opencart/upload/admin/"
    ADMIN_USER = "admin"
    ADMIN_PASS = "admin"

    @pytest.fixture()
    def soft(self, driver, request) -> SoftAssert:
        """Soft assertion helper with logging/screenshots support."""
        return SoftAssert(driver, request)

    @pytest.fixture()
    def login(self, driver) -> AdminLoginPage:
        """Admin login page object."""
        return AdminLoginPage(driver)

    @pytest.fixture()
    def dashboard(self, driver) -> AdminDashboardPage:
        """Admin dashboard page object (menu navigation)."""
        return AdminDashboardPage(driver)

    @pytest.fixture()
    def products(self, driver) -> AdminProductPage:
        """Helper page object used only to close the login alert banner if it appears."""
        return AdminProductPage(driver)

    @pytest.fixture()
    def orders(self, driver) -> AdminOrderPage:
        """Admin orders page object (list + order view)."""
        return AdminOrderPage(driver)

    @pytest.fixture()
    def admin_orders(self, login, dashboard, products, orders) -> AdminOrderPage:
        """Logs in as admin and opens the Orders page, ready for test actions."""
        login.open(self.ADMIN_URL)
        login.login_as(self.ADMIN_USER, self.ADMIN_PASS)

        products.close_alert_if_present()
        dashboard.open_orders()

        return orders

    @pytest.mark.tc_id("ADMIN-ORD-001")
    @pytest.mark.functional
    def test_view_customer_order(self, admin_orders, soft):
        """Opens an order and checks basic customer and payment details are shown."""
        orders = admin_orders

        order_id = orders.get_first_order_id()
        soft.assert_true(order_id.isdigit(), f"Expected numeric order ID, got: {order_id}")

        orders.filter_by_order_id(order_id)
        soft.assert_true(orders.is_order_displayed(), f"Expected order ID {order_id} to be displayed")

        orders.open_order(order_id)

        soft.assert_equal(orders.get_customer_name(), "John Doe", "Expected customer name: John Doe")
        soft.assert_true(
            "Cash On Delivery" in orders.get_payment_method(),
            "Expected payment method to contain 'Cash On Delivery'",
        )
        soft.assert_all()

    @pytest.mark.tc_id("ADMIN-ORD-002")
    @pytest.mark.functional
    def test_update_order_status_to_shipped(self, admin_orders, dashboard, soft):
        """Updates an order status to Shipped and verifies it is saved in the list."""
        orders = admin_orders

        order_id = orders.get_first_order_id()
        soft.assert_true(order_id.isdigit(), f"Expected numeric order ID, got: {order_id}")

        orders.filter_by_order_id(order_id)
        soft.assert_true(
            orders.is_order_displayed(),
            f"Expected order ID {order_id} to be displayed before update",
        )

        orders.open_order(order_id)

        orders.set_order_status("Shipped")
        orders.save_history()
        soft.assert_true(orders.is_success_alert_displayed(), "Expected success alert after status update")

        dashboard.open_orders()

        soft.assert_equal(
            orders.get_order_status(order_id),
            "Shipped",
            "Expected order status to be 'Shipped'",
        )
        soft.assert_all()
