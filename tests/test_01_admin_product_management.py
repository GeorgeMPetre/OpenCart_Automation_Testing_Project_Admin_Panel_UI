import pytest
from pages.admin_dashboard_page import AdminDashboardPage
from pages.admin_login_page import AdminLoginPage
from pages.admin_product_page import AdminProductPage
from utils.soft_assert import SoftAssert


@pytest.mark.admin
@pytest.mark.products
@pytest.mark.ui
@pytest.mark.regression
class TestAdminProductManagement:
    """Admin product E2E tests: add, edit, and delete a product from the OpenCart admin panel."""

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
        """Admin products page object (list + product form)."""
        return AdminProductPage(driver)

    @pytest.fixture()
    def admin_products(self, login, dashboard, products) -> AdminProductPage:
        """Logs in as admin and opens the Products page, ready for test actions."""
        login.open(self.ADMIN_URL)
        login.login_as(self.ADMIN_USER, self.ADMIN_PASS)

        products.close_alert_if_present()
        dashboard.open_products()

        return products

    @pytest.mark.tc_id("ADMIN-PROD-001")
    @pytest.mark.functional
    def test_add_new_product(self, admin_products, soft):
        """Adds a new product and checks that OpenCart confirms the save."""
        products = admin_products

        name = "Apple Test Product Automation"
        meta_title = "Test Meta Title"

        products.open_add()

        products.set_name(name)
        products.set_meta_title(meta_title)
        products.set_description_ckeditor("input-description-1", "This is an automated test product.")
        products.set_meta_description("Automated meta description")
        products.set_meta_keywords("test, automation, opencart")
        products.set_tags("test, opencart")

        products.open_data_tab()
        products.set_model("MODEL-001")
        products.set_price("99.99")
        products.set_quantity(25)
        products.set_location("Warehouse 1")
        products.set_date_available("2025-08-01")
        products.set_stock_status("In Stock")
        products.set_status(True)

        products.open_links_tab()
        products.set_category("Desktops > Mac")

        products.open_seo_tab()
        products.set_seo_keyword("Keyword")

        products.save()

        msg = products.get_success_message_if_any()
        soft.assert_in("Success", msg, "Expected success message after adding product")
        soft.assert_all()

    @pytest.mark.tc_id("ADMIN-PROD-002")
    @pytest.mark.functional
    def test_edit_existing_product(self, admin_products, soft):
        """Edits an existing product and checks that the update is saved."""
        products = admin_products

        original_name = "Apple Test Product Automation"
        edited_name = "Test Product Automation - Edited"

        products.search_by_name(original_name)
        products.open_edit(original_name)

        products.set_name(edited_name)

        products.open_data_tab()
        products.set_price("129.99")
        products.set_quantity(50)

        products.save()

        msg = products.get_success_message_if_any()
        soft.assert_in("Success", msg, "Expected success message after editing product")
        soft.assert_all()

    @pytest.mark.tc_id("ADMIN-PROD-003")
    @pytest.mark.functional
    def test_delete_product(self, admin_products, soft):
        """Deletes the test product and checks that OpenCart confirms the deletion."""
        products = admin_products

        target_name = "Test Product Automation - Edited"

        products.search_by_name(target_name)

        products.select_row_checkbox(target_name)
        products.delete_selected()
        products.accept_delete_confirm()

        msg = products.get_success_message_if_any() or products.wait_success_message().text.strip()
        soft.assert_in("Success", msg, "Expected success message after deleting product")
        soft.assert_all()
