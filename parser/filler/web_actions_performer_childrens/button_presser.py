from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from parser.filler.web_actions_performer import WebActionsPerformer


class ButtonPresser(WebActionsPerformer):
    def __init__(self, browser: WebDriver):
        super().__init__(browser)

    def press_button_with_offset(self, element: WebElement, cords: list[list[int]]):
        x_offset = (cords[1][0] - cords[0][0]) / 2 + cords[0][0] - element.size["width"] / 2
        y_offset = ((cords[3][1] - cords[0][1]) / 2 + cords[0][1]) - element.size["height"] / 2
        ActionChains(self.__browser) \
            .move_to_element_with_offset(element, x_offset, y_offset) \
            .click() \
            .perform()

    def press_button_by_selector(self, element_selector: str):
        button = self.__browser.find_element(By.CSS_SELECTOR, element_selector)
        ActionChains(self.__browser) \
            .click(button) \
            .perform()
