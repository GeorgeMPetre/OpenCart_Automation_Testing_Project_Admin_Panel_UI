from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from utils.base_page import BaseAdminPage


class AdminProductPage(BaseAdminPage):
    """
    Page Object Model for Admin -> Catalog -> Products page.
    Provides actions for managing products, including listing, filtering,
    creating, editing, deleting, and updating product details.
    """

    """
    Locators used on the Admin -> Catalog -> Products page.
    """

    # -------------------------
    # Global actions / alerts
    # -------------------------
    ALERT_CLOSE_BUTTON = (
        By.XPATH,
        "//button[@type='button' and contains(@class,'btn-close')]",
    )
    """Close button for success or warning alerts."""

    ADD_PRODUCT_BUTTON = (By.CSS_SELECTOR, "a[title='Add New']")
    """Button used to open the Add Product form."""

    SAVE_BUTTON = (By.XPATH, "//button[@form='form-product' and @type='submit']")
    """Button used to save product changes."""

    DELETE_BUTTON = (By.CSS_SELECTOR, "button[formaction*='product|delete']")
    """Button used to delete selected products."""

    # -------------------------
    # Product list & filtering
    # -------------------------
    PRODUCT_TABLE_ROWS = (By.CSS_SELECTOR, "#product table.table tbody tr")
    """All rows displayed in the product list table."""

    PRODUCT_FORM = (By.ID, "form-product")
    """Main product form container used for add/edit actions."""

    FILTER_PANEL = (By.ID, "filter-product")
    """Filter panel container for product search."""

    FILTER_TOGGLE_BUTTON = (By.CSS_SELECTOR, "button[title='Filter']")
    """Button used to show or hide the filter panel."""

    FILTER_NAME_INPUT = (By.ID, "input-name")
    """Input field for filtering products by name."""

    FILTER_APPLY_BUTTON = (By.ID, "button-filter")
    """Button used to apply product filters."""

    # -------------------------
    # General tab fields
    # -------------------------
    PRODUCT_NAME = (By.ID, "input-name-1")
    """Input field for the product name."""

    META_TITLE = (By.ID, "input-meta-title-1")
    """Input field for the product meta title."""

    META_DESCRIPTION = (By.ID, "input-meta-description-1")
    """Input field for the product meta description."""

    META_KEYWORDS = (By.ID, "input-meta-keyword-1")
    """Input field for the product meta keywords."""

    TAGS = (By.ID, "input-tag-1")
    """Input field for product tags."""

    STATUS_CHECKBOX = (By.ID, "input-status")
    """Checkbox used to enable or disable the product."""

    # -------------------------
    # Tabs
    # -------------------------
    DATA_TAB = (By.CSS_SELECTOR, "a[href='#tab-data']")
    """Tab used to open the Data section."""

    LINKS_TAB = (By.CSS_SELECTOR, "a[href='#tab-links']")
    """Tab used to open the Links section."""

    SEO_TAB = (By.CSS_SELECTOR, "a[href='#tab-seo']")
    """Tab used to open the SEO section."""

    TAB_DATA = (By.ID, "tab-data")
    """Container for Data tab content."""

    TAB_LINKS = (By.ID, "tab-links")
    """Container for Links tab content."""

    TAB_SEO = (By.ID, "tab-seo")
    """Container for SEO tab content."""

    # -------------------------
    # Data tab fields
    # -------------------------
    MODEL = (By.ID, "input-model")
    """Input field for the product model."""

    PRICE = (By.ID, "input-price")
    """Input field for the product price."""

    QUANTITY = (By.ID, "input-quantity")
    """Input field for the product quantity."""

    LOCATION = (By.ID, "input-location")
    """Input field for the product location."""

    DATE_AVAILABLE = (By.ID, "input-date-available")
    """Input field for the product availability date."""

    STOCK_STATUS = (By.ID, "input-stock-status")
    """Dropdown used to select product stock status."""

    # -------------------------
    # Links tab fields
    # -------------------------
    CATEGORY_FIELD = (By.ID, "input-category")
    """Autocomplete input used to assign product categories."""

    # -------------------------
    # SEO tab fields
    # -------------------------
    SEO_KEYWORD = (By.ID, "input-keyword-0-1")
    """Input field for the product SEO keyword."""


    # -------------------------
    # Internal helpers
    # -------------------------
    def _rows(self, timeout=None):
        """Return all product table rows."""
        return self.get_all(self.PRODUCT_TABLE_ROWS, timeout=timeout)

    def _find_row_by_product_name(self, product_name, timeout=10):
        """Find and return a product row matching the given product name."""
        needle = (product_name or "").strip().lower()
        for row in self._rows(timeout=timeout):
            if needle and needle in row.text.lower():
                return row
        return None

    def _filter_panel_is_collapsed(self):
        """Check whether the filter panel is currently collapsed."""
        panel = self.wait_present(self.FILTER_PANEL, timeout=5)
        classes = panel.get_attribute("class") or ""
        return "d-none" in classes

    def _open_filter_panel_if_needed(self):
        """Open the filter panel if it is currently collapsed."""
        if self._filter_panel_is_collapsed():
            self.click(self.FILTER_TOGGLE_BUTTON, timeout=5, scroll=False)
            self._wait(timeout=5).until(lambda d: not self._filter_panel_is_collapsed())

    def _toggle_checkbox(self, locator, enable=True):
        """Enable or disable a checkbox based on the desired state."""
        checkbox = self.wait_present(locator)
        self.scroll_into_view(checkbox)
        current = checkbox.is_selected()
        if current != enable:
            checkbox.click()

    # -------------------------
    # Page actions (List page)
    # -------------------------
    def click_add_product(self):
        """Open the Add Product form."""
        self.click(self.ADD_PRODUCT_BUTTON)
        self.wait_visible(self.PRODUCT_FORM)

    def search_product(self, product_name):
        """Filter products by name and wait for results to load."""
        self._open_filter_panel_if_needed()
        self.type(self.FILTER_NAME_INPUT, product_name)
        self.click(self.FILTER_APPLY_BUTTON, scroll=False)
        self._rows(timeout=10)

    def click_edit_button_for_product(self, product_name):
        """Open the Edit form for the specified product."""
        row = self._find_row_by_product_name(product_name)
        if not row:
            raise AssertionError(f"Product '{product_name}' not found in product list.")
        edit_btn = row.find_element(By.CSS_SELECTOR, "a.btn.btn-primary[title='Edit']")
        self.scroll_into_view(edit_btn)
        try:
            edit_btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", edit_btn)
        self.wait_visible(self.PRODUCT_FORM)

    def select_product_checkbox(self, product_name):
        """Select the checkbox for a specific product row."""
        row = self._find_row_by_product_name(product_name)
        if not row:
            raise AssertionError(f"Product '{product_name}' not found in product list for deletion.")
        checkbox = row.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
        self.scroll_into_view(checkbox)
        if not checkbox.is_selected():
            checkbox.click()

    def click_delete_product(self):
        """Click the Delete button to remove selected products."""
        self.click(self.DELETE_BUTTON)

    def go_to_page_two(self):
        """Navigate to the second page of the product list."""
        wait = WebDriverWait(self.driver, 10)
        first_row = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#product table.table tbody tr")
            )
        )
        page_two = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "ul.pagination li.page-item a.page-link[href*='page=2']")
            )
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", page_two
        )
        self.driver.execute_script("arguments[0].click();", page_two)
        wait.until(EC.staleness_of(first_row))
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#product table.table tbody tr")
            )
        )

    # -------------------------
    # Form actions
    # -------------------------
    def save_product(self):
        """Save the product form."""
        self.scroll_to_top()
        self.wait_present(self.PRODUCT_FORM)
        self.click(self.SAVE_BUTTON)

    def close_success_alert_if_present(self, timeout=2):
        """Close the success alert if it is visible."""
        if not self.is_clickable(self.ALERT_CLOSE_BUTTON, timeout=timeout):
            return False
        self.click(self.ALERT_CLOSE_BUTTON, timeout=timeout)
        return True

    # -------------------------
    # General Tab setters
    # -------------------------
    def set_product_name(self, name):
        """Set the product name."""
        self.type(self.PRODUCT_NAME, name)

    def set_meta_title(self, title):
        """Set the product meta title."""
        self.type(self.META_TITLE, title)

    def set_meta_description(self, text):
        """Set the product meta description."""
        self.type(self.META_DESCRIPTION, text)

    def set_meta_keywords(self, text):
        """Set the product meta keywords."""
        self.type(self.META_KEYWORDS, text)

    def set_tags(self, tags):
        """Set product tags."""
        self.type(self.TAGS, tags)

    def set_status(self, enabled=True):
        """Enable or disable the product status."""
        self._toggle_checkbox(self.STATUS_CHECKBOX, enable=enabled)

    def set_description_with_ckeditor(self, textarea_id, text):
        """Set product description using CKEditor."""
        self.driver.execute_script(
            "CKEDITOR.instances[arguments[0]].setData(arguments[1]);",
            textarea_id,
            text,
        )

    # -------------------------
    # Tabs
    # -------------------------
    def switch_to_data_tab(self):
        """Switch to the Data tab."""
        self.click(self.DATA_TAB)
        self.wait_visible(self.TAB_DATA)

    def switch_to_links_tab(self):
        """Switch to the Links tab."""
        self.click(self.LINKS_TAB)
        self.wait_visible(self.TAB_LINKS)

    def switch_to_seo_tab(self):
        """Switch to the SEO tab."""
        self.click(self.SEO_TAB)
        self.wait_visible(self.TAB_SEO)

    # -------------------------
    # Data Tab setters
    # -------------------------
    def set_model(self, model):
        """Set the product model."""
        self.type(self.MODEL, model)

    def set_price(self, price):
        """Set the product price."""
        self.type(self.PRICE, price)

    def set_quantity(self, qty):
        """Set the product quantity."""
        self.type(self.QUANTITY, str(qty))

    def set_location(self, location):
        """Set the product location."""
        self.type(self.LOCATION, location)

    def set_date_available(self, date_str):
        """Set the product availability date."""
        self.type(self.DATE_AVAILABLE, date_str)

    def set_stock_status(self, status_text):
        """Select the product stock status."""
        select_el = self.wait_visible(self.STOCK_STATUS)
        Select(select_el).select_by_visible_text(status_text)

    # -------------------------
    # Links Tab
    # -------------------------
    def select_category(self, category_name):
        """Select a product category using autocomplete."""
        field = self.wait_visible(self.CATEGORY_FIELD)
        self.scroll_into_view(field)
        field.clear()
        field.send_keys(category_name)
        field.send_keys(Keys.TAB)
        self._wait().until(lambda d: (field.get_attribute("value") or "").strip() == category_name)

    # -------------------------
    # SEO Tab
    # -------------------------
    def set_seo_keyword(self, keyword):
        """Set the SEO keyword for the product."""
        self.type(self.SEO_KEYWORD, keyword)
