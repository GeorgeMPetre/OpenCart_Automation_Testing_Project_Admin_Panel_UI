from selenium.webdriver.common.by import By
from utils.base_page import BaseAdminPage


class AdminLoginPage(BaseAdminPage):
    """Handles admin login: open the page, enter credentials, and submit."""

    # ---------------------------
    # Locators
    # ---------------------------
    USERNAME = (By.ID, "input-username")
    PASSWORD = (By.ID, "input-password")
    SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")

    # ---------------------------
    # Navigation
    # ---------------------------
    def open(self, url: str) -> None:
        """Opens the admin login page."""
        self.driver.get(url)

    # ---------------------------
    # Actions
    # ---------------------------
    def login_as(self, username: str, password: str) -> None:
        """Logs in using the provided admin username and password."""
        self._enter_credentials(username, password)
        self.click(self.SUBMIT)

    # ---------------------------
    # Internal helpers
    # ---------------------------
    def _enter_credentials(self, username: str, password: str) -> None:
        """Types the username and password into the login form."""
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
