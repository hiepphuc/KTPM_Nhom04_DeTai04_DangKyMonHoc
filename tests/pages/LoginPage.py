from selenium.webdriver.common.by import By
from tests.pages.BasePage import BasePage


class LoginPage(BasePage):
    URL = 'http://127.0.0.1:5000/login'

    STUDENT_ID_INPUT = (By.NAME, 'student_id')
    PASSWORD_INPUT = (By.NAME, 'password')
    LOGIN_BTN = (By.CSS_SELECTOR, 'button[type="submit"]')

    def open_page(self, url=URL):
        self.open(url)

    def login(self, student_id, password):
        self.typing(*self.STUDENT_ID_INPUT, student_id)
        self.typing(*self.PASSWORD_INPUT, password)
        self.click(*self.LOGIN_BTN)