from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import json_checker
from selenium.webdriver.remote.webdriver import WebDriver
from parser.filler import Filler
import easyocr
import time
import os


class AiElementChecker:
    def __init__(self, browser: WebDriver, selector: str):
        self.__selector = selector
        self.__browser = browser
        self.__numbers_and_cords = []
        self.__image_path = ""
        self.__path_to_screenshots = json_checker.get_data_for_web_bot()["path_to_screenshots"]
        self.__filler = Filler(self.__browser)
        self.__element = None

    def screenshot(self):
        screen_shot_name = f"screen_shot_{time.time()}.png"
        screenshot_path = f"{self.__path_to_screenshots}" + screen_shot_name
        self.__element.screenshot(screenshot_path)
        self.__image_path = screenshot_path

    def check(self, lang: str):
        data = easyocr.Reader([lang]).readtext(self.__image_path, detail=1, paragraph=False, text_threshold=0.8)
        self.__numbers_and_cords = data

    def set_element(self):
        self.__element = self.__browser.find_element(By.CSS_SELECTOR, self.__selector)

    def reset(self):
        if os.path.exists(self.__image_path):
            os.remove(self.__image_path)

        self.__element = None
        self.__numbers_and_cords = []
        self.__image_path = ""

    def get_filler(self) -> Filler:
        return self.__filler

    def get_element(self) -> WebElement:
        return self.__element

    def get_selector(self) -> str:
        return self.__selector