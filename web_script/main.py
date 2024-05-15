import time
import json_checker
from web_script import appointment
from selenium.webdriver.remote.webdriver import WebDriver
from database.setter import UserTable, BlsTable
from seleniumwire import webdriver
from selenium.webdriver import FirefoxOptions
from web_script.sender import send_message


class Parser:

    def __init__(self):
        self.user_table = UserTable()
        self.bls_table = BlsTable()
        self.data = json_checker.get_data_for_web_bot()

    def run(self):
        while True:
            accounts = self.user_table.select_all_from_database()
            self.check_accounts(accounts)
            self.sleep()

    def check_accounts(self, accounts: list[list]):
        if not accounts:
            return

        for account in accounts:
            self.check_account(account)

    def check_account(self, account: list):
        if not account:
            return
        account_id = account[0]
        account_blses = self.bls_table.get_all_user_check(account[0])
        for blses in account_blses:
            """browser = self.open_browser_with_proxy(*blses[len(blses) - 3:])
            try:
                authorizer = appointment.Authorizer(browser)
                appointment_checker = appointment.AppointmentChecker(browser)
                authorizer.set_login_and_password(blses[2], blses[3])
                authorizer.login()
                authorizer.filler.sleep()
                data = appointment_checker.check_appointment(Parser.extract_data_for_check(blses))
                browser.close()
                send_message(data, account_id)
            except Exception as e:
                print(e)
                browser.close()"""
            send_message(f"Виз по городу {blses[5]} нет! Можете не обращать внимания.", account_id)
            self.sleep()

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


def start():
    parser = Parser()
    parser.run()
