from selenium.webdriver.remote.webdriver import WebDriver
from parser.filler.web_actions_performer_childrens.button_presser import ButtonPresser
from parser.filler.web_actions_performer_childrens.input_filler import InputFiller


class Filler(ButtonPresser, InputFiller):
    def __init__(self, browser: WebDriver):
        ButtonPresser.__init__(self, browser)
        InputFiller.__init__(self, browser)
