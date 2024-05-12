from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException
import json_checker
from selenium.webdriver.remote.webdriver import WebDriver
from web_script.filler import Filler
import easyocr
import time
import os


class AiElementChecker:

    def __init__(self, browser: WebDriver, selector: str):
        self.selector = selector
        self.browser = browser
        self.numbers_and_cords = []
        self.image_path = ""
        self.path_to_screenshots = json_checker.get_data_for_web_bot()["path_to_screenshots"]
        self.element = None
        self.filler = Filler(self.browser)

    def screenshot(self):
        screen_shot_name = f"screen_shot_{time.time()}.png"
        screenshot_path = f"{self.path_to_screenshots}" + screen_shot_name
        self.element.screenshot(screenshot_path)
        self.image_path = screenshot_path

    def set_numbers_from_image(self):
        lang = "en"
        data = easyocr.Reader([lang]).readtext(self.image_path, detail=1, paragraph=False, text_threshold=0.8)
        self.numbers_and_cords = data

    def get_offset(self, cords: list[list[int]]):
        x_offset = (cords[1][0] - cords[0][0]) / 2 + cords[0][0] - self.element.size["width"] / 2
        y_offset = ((cords[3][1] - cords[0][1]) / 2 + cords[0][1]) - self.element.size["height"] / 2
        return x_offset, y_offset

    def press_button_with_offset(self, cords: list[list[int]]):
        ActionChains(self.browser) \
            .move_to_element_with_offset(self.element, *self.get_offset(cords)) \
            .click() \
            .perform()

    def set_element(self):
        self.element = self.browser.find_element(By.CSS_SELECTOR, self.selector)

    def reset(self):
        if os.path.exists(self.image_path):
            os.remove(self.image_path)
        self.element = None
        self.numbers_and_cords = []
        self.image_path = ""


class CaptchaChecker(AiElementChecker):
    def __init__(self, browser: WebDriver, captcha_selector: str):
        super().__init__(browser, captcha_selector)
        self.true_numbers = []

    def check_captcha(self):
        self.filler.sleep()
        self.filler.sleep()
        self.set_element()
        self.pass_the_captcha()
        self.reset_captcha()
        self.filler.sleep()

    def pass_the_captcha(self):
        self.screenshot()
        self.set_numbers_from_image()
        self.check_captcha_is_worked()
        self.set_true_numbers_id()
        self.press_buttons_on_captcha()
        self.press_submit_button()
        self.accept_alert()
        if self.captcha_is_here():
            self.reset_captcha()
            self.check_captcha()

    def press_submit_button(self):
        if self.numbers_and_cords[len(self.numbers_and_cords) - 1][1] == "Submit Selection":
            self.press_button_with_offset(self.numbers_and_cords[len(self.numbers_and_cords) - 1][0])
        else:
            self.press_button_with_offset(self.numbers_and_cords[len(self.numbers_and_cords) - 2][0])

    def check_captcha_is_worked(self):
        if len(self.numbers_and_cords) < 5:
            raise Exception("Captcha is blocked")

    def captcha_is_here(self) -> bool:
        try:
            self.browser.find_element(By.CSS_SELECTOR, self.selector)
            return True
        except NoSuchElementException:
            print("Captcha passed")
            return False

    def accept_alert(self):
        self.filler.sleep()
        try:
            Alert(self.browser).accept()
        except NoAlertPresentException:
            pass

    def press_buttons_on_captcha(self):
        for i in self.true_numbers:
            self.press_button_with_offset(self.numbers_and_cords[i][0])
            time.sleep(0.5)

    def set_true_numbers_id(self):
        true_numbers = self.numbers_and_cords[0][1].split(" ")
        true_numbers = true_numbers[len(true_numbers) - 1]
        for i in range(1, len(self.numbers_and_cords) - 3):
            if self.numbers_and_cords[i][1] == true_numbers:
                self.true_numbers.append(i)

    def reset_captcha(self):
        self.reset()
        self.true_numbers = []
