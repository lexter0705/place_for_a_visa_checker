from web_script import appointment
from selenium.webdriver.remote.webdriver import WebDriver
from database.setter import UserTable, BlsTable
from seleniumwire import webdriver
from selenium import webdriver as webdriver_without_proxy
from selenium.webdriver import FirefoxOptions
from web_script.sender import send_message


class Parser:

    def __init__(self):
        self.user_table = UserTable()
        self.bls_table = BlsTable()

    def run(self):
        while True:
            accounts_with_prime = self.user_table.get_users_with_high_priority()
            accounts_without_prime = self.user_table.get_users_with_low_priority()
            self.check_accounts(accounts_with_prime)
            self.check_accounts(accounts_without_prime)

    def check_accounts(self, accounts: list[list]):
        for account in accounts:
            self.check_account(account)

    def check_account(self, account: list):
        account_id = account[0]
        account_blses = self.bls_table.get_all_user_check(account[0])
        for blses in account_blses:
            browser = Parser.open_browser_with_proxy(*blses[len(blses) - 3:])
            authorizer = appointment.Authorizer(browser)
            appointment_checker = appointment.AppointmentChecker(browser)
            authorizer.login()
            authorizer.filler.sleep()
            data = appointment_checker.check_appointment(Parser.extract_data_for_check(blses))
            send_message(data, account_id)

    @staticmethod
    def extract_data_for_check(check_data: list) -> list:
        data = check_data[len(check_data) - 8:len(check_data) - 3]
        return data

    @staticmethod
    def open_browser_with_proxy(ip_port: str, login: str, password: str) -> WebDriver:
        if ip_port is "":
            return webdriver_without_proxy.Firefox()

        options = {
            'proxy': {
                'http': f'http://{login}:{password}@{ip_port}',
                'verify_ssl': False,
            },
        }
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        return webdriver.Firefox(seleniumwire_options=options, options=opts)


def start():
    parser = Parser()
    parser.run()
