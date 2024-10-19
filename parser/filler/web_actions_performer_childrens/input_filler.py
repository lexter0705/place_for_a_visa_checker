from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from parser.filler.web_actions_performer import WebActionsPerformer


class InputFiller(WebActionsPerformer):
    def __init__(self, browser: WebDriver):
        super().__init__(browser)

    def fill_input(self, element: WebElement, text: str):
        ActionChains(self.__browser) \
            .click(element) \
            .send_keys(text) \
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
