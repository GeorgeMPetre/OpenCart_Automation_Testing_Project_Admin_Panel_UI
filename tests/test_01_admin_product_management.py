import pytest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.admin_login_page import AdminLoginPage
from pages.admin_dashboard_page import AdminDashboardPage
from pages.admin_product_page import AdminProductPage
from utils.soft_assert import SoftAssert


@pytest.mark.admin
@pytest.mark.functional
@pytest.mark.products
class TestAdminProductManagement:
    """
    Test suite for validating product management functionality in the OpenCart Admin Panel.
    Includes adding, editing, and deleting products using the Admin interface.
    """

    @pytest.mark.tc_id("ADMIN-PROD-001")
    @pytest.mark.ui
    @pytest.mark.regression
    @pytest.mark.functional
    def test_add_new_product(self, driver, request):
        """
        Test Case: ADMIN-PROD-001
        Purpose: Verify that a new product can be successfully added via the admin panel.
        """
        soft_assert = SoftAssert(driver, request)
        login_page = AdminLoginPage(driver)
        dashboard = AdminDashboardPage(driver)
        product_page = AdminProductPage(driver)

        login_page.open("http://localhost/opencart/upload/admin/")
        login_page.login_as("admin", "admin")
        product_page.close_alert_if_present()
        dashboard.go_to_products_page()

        product_page.click_add_product()
        product_page.set_product_name("Apple Test Product Automation")
        product_page.set_meta_title("Test Meta Title")
        product_page.set_description_with_ckeditor("input-description-1", "This is an automated test product.")
        product_page.set_meta_description("Automated meta description")
        product_page.set_meta_keywords("test, automation, opencart")
        product_page.set_tags("test, opencart")

        product_page.switch_to_data_tab()
        product_page.set_model("MODEL-001")
        product_page.set_price("99.99")
        product_page.set_quantity("25")
        product_page.set_location("Warehouse 1")
        product_page.set_date_available("2025-08-01")
        product_page.set_stock_status("In Stock")

        product_page.switch_to_links_tab()
        product_page.select_category("Desktops > Mac")

        product_page.switch_to_data_tab()
        product_page.set_status(True)

        product_page.switch_to_seo_tab()
        product_page.set_seo_keyword("Keyword")

        product_page.save_product()
        success_message = product_page.get_success_message_if_any()

        soft_assert.assert_in("Success", success_message, "Expected success message after adding product")
        soft_assert.assert_all()

    @pytest.mark.tc_id("ADMIN-PROD-002")
    @pytest.mark.ui
    @pytest.mark.regression
    @pytest.mark.functional
    def test_edit_existing_product(self, driver, request):
        """
        Test Case: ADMIN-PROD-002
        Purpose: Verify that an existing product can be edited and saved successfully.
        """
        soft_assert = SoftAssert(driver, request)
        login_page = AdminLoginPage(driver)
        dashboard = AdminDashboardPage(driver)
        product_page = AdminProductPage(driver)

        login_page.open("http://localhost/opencart/upload/admin/")
        login_page.login_as("admin", "admin")
        product_page.close_alert_if_present()
        dashboard.go_to_products_page()

        product_page.click_edit_button_for_product("Apple Test Product Automation")
        product_page.set_product_name("Test Product Automation - Edited")

        product_page.switch_to_data_tab()
        product_page.set_price("129.99")
        product_page.set_quantity("50")

        product_page.save_product()

        success_message = product_page.get_success_message_if_any()

        soft_assert.assert_in("Success", success_message, "Expected success message after editing product")
        soft_assert.assert_all()

    @pytest.mark.tc_id("ADMIN-PROD-003")
    @pytest.mark.ui
    @pytest.mark.regression
    @pytest.mark.functional
    def test_delete_product(self, driver, request):
        """
        Test Case: ADMIN-PROD-003
        Purpose: Verify that an existing product can be selected and deleted successfully.
        """
        soft_assert = SoftAssert(driver, request)
        login_page = AdminLoginPage(driver)
        dashboard = AdminDashboardPage(driver)
        product_page = AdminProductPage(driver)

        login_page.open("http://localhost/opencart/upload/admin/")
        login_page.login_as("admin", "admin")
        product_page.close_alert_if_present()
        dashboard.go_to_products_page()

        product_page.go_to_page_two()
        product_page.select_product_checkbox("Test Product Automation - Edited")
        product_page.click_delete_product()

        WebDriverWait(driver, 5).until(EC.alert_is_present())
        driver.switch_to.alert.accept()

        success_message = product_page.wait_success_message().text.strip()


        soft_assert.assert_in("Success", success_message, "Expected success message after deleting product")
        soft_assert.assert_all()
