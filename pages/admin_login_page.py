from selenium.webdriver.common.by import By
from utils.base_page import BaseAdminPage


class AdminLoginPage(BaseAdminPage):
    """
    Page Object Model for the Admin Login Page.
    Handles admin authentication actions only.
    """

    # --- Locators ---
    USERNAME_FIELD = (By.ID, "input-username")
    PASSWORD_FIELD = (By.ID, "input-password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    # --- Navigation ---
    def open(self, url):
        """Open admin login page."""

        self.driver.get(url)

    # --- Actions ---
    def login_as(self, username, password):
        """Login using provided credentials."""

        self.type(self.USERNAME_FIELD, username)
        self.type(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BUTTON)
