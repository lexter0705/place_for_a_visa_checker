from selenium.webdriver import ActionChains, Keys
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
import json_checker
import time


class Filler:
    def __init__(self, browser: WebDriver):
        self.__browser = browser
        self.__sleep_time = json_checker.get_data_for_web_bot()["sleep_time"]

    def get_offset(self, element: WebElement, cords: list[list[int]]):
        x_offset = (cords[1][0] - cords[0][0]) / 2 + cords[0][0] - element.size["width"] / 2
        y_offset = ((cords[3][1] - cords[0][1]) / 2 + cords[0][1]) - element.size["height"] / 2
        return x_offset, y_offset

    def press_button_with_offset(self, element: WebElement, cords: list[list[int]]):
        ActionChains(self.__browser) \
            .move_to_element_with_offset(element, *self.get_offset(element, cords)) \
            .click() \
            .perform()

    def fill_input(self, element: WebElement, text: str):
        ActionChains(self.__browser) \
            .click(element) \
            .send_keys(text) \
            .perform()

    def press_button_by_selector(self, element_selector: str):
        button = self.__browser.find_element(By.CSS_SELECTOR, element_selector)
        ActionChains(self.__browser) \
            .click(button) \
            .perform()

    def fill_drop_down_list(self, element: WebElement, text: str):
        self.sleep()
        ActionChains(self.__browser).click(element).perform()
        self.sleep()
        ActionChains(self.__browser).send_keys(text).perform()
        self.sleep()
        self.press_keyboard_button(Keys.ARROW_DOWN)
        self.press_keyboard_button(Keys.ENTER)

    def fill_protected_inputs(self, text_for_input: str, selector: str, count: int):
        for i in range(1, count + 1):
            element_selector = selector + str(i)
            if self.is_element_on_display(element_selector):
                input_element = self.__browser.find_element(By.CSS_SELECTOR, f"{selector}{i}")
                if input_element.is_displayed():
                    self.fill_input(input_element, text_for_input)
                    break

    def fill_protected_drop_down_list(self, selector_without_number: str, count: int, text: str):
        for i in range(1, count + 1):
            element_selector = selector_without_number + str(i)
            if self.is_element_on_display(element_selector):
                element = self.__browser.find_element(By.CSS_SELECTOR, element_selector)
                element = element.find_element(By.XPATH, "..")
                if element.is_displayed():
                    self.fill_drop_down_list(element, text)
                    break

    def scroll(self, scroll_delta: int):
        ActionChains(self.__browser) \
            .scroll_by_amount(0, scroll_delta) \
            .perform()

    def press_keyboard_button(self, button_keys: str):
        ActionChains(self.__browser) \
            .send_keys(button_keys) \
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
