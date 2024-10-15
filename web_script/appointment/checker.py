from web_script.filler import Filler
from web_script.captcha_checker import CaptchaChecker
from selenium.webdriver.remote.webdriver import WebDriver
import json_checker


class Checker:
    def __init__(self, browser: WebDriver):
        self.__browser = browser
        self.__filler = Filler(self.__browser)
        checker = CaptchaChecker(self.__browser, "#popup_1")
        self.__captcha_checker = checker
        self.__check_appointment_url = \
            json_checker.get_data_for_web_bot()["data_for_add_appointment"]["check_appointment_url"]

    def check_appointment(self, appointment_data: list[str]) -> bool:
        self.__browser.get(self.__check_appointment_url)
        self.__filler.press_button_by_selector("#btnVerify")
        self.__captcha_checker.check_captcha()
        self.__filler.press_button_by_selector("#btnSubmit")
        self.__filler.sleep()
        self.__filler.scroll(400)
        self.fill_input_for_appointment(appointment_data)
        self.__filler.press_button_by_selector("#btnSubmit")
        self.__filler.sleep()
        return self.get_last_answer()

    def fill_input_for_appointment(self, data_for_inputs: list[str]):
        keys = json_checker.get_data_for_web_bot()["data_for_add_appointment"]["inputs_data_for_check"]
        self.__filler.sleep()
        for i in keys.keys():
            self.__filler.fill_protected_drop_down_list(i, 20, data_for_inputs[keys[i]])

    def get_last_answer(self) -> bool:
        return (not self.__filler.is_element_on_display("#commonModalHeader")
                and self.__filler.is_element_on_display("#addressModalHeader"))