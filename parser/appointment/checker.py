from parser.ai_checker.captcha_checker import CaptchaChecker
from selenium.webdriver.remote.webdriver import WebDriver
import json_checker
from parser.data_types.check_data import CheckData
from parser.filler.filler import Filler


class Checker:
    def __init__(self, browser: WebDriver, check_data: CheckData):
        self.__browser = browser
        self.__check_data = check_data
        self.__filler = Filler(self.__browser)
        checker = CaptchaChecker(self.__browser, "#popup_1")
        self.__captcha_checker = checker
        self.__check_appointment_url = \
            json_checker.get_data_for_parser()["data_for_add_appointment"]["check_appointment_url"]

    def check_appointment(self) -> bool:
        self.__browser.get(self.__check_appointment_url)
        self.__filler.press_button_by_selector("#btnVerify")
        self.__captcha_checker.check_captcha()
        self.__filler.press_button_by_selector("#btnSubmit")
        self.__filler.sleep()
        self.__filler.scroll(400)
        self.__fill_input_for_appointment()
        self.__filler.press_button_by_selector("#btnSubmit")
        self.__filler.sleep()
        return self.__get_last_answer()

    def __fill_input_for_appointment(self):
        keys = json_checker.get_data_for_parser()["data_for_add_appointment"]["inputs_data_for_check"]
        self.__filler.sleep()
        for i in keys.keys():
            self.__filler.fill_protected_drop_down_list(i, 20, self.__check_data.get_data_list()[keys[i]])

    def __get_last_answer(self) -> bool:
        return (not self.__filler.is_element_on_display("#commonModalHeader")
                and self.__filler.is_element_on_display("#addressModalHeader"))
