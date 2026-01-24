from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class BaseAdminPage:
    """Common Selenium helpers for OpenCart admin pages (waits, actions, and alert helpers)."""

    # Admin common locators
    ALERT_CLOSE_BUTTON = (By.XPATH, "//button[@type='button' and contains(@class,'btn-close')]")
    SUCCESS_ALERT = (By.CSS_SELECTOR, "div.alert-success")
    ERROR_ALERT = (By.CSS_SELECTOR, "div.alert-danger")

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout

    # -------------------------
    # Wait helpers
    # -------------------------
    def _wait(self, timeout: int | None = None) -> WebDriverWait:
        """Creates a WebDriverWait using the default timeout (or a custom one)."""
        return WebDriverWait(self.driver, timeout or self.timeout)

    def wait_visible(self, locator, timeout: int | None = None):
        """Waits until the element is visible and returns it."""
        try:
            return self._wait(timeout).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            raise AssertionError(f"Timed out waiting for visible element: {locator}")

    def wait_present(self, locator, timeout: int | None = None):
        """Waits until the element exists in the DOM and returns it."""
        try:
            return self._wait(timeout).until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise AssertionError(f"Timed out waiting for present element: {locator}")

    def wait_clickable(self, locator, timeout: int | None = None):
        """Waits until the element is clickable and returns it."""
        try:
            return self._wait(timeout).until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            raise AssertionError(f"Timed out waiting for clickable element: {locator}")

    def wait_invisible(self, locator, timeout=None):
        """Wait until the element becomes invisible or is removed from the DOM."""
        try:
            return self._wait(timeout).until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            raise AssertionError(f"Timed out waiting for INVISIBLE element: {locator}")

    # -------------------------
    # Element getters
    # -------------------------
    def get(self, locator, timeout: int | None = None):
        """Returns a visible element (simple alias)."""
        return self.wait_visible(locator, timeout)

    def get_all(self, locator, timeout: int | None = None):
        """Returns all visible elements that match the locator."""
        try:
            return self._wait(timeout).until(EC.visibility_of_all_elements_located(locator))
        except TimeoutException:
            raise AssertionError(f"Timed out waiting for visible elements: {locator}")

    # -------------------------
    # Simple UI actions
    # -------------------------
    def scroll_into_view(self, element) -> None:
        """Scrolls the page so the given element is in view."""
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            element,
        )

    def scroll_to_top(self) -> None:
        """Scrolls to the top of the page."""
        self.driver.execute_script("window.scrollTo(0, 0);")

    def click(self, locator, timeout: int | None = None, scroll: bool = True) -> None:
        """Clicks an element, with optional scroll and JS fallback."""
        element = self.wait_visible(locator, timeout)
        if scroll:
            self.scroll_into_view(element)

        element = self.wait_clickable(locator, timeout)
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    def js_click(self, locator, timeout: int | None = None, scroll: bool = True) -> None:
        """Clicks an element via JavaScript (useful for tricky admin UI)."""
        element = self.wait_present(locator, timeout)
        if scroll:
            self.scroll_into_view(element)
        self.driver.execute_script("arguments[0].click();", element)

    def type(self, locator, text: str, timeout: int | None = None, clear: bool = True) -> None:
        """Types into a field (optionally clears first)."""
        element = self.wait_visible(locator, timeout)
        if clear:
            element.clear()
        element.send_keys(text)

    def text_of(self, locator, timeout: int | None = None) -> str:
        """Returns element text."""
        return self.wait_visible(locator, timeout).text.strip()

    # -------------------------
    # State checks
    # -------------------------
    def is_present(self, locator, timeout: int = 0) -> bool:
        """True if the element appears in the DOM within the timeout."""
        try:
            self._wait(timeout).until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_visible(self, locator, timeout: int = 0) -> bool:
        """True if the element becomes visible within the timeout."""
        try:
            self._wait(timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_clickable(self, locator, timeout: int = 0) -> bool:
        """True if the element becomes clickable within the timeout."""
        try:
            self._wait(timeout).until(EC.element_to_be_clickable(locator))
            return True
        except TimeoutException:
            return False

    # -------------------------
    # Message handling
    # -------------------------
    def wait_success_message(self, timeout: int = 10):
        """Waits for the success alert and returns it."""
        return self.wait_visible(self.SUCCESS_ALERT, timeout)

    def wait_error_message(self, timeout: int | None = None) -> str:
        """Waits for the error alert and returns its text."""
        return self.text_of(self.ERROR_ALERT, timeout=timeout)

    def get_success_message_if_any(self, timeout: int = 1) -> str:
        """Returns success text if visible, otherwise an empty string."""
        return self.text_of(self.SUCCESS_ALERT, timeout=timeout) if self.is_visible(self.SUCCESS_ALERT, timeout) else ""

    def get_error_message_if_any(self, timeout: int = 1) -> str:
        """Returns error text if visible, otherwise an empty string."""
        return self.text_of(self.ERROR_ALERT, timeout=timeout) if self.is_visible(self.ERROR_ALERT, timeout) else ""

    def close_alert_if_present(self, timeout: int = 3) -> bool:
        """Closes the top alert banner if the close button is available."""
        if not self.is_clickable(self.ALERT_CLOSE_BUTTON, timeout=timeout):
            return False
        self.wait_clickable(self.ALERT_CLOSE_BUTTON, timeout=timeout).click()
        return True
