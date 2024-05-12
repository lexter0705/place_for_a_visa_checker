from web_script.filler import Filler
from web_script.captcha_checker import CaptchaChecker
from selenium.webdriver.remote.webdriver import WebDriver
import json_checker


class Authorizer:
    def __init__(self, browser):
        self.browser = browser
        self.data = json_checker.get_data_for_web_bot()
        self.captcha_checker = CaptchaChecker(self.browser, "#popup_1")
        self.filler = Filler(self.browser)
        self.email = ""
        self.password = ""

    def login(self):
        login_url = self.data["data_for_login"]["url"]
        self.browser.get(login_url)
        self.filler.sleep()
        self.filler.fill_protected_inputs(self.email, "#UserId", 10)
        self.filler.fill_protected_inputs(self.password, "#Password", 10)
        self.filler.press_button_by_selector("#btnVerify")
        self.captcha_checker.check_captcha()
        self.filler.press_button_by_selector("#btnSubmit")

    def set_login_and_password(self, email: str, password: str):
        if len(email.split("@")) < 2 and len(email.split(".")) < 2:
            return
        self.email = email
        self.password = password


class AppointmentChecker:
    def __init__(self, browser: WebDriver):
        self.browser = browser
        self.filler = Filler(self.browser)
        self.captcha_checker = CaptchaChecker(self.browser, "#popup_1")
        self.check_appointment_url = json_checker.get_data_for_web_bot()["data_for_add_appointment"][
            "check_appointment_url"]

    def check_appointment(self, appointment_data: list[str]) -> str:
        self.browser.get(self.check_appointment_url)
        self.filler.press_button_by_selector("#btnVerify")
        self.captcha_checker.check_captcha()
        self.filler.press_button_by_selector("#btnSubmit")
        self.filler.sleep()
        self.filler.scroll(400)
        self.fill_input_for_appointment(appointment_data)
        self.filler.press_button_by_selector("#btnSubmit")
        self.filler.sleep()
        keys = json_checker.get_data_for_web_bot()["data_for_add_appointment"]["inputs_data_for_check"]
        return self.get_last_answer(appointment_data[keys["#Location"]])

    def fill_input_for_appointment(self, data_for_inputs: list[str]):
        keys = json_checker.get_data_for_web_bot()["data_for_add_appointment"]["inputs_data_for_check"]
        self.filler.sleep()
        for i in keys.keys():
            self.filler.fill_protected_drop_down_list(i, 20, data_for_inputs[keys[i]])

    def get_last_answer(self, city: str) -> str:
        if self.filler.is_element_on_display("#commonModalHeader"):
            last_element_text = f"Виз по городу {city} нет! Можете не обращать внимания."
        elif self.filler.is_element_on_display("#addressModalHeader"):
            last_element_text = f"Визы по городу {city} есть! Бегите регистрироваться."
        else:
            last_element_text = f"Виз по городу {city} нет! Можете не обращать внимания."

        return last_element_text
