import time
from selenium.common import NoSuchElementException, NoAlertPresentException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import json_checker


class WebActionsPerformer:
    def __init__(self, browser: WebDriver):
        self.__browser = browser
        self.__sleep_time = json_checker.get_data_for_parser()["sleep_time"]

    def get_browser(self) -> WebDriver:
        return self.__browser

    def scroll(self, scroll_delta: int):
        ActionChains(self.__browser) \
            .scroll_by_amount(0, scroll_delta) \
            .perform()

    def sleep(self):
        time.sleep(self.__sleep_time)

    def is_element_on_display(self, element_selector: str) -> bool:
        try:
            self.__browser.find_element(By.CSS_SELECTOR, element_selector)
            return True
        except NoSuchElementException:
            return False

    def accept_alert(self):
        try:
            Alert(self.__browser).accept()
        except NoAlertPresentException:
            pass

    def press_keyboard_button(self, button_keys: str):
        ActionChains(self.__browser) \
            .send_keys(button_keys) \
            .perform()
