from selenium.webdriver.common.by import By
from tests.pages.BasePage import BasePage


class HomePage(BasePage):
    URL = 'http://127.0.0.1:5000/'

    REGISTER_COURSE_BTN = (By.XPATH, "//a[contains(@href, '/register-course')]")
    LOGOUT_BTN = (By.XPATH, "//a[contains(@href, '/logout')]")

    def open_page(self, url=URL):
        self.open(url)

    def go_to_register_course(self):
        self.click(*self.REGISTER_COURSE_BTN)

    def logout(self):
        self.click(*self.LOGOUT_BTN)