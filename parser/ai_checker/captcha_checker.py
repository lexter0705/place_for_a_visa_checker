from selenium.webdriver.remote.webdriver import WebDriver
from parser.ai_checker.ai_element_checker import AiElementChecker
import time

from parser.filler.web_actions_performer_childrens.button_presser import ButtonPresser


class CaptchaChecker(AiElementChecker):
    def __init__(self, browser: WebDriver, captcha_selector: str):
        super().__init__(browser, captcha_selector)
        self.__true_numbers = []
        self.__button_presser = ButtonPresser(self.__browser)

    def check_captcha(self):
        self.__button_presser.sleep()
        self.__button_presser.sleep()
        self.set_element()
        self.__pass_the_captcha()
        self.__reset_captcha()
        self.__button_presser.sleep()

    def __pass_the_captcha(self):
        self.screenshot()
        self.check("en")
        self.__check_captcha_is_worked()
        self.__set_true_numbers_id()
        self.__press_buttons_on_captcha()
        self.__press_submit_button()
        self.__button_presser.sleep()
        self.__button_presser.accept_alert()
        if self.__button_presser.is_element_on_display(self.get_selector()):
            self.__reset_captcha()
            self.check_captcha()

    def __press_submit_button(self):
        if self.__numbers_and_cords[len(self.__numbers_and_cords) - 1][1] == "Submit Selection":
            self.__button_presser.press_button_with_offset \
                (self.get_element(), self.__numbers_and_cords[len(self.__numbers_and_cords) - 1][0])
        else:
            self.__button_presser.press_button_with_offset \
                (self.get_element(), self.__numbers_and_cords[len(self.__numbers_and_cords) - 2][0])

    def __check_captcha_is_worked(self):
        if len(self.__numbers_and_cords) < 5:
            raise Exception("Captcha is blocked")

    def __press_buttons_on_captcha(self):
        for i in self.__true_numbers:
            self.__button_presser.press_button_with_offset(self.__numbers_and_cords[i][0])
            time.sleep(0.5)

    def __set_true_numbers_id(self):
        true_numbers = self.__numbers_and_cords[0][1].split(" ")
        true_numbers = true_numbers[len(true_numbers) - 1]
        for i in range(1, len(self.__numbers_and_cords) - 3):
            if self.__numbers_and_cords[i][1] == true_numbers:
                self.__true_numbers.append(i)

    def __reset_captcha(self):
        self.reset()
        self.__true_numbers = []
