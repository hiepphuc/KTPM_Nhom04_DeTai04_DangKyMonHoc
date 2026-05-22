import time
from selenium.webdriver.common.by import By

from tests.pages.LoginPage import LoginPage
from tests.pages.HomePage import HomePage
from tests.pages.RegisterCoursePage import RegisterCoursePage
from tests.test_base import driver


def test_login_success(driver):
    login_page = LoginPage(driver=driver)
    login_page.open_page()

    login_page.login('2351050135', '123456')

    time.sleep(2)

    assert driver.current_url == 'http://127.0.0.1:5000/'

    welcome_text = driver.find_element(By.CSS_SELECTOR, '.thanh_tren .text-dark').text
    assert 'Phúc' in welcome_text


def test_course_registration_flow(driver):
    login_page = LoginPage(driver=driver)
    login_page.open_page()
    login_page.login('2351050135', '123456')
    time.sleep(1)

    home_page = HomePage(driver=driver)
    home_page.go_to_register_course()
    time.sleep(1)

    reg_course_page = RegisterCoursePage(driver=driver)
    assert 'register-course' in driver.current_url

    reg_course_page.select_semester(index=1)

    if reg_course_page.add_first_course():
        flash_msg = reg_course_page.get_flash_message()
        assert ('Đăng ký thành công' in flash_msg) or \
               ('tín chỉ' in flash_msg) or \
               ('Bạn đã đăng ký lớp này rồi' in flash_msg)

    if reg_course_page.cancel_first_course():
        flash_msg_cancel = reg_course_page.get_flash_message()
        assert ('Huỷ đăng ký thành công' in flash_msg_cancel) or \
               ('Không thể huỷ' in flash_msg_cancel) or \
               ('tối thiểu' in flash_msg_cancel)



def test_view_student_history(driver):
    login_page = LoginPage(driver=driver)
    login_page.open_page()
    login_page.login('2351050135', '123456')
    time.sleep(1)

    driver.get('http://127.0.0.1:5000/student-history')
    time.sleep(1)

    page_text = driver.find_element(By.TAG_NAME, 'body').text
    assert 'Lịch sử học tập' in page_text

    tables = driver.find_elements(By.TAG_NAME, 'table')
    assert len(tables) > 0