import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.pages.BasePage import BasePage


class RegisterCoursePage(BasePage):
    URL = 'http://127.0.0.1:5000/register-course'

    SEMESTER_SELECT = (By.NAME, 'semester_id')
    ADD_BTN = (By.CSS_SELECTOR, "form[action='/register-course/add'] button")
    CANCEL_BTN = (By.CSS_SELECTOR, "form[action='/register-course/cancel'] button")
    FLASH_MSG = (By.CSS_SELECTOR, '.alert')

    def open_page(self, url=URL):
        self.open(url)

    def select_semester(self, index=1):
        select = Select(self.find(*self.SEMESTER_SELECT))
        select.select_by_index(index)
        time.sleep(1)

    def add_first_course(self):
        add_buttons = self.finds(*self.ADD_BTN)
        if add_buttons:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_buttons[0])
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", add_buttons[0])
            time.sleep(1)
            return True
        return False

    def cancel_first_course(self):
        cancel_buttons = self.finds(*self.CANCEL_BTN)
        if cancel_buttons:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cancel_buttons[0])
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", cancel_buttons[0])

            wait = WebDriverWait(self.driver, 5)
            alert = wait.until(EC.alert_is_present())
            alert.accept()
            time.sleep(1)
            return True
        return False

    def get_flash_message(self):
        return self.find(*self.FLASH_MSG).text