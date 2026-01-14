from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BaseAdminPage:
    """
    Base Page Object for OpenCart Admin Panel pages.
    """

    # --- Admin Common Locators ---
    ALERT_CLOSE_BUTTON = (
        By.XPATH, "//button[@type='button' and contains(@class,'btn-close')]"
    )
    SUCCESS_ALERT = (By.CSS_SELECTOR, "div.alert-success")
    ERROR_ALERT = (By.CSS_SELECTOR, "div.alert-danger")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    # -------------------------
    # Wait helpers
    # -------------------------
    def _wait(self, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout)

    def wait_visible(self, locator, timeout=None):
        try:
            return self._wait(timeout).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            raise AssertionError(f"Timed out waiting for VISIBLE element: {locator}")

    def wait_present(self, locator, timeout=None):
        try:
            return self._wait(timeout).until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise AssertionError(f"Timed out waiting for PRESENT element: {locator}")

    def wait_clickable(self, locator, timeout=None):
        try:
            return self._wait(timeout).until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            raise AssertionError(f"Timed out waiting for CLICKABLE element: {locator}")

    def wait_invisible(self, locator, timeout=None):
        try:
            return self._wait(timeout).until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            raise AssertionError(f"Timed out waiting for INVISIBLE element: {locator}")

    # -------------------------
    # Element getters
    # -------------------------
    def get(self, locator, timeout=None):
        return self.wait_visible(locator, timeout)

    def get_all(self, locator, timeout=None):
        try:
            return self._wait(timeout).until(EC.visibility_of_all_elements_located(locator))
        except TimeoutException:
            raise AssertionError(f"Timed out waiting for VISIBLE elements: {locator}")

    # -------------------------
    # Simple UI actions
    # -------------------------
    def scroll_into_view(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            element
        )

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0);")

    def click(self, locator, timeout=None, scroll=True):
        element = self.wait_visible(locator, timeout)
        if scroll:
            self.scroll_into_view(element)
        element = self.wait_clickable(locator, timeout)
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    def js_click(self, locator, timeout=None, scroll=True):
        element = self.wait_present(locator, timeout)
        if scroll:
            self.scroll_into_view(element)
        self.driver.execute_script("arguments[0].click();", element)

    def type(self, locator, text, timeout=None, clear=True):
        element = self.wait_visible(locator, timeout)
        if clear:
            element.clear()
        element.send_keys(text)

    def text_of(self, locator, timeout=None):
        return self.wait_visible(locator, timeout).text.strip()

    # -------------------------
    # State checks
    # -------------------------
    def is_present(self, locator, timeout=0):
        try:
            self._wait(timeout).until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_visible(self, locator, timeout=0):
        try:
            self._wait(timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_clickable(self, locator, timeout=0):
        try:
            self._wait(timeout).until(EC.element_to_be_clickable(locator))
            return True
        except TimeoutException:
            return False

    # -------------------------
    # Message handling
    # -------------------------
    def wait_success_message(self, timeout=10):
        return self.wait_visible(self.SUCCESS_ALERT, timeout)

    def wait_error_message(self, timeout=None):
        return self.text_of(self.ERROR_ALERT, timeout=timeout)

    def get_success_message_if_any(self, timeout=1):
        return self.text_of(self.SUCCESS_ALERT, timeout=timeout) if self.is_visible(self.SUCCESS_ALERT, timeout) else ""

    def get_error_message_if_any(self, timeout=1):
        return self.text_of(self.ERROR_ALERT, timeout=timeout) if self.is_visible(self.ERROR_ALERT, timeout) else ""

    def close_alert_if_present(self, timeout=3):
        self.wait_clickable(self.ALERT_CLOSE_BUTTON, timeout).click()