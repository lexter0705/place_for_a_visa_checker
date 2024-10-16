import time
import json_checker
from selenium.webdriver.remote.webdriver import WebDriver
from database.setter import UserTable, BlsTable
from seleniumwire import webdriver
from selenium.webdriver import FirefoxOptions


class Parser:
    def __init__(self):
        self.user_table = UserTable()
        self.bls_table = BlsTable()
        self.data = json_checker.get_data_for_web_bot()

    def check_account(self, account: list) -> bool:
        if not account:
            raise ValueError("account is empty")

        account_id = account[0]
        account_blses = self.bls_table.get_all_user_check(account[0])
        for blses in account_blses:
            return True

    def open_browser_with_proxy(self, ip_port: str, login: str, password: str) -> WebDriver:
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
        return webdriver.Firefox(seleniumwire_options=options, options=opts)

    def sleep(self):
        time.sleep(self.data["sleep_between_accounts"])

    @staticmethod
    def extract_data_for_check(check_data: list) -> list:
        data = check_data[len(check_data) - 8:len(check_data) - 3]
        return data
