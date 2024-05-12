from selenium.webdriver import ActionChains, Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
import json_checker
import time


class Filler:
    def __init__(self, browser: WebDriver):
        self.browser = browser
        self.sleep_time = json_checker.get_data_for_web_bot()["sleep_time"]

    def fill_input(self, element: WebElement, text: str):
        ActionChains(self.browser) \
            .click(element) \
            .send_keys(text) \
            .perform()

    def press_button_by_selector(self, element_selector: str):
        button = self.browser.find_element(By.CSS_SELECTOR, element_selector)
        ActionChains(self.browser) \
            .click(button) \
            .perform()

    def fill_drop_down_list(self, element: WebElement, text: str):
        self.sleep()
        ActionChains(self.browser).click(element).perform()
        self.sleep()
        ActionChains(self.browser).send_keys(text).perform()
        self.sleep()
        self.press_keyboard_button(Keys.ARROW_DOWN)
        self.press_keyboard_button(Keys.ENTER)

    def fill_protected_inputs(self, text_for_input: str, selector: str, count: int):
        for i in range(1, count + 1):
            element_selector = selector + str(i)
            if self.is_element_on_display(element_selector):
                input_element = self.browser.find_element(By.CSS_SELECTOR, f"{selector}{i}")
                if input_element.is_displayed():
                    self.fill_input(input_element, text_for_input)
                    break

    def fill_protected_drop_down_list(self, selector_without_number: str, count: int, text: str):
        for i in range(1, count + 1):
            element_selector = selector_without_number + str(i)
            if self.is_element_on_display(element_selector):
                element = self.browser.find_element(By.CSS_SELECTOR, element_selector)
                element = element.find_element(By.XPATH, "..")
                if element.is_displayed():
                    self.fill_drop_down_list(element, text)
                    break

    def scroll(self, scroll_delta: int):
        ActionChains(self.browser) \
            .scroll_by_amount(0, scroll_delta) \
            .perform()

    def press_keyboard_button(self, button_keys: str):
        ActionChains(self.browser) \
            .send_keys(button_keys) \
            .perform()

    def sleep(self):
        time.sleep(self.sleep_time)

    def is_element_on_display(self, element_selector: str) -> bool:
        try:
            self.browser.find_element(By.CSS_SELECTOR, element_selector)
            return True
        except NoSuchElementException:
            return False
