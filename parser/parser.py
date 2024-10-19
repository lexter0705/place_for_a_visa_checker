from selenium.webdriver.remote.webdriver import WebDriver
from database.setter import UserTable, BlsTable
from seleniumwire import webdriver
from selenium.webdriver import FirefoxOptions
from appointment.authorizer import Authorizer
from appointment.checker import Checker
from data_types.check_data import CheckData
from data_types.login_data import LoginData
import time
import json_checker


class Parser:
    def __init__(self, browser: WebDriver):
        self.user_table = UserTable()
        self.bls_table = BlsTable()
        self.data = json_checker.get_data_for_parser()
        self.browser = browser

    def check_account(self, login_data: LoginData, check_data: CheckData) -> bool:
        authorizer = Authorizer(self.browser, login_data.get_login(), login_data.get_password())
        authorizer.login()
        checker = Checker(self.browser, check_data)
        return checker.check_appointment()

    def open_browser_with_proxy(self, ip_port: str, login: str, password: str):
        if not ip_port:
            ip_port = self.data["base_proxy_ip_port"]
            login = self.data["base_proxy_login"]
            password = self.data["base_proxy_password"]

        options = {
            'proxy': {
                'http': f'http://{login}:{password}@{ip_port}',
                'verify_ssl': False,
            },
        }
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        self.browser = webdriver.Firefox(seleniumwire_options=options, options=opts)

    def open_browser(self):
        opts = FirefoxOptions()
        self.browser = webdriver.Firefox(options=opts)

    def sleep(self):
        time.sleep(self.data["sleep_between_accounts"])
