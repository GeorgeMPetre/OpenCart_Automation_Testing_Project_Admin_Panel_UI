import pytest
from pages.admin_login_page import AdminLoginPage
from pages.admin_dashboard_page import AdminDashboardPage
from pages.admin_order_page import AdminOrderPage
from pages.admin_product_page import AdminProductPage
from utils.soft_assert import SoftAssert


@pytest.mark.admin
@pytest.mark.functional
@pytest.mark.orders
class TestAdminOrderManagement:
    """
    Test suite for verifying order management functionalities in the OpenCart Admin Panel.
    Includes viewing order details and updating order status from the admin interface.
    """

    @pytest.mark.tc_id("ADMIN-ORD-001")
    @pytest.mark.ui
    @pytest.mark.regression
    @pytest.mark.functional
    def test_view_customer_order(self, driver, request):
        """
        Test Case: ADMIN-ORD-001
        Purpose: Verify that admin can view order details including customer name and payment method.
        """
        soft_assert = SoftAssert(driver, request)
        login_page = AdminLoginPage(driver)
        dashboard = AdminDashboardPage(driver)
        product_page = AdminProductPage(driver)
        order_page = AdminOrderPage(driver)

        login_page.open("http://localhost/opencart/upload/admin/")
        login_page.login_as("admin", "admin")
        product_page.close_alert_if_present()
        dashboard.go_to_orders_page()

        order_id = order_page.get_first_order_id()
        soft_assert.assert_true(order_id.isdigit(), f"Expected numeric order ID, got: {order_id}")

        order_page.filter_by_order_id(order_id)
        soft_assert.assert_true(order_page.is_order_displayed(),
                                f"Expected order ID {order_id} to be displayed")

        order_page.click_view_order(order_id)

        soft_assert.assert_equal(order_page.get_customer_name(), "John Doe", "Expected customer name: John Doe")
        soft_assert.assert_true(
            "Cash On Delivery" in order_page.get_payment_method(),
            f"Expected payment method to contain 'Cash On Delivery'"
        )
        soft_assert.assert_all()

    @pytest.mark.tc_id("ADMIN-ORD-002")
    @pytest.mark.ui
    @pytest.mark.regression
    @pytest.mark.functional
    def test_update_order_status_to_shipped(self, driver, request):
        """
        Test Case: ADMIN-ORD-002
        Purpose: Verify that admin can update the status of an order to 'Shipped' and confirm the change is saved.
        """
        soft_assert = SoftAssert(driver, request)
        login_page = AdminLoginPage(driver)
        dashboard = AdminDashboardPage(driver)
        product_page = AdminProductPage(driver)
        order_page = AdminOrderPage(driver)

        login_page.open("http://localhost/opencart/upload/admin/")
        login_page.login_as("admin", "admin")
        product_page.close_alert_if_present()
        dashboard.go_to_orders_page()

        order_id = order_page.get_first_order_id()
        soft_assert.assert_true(order_id.isdigit(), f"Expected numeric order ID, got: {order_id}")

        order_page.filter_by_order_id(order_id)
        soft_assert.assert_true(order_page.is_order_displayed(),
                                f"Expected order ID {order_id} to be displayed before update")

        order_page.click_view_order(order_id)

        order_page.select_order_status("Shipped")
        order_page.click_add_history()

        soft_assert.assert_true(order_page.is_success_alert_displayed(),
                                "Expected success alert after updating order status")

        dashboard.go_to_orders_page()

        soft_assert.assert_equal(order_page.get_order_status(order_id), "Shipped",
                                 "Expected order status to be 'Shipped'")

        soft_assert.assert_all()
