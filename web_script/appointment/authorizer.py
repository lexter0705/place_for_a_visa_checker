from web_script.filler import Filler
from web_script.captcha_checker import CaptchaChecker
from selenium.webdriver.remote.webdriver import WebDriver
import json_checker


class Authorizer:
    def __init__(self, browser: WebDriver, email: str, password: str):
        self.__browser = browser
        self.__data = json_checker.get_data_for_web_bot()
        self.__captcha_checker = CaptchaChecker(self.__browser, "#popup_1")
        self.__filler = Filler(self.__browser)
        self.__email = ""
        self.__password = ""
        self.set_login_and_password(email, password)

    def login(self):
        login_url = self.__data["data_for_login"]["url"]
        self.__browser.get(login_url)
        self.__filler.sleep()
        self.__filler.fill_protected_inputs(self.__email, "#UserId", 10)
        self.__filler.fill_protected_inputs(self.__password, "#Password", 10)
        self.__filler.press_button_by_selector("#btnVerify")
        self.__captcha_checker.check_captcha()
        self.__filler.press_button_by_selector("#btnSubmit")

    def set_login_and_password(self, email: str, password: str):
        if len(email.split("@")) <= 0 or len(email.split(".")) <= 0:
            raise ValueError("Incorrect email")

        self.__email = email
        self.__password = password