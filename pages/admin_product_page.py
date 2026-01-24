from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from utils.base_page import BaseAdminPage


class AdminProductPage(BaseAdminPage):
    """Admin Products page: search/filter the list, open add/edit, update fields, and save/delete."""

    # -------------------------
    # Alerts / global actions
    # -------------------------
    ALERT_CLOSE = (By.XPATH, "//button[@type='button' and contains(@class,'btn-close')]")
    ALERT_SUCCESS = (By.CSS_SELECTOR, "div.alert-success")

    ADD_NEW = (By.CSS_SELECTOR, "a[title='Add New']")
    SAVE = (By.XPATH, "//button[@form='form-product' and @type='submit']")
    DELETE = (By.CSS_SELECTOR, "button[formaction*='product|delete']")

    # -------------------------
    # List page: table, filter, paging
    # -------------------------
    PRODUCT_FORM = (By.ID, "form-product")
    TABLE_ROWS = (By.CSS_SELECTOR, "#product table.table tbody tr")

    FILTER_PANEL = (By.ID, "filter-product")
    FILTER_TOGGLE = (By.CSS_SELECTOR, "button[title='Filter'], a[title='Filter']")
    FILTER_NAME = (By.ID, "input-name")
    FILTER_APPLY = (By.ID, "button-filter")

    PAGE_2 = (By.CSS_SELECTOR, "ul.pagination li.page-item a.page-link[href*='page=2']")

    # -------------------------
    # Tabs
    # -------------------------
    TAB_DATA_LINK = (By.CSS_SELECTOR, "a[href='#tab-data']")
    TAB_LINKS_LINK = (By.CSS_SELECTOR, "a[href='#tab-links']")
    TAB_SEO_LINK = (By.CSS_SELECTOR, "a[href='#tab-seo']")

    TAB_DATA = (By.ID, "tab-data")
    TAB_LINKS = (By.ID, "tab-links")
    TAB_SEO = (By.ID, "tab-seo")

    # -------------------------
    # General tab fields
    # -------------------------
    NAME = (By.ID, "input-name-1")
    META_TITLE = (By.ID, "input-meta-title-1")
    META_DESCRIPTION = (By.ID, "input-meta-description-1")
    META_KEYWORDS = (By.ID, "input-meta-keyword-1")
    TAGS = (By.ID, "input-tag-1")
    STATUS = (By.ID, "input-status")

    # -------------------------
    # Data tab fields
    # -------------------------
    MODEL = (By.ID, "input-model")
    PRICE = (By.ID, "input-price")
    QUANTITY = (By.ID, "input-quantity")
    LOCATION = (By.ID, "input-location")
    DATE_AVAILABLE = (By.ID, "input-date-available")
    STOCK_STATUS = (By.ID, "input-stock-status")

    # -------------------------
    # Links tab fields
    # -------------------------
    CATEGORY = (By.ID, "input-category")

    # -------------------------
    # SEO tab fields
    # -------------------------
    SEO_KEYWORD = (By.ID, "input-keyword-0-1")

    # -------------------------
    # List actions
    # -------------------------
    def open_add(self) -> None:
        """Opens the Add Product form."""
        self.click(self.ADD_NEW)
        self.wait_visible(self.PRODUCT_FORM)

    def search_by_name(self, name: str) -> None:
        """Filters the product list by product name."""
        self.scroll_to_top()
        self._ensure_filter_panel_open()

        self.type(self.FILTER_NAME, name)
        self.click(self.FILTER_APPLY, scroll=False)
        self._wait_for_rows()

    def open_edit(self, product_name: str) -> None:
        """Opens the Edit form for the first row that matches the product name."""
        row = self._find_row(product_name)
        if not row:
            raise AssertionError(f"Product not found: {product_name}")

        edit = row.find_element(By.CSS_SELECTOR, "a.btn.btn-primary[title='Edit']")
        self.scroll_into_view(edit)
        self._safe_click_element(edit)
        self.wait_visible(self.PRODUCT_FORM)

    def select_row_checkbox(self, product_name: str) -> None:
        """Selects the checkbox for the first row that matches the product name."""
        row = self._find_row(product_name)
        if not row:
            raise AssertionError(f"Product not found for selection: {product_name}")

        checkbox = row.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
        self.scroll_into_view(checkbox)
        if not checkbox.is_selected():
            checkbox.click()

    def delete_selected(self) -> None:
        """Clicks Delete for currently selected rows."""
        self.click(self.DELETE)

    def accept_delete_confirm(self, timeout: int = 5) -> None:
        """Accepts the browser confirm alert after clicking Delete."""
        WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()

    def go_to_page_two(self) -> None:
        """Navigates to page 2 and waits for the list to refresh."""
        first = self.wait_present(self.TABLE_ROWS, timeout=10)
        page_2 = self.wait_present(self.PAGE_2, timeout=10)

        self.scroll_into_view(page_2)
        self._safe_click_element(page_2)

        WebDriverWait(self.driver, 10).until(EC.staleness_of(first))
        self.wait_present(self.TABLE_ROWS, timeout=10)

    # -------------------------
    # Form actions
    # -------------------------
    def save(self) -> None:
        """Saves the product form."""
        self.scroll_to_top()
        self.wait_present(self.PRODUCT_FORM)
        self.click(self.SAVE)

    def close_alert_if_present(self, timeout: int = 2) -> bool:
        """Closes the top alert if it appears."""
        if not self.is_clickable(self.ALERT_CLOSE, timeout=timeout):
            return False
        self.click(self.ALERT_CLOSE, timeout=timeout)
        return True

    def get_success_message_if_any(self, timeout: int = 3) -> str:
        """Returns the success banner text, or an empty string if not shown."""
        if not self.is_visible(self.ALERT_SUCCESS, timeout=timeout):
            return ""
        return self.wait_visible(self.ALERT_SUCCESS, timeout=timeout).text.strip()

    def wait_success_message(self, timeout: int = 10):
        """Waits for the success banner to appear and returns it."""
        return self.wait_visible(self.ALERT_SUCCESS, timeout=timeout)

    # -------------------------
    # General tab setters
    # -------------------------
    def set_name(self, value: str) -> None:
        """Sets the product name."""
        self.type(self.NAME, value)

    def set_meta_title(self, value: str) -> None:
        """Sets the meta title (required by many themes)."""
        self.type(self.META_TITLE, value)

    def set_meta_description(self, value: str) -> None:
        """Sets the meta description."""
        self.type(self.META_DESCRIPTION, value)

    def set_meta_keywords(self, value: str) -> None:
        """Sets the meta keywords."""
        self.type(self.META_KEYWORDS, value)

    def set_tags(self, value: str) -> None:
        """Sets product tags."""
        self.type(self.TAGS, value)

    def set_status(self, enabled: bool = True) -> None:
        """Enables or disables product status."""
        self._set_checkbox(self.STATUS, enabled)

    def set_description_ckeditor(self, textarea_id: str, value: str) -> None:
        """Sets the CKEditor description by textarea id."""
        self.driver.execute_script(
            "CKEDITOR.instances[arguments[0]].setData(arguments[1]);",
            textarea_id,
            value,
        )

    # -------------------------
    # Tabs
    # -------------------------
    def open_data_tab(self) -> None:
        """Opens the Data tab."""
        self.click(self.TAB_DATA_LINK)
        self.wait_visible(self.TAB_DATA)

    def open_links_tab(self) -> None:
        """Opens the Links tab."""
        self.click(self.TAB_LINKS_LINK)
        self.wait_visible(self.TAB_LINKS)

    def open_seo_tab(self) -> None:
        """Opens the SEO tab."""
        self.click(self.TAB_SEO_LINK)
        self.wait_visible(self.TAB_SEO)

    # -------------------------
    # Data tab setters
    # -------------------------
    def set_model(self, value: str) -> None:
        """Sets product model."""
        self.type(self.MODEL, value)

    def set_price(self, value: str) -> None:
        """Sets product price."""
        self.type(self.PRICE, value)

    def set_quantity(self, value) -> None:
        """Sets stock quantity."""
        self.type(self.QUANTITY, str(value))

    def set_location(self, value: str) -> None:
        """Sets product location."""
        self.type(self.LOCATION, value)

    def set_date_available(self, value: str) -> None:
        """Sets the date available."""
        self.type(self.DATE_AVAILABLE, value)

    def set_stock_status(self, visible_text: str) -> None:
        """Selects a stock status from the dropdown."""
        el = self.wait_visible(self.STOCK_STATUS)
        Select(el).select_by_visible_text(visible_text)

    # -------------------------
    # Links tab
    # -------------------------
    def set_category(self, category_name: str) -> None:
        """Types a category name and confirms it with TAB."""
        field = self.wait_visible(self.CATEGORY)
        self.scroll_into_view(field)
        field.clear()
        field.send_keys(category_name)
        field.send_keys(Keys.TAB)

        self._wait().until(lambda d: (field.get_attribute("value") or "").strip() == category_name)

    # -------------------------
    # SEO tab
    # -------------------------
    def set_seo_keyword(self, value: str) -> None:
        """Sets the SEO keyword."""
        self.type(self.SEO_KEYWORD, value)

    # -------------------------
    # Internal helpers
    # -------------------------
    def _wait_for_rows(self, timeout: int = 10) -> None:
        """Waits until the products table has rows (or is fully refreshed)."""
        self.get_all(self.TABLE_ROWS, timeout=timeout)

    def _rows(self, timeout: int = 10):
        """Returns all product table rows."""
        return self.get_all(self.TABLE_ROWS, timeout=timeout)

    def _find_row(self, product_name: str, timeout: int = 10):
        """Finds the first row that contains the given product name."""
        needle = (product_name or "").strip().lower()
        if not needle:
            return None

        for row in self._rows(timeout=timeout):
            try:
                if needle in row.text.lower():
                    return row
            except StaleElementReferenceException:
                continue
        return None

    def _ensure_filter_panel_open(self) -> None:
        """Opens the filter panel when it is collapsed (theme-safe)."""
        panel = self.wait_present(self.FILTER_PANEL, timeout=10)

        if panel.is_displayed():
            return

        if self.is_present(self.FILTER_TOGGLE, timeout=2):
            self.js_click(self.FILTER_TOGGLE, timeout=5)
            self._wait(timeout=5).until(lambda d: self.wait_present(self.FILTER_PANEL, timeout=2).is_displayed())
            return

        raise AssertionError(
            "Filter panel is not visible and filter toggle was not found. "
            "Update FILTER_TOGGLE locator for your admin theme."
        )

    def _set_checkbox(self, locator, enabled: bool) -> None:
        """Ensures a checkbox matches the expected on/off state."""
        el = self.wait_present(locator)
        self.scroll_into_view(el)
        if el.is_selected() != enabled:
            el.click()

    def _safe_click_element(self, element) -> None:
        """Clicks a WebElement, falling back to JS click if needed."""
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)
