import os
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

CURRENT_DAY = datetime.datetime.now().strftime("%d")
CURRENT_MONTH = datetime.datetime.now().strftime("%m")
YEAR_MONTH = datetime.datetime.now().strftime("%Y%m")
ISO_DATE = datetime.datetime.now().strftime("%Y-%m-%d")


class Scraper:
    def __init__(self):
        self.instance = os.getenv("INSTANCE")
        self.district = os.getenv("DISTRICT")
        self.school = os.getenv("SCHOOL")
        # it looks like menu changes between school years?
        self.menu = os.getenv("MENU")

        self.chrome_driver_path = "./chromedriver"
        self.service = Service(self.chrome_driver_path)
        # below makes chrome run in headless mode, sets an emulated resolution
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--window-size=1920x1080")
        # remove chrome_options kwarg below to disable headless mode
        # TODO DeprecationWarning below - "chrome_options" should be "options"
        self.driver = webdriver.Chrome(service=self.service, chrome_options=self.chrome_options)

    def scrape(self):
        self.driver.get(
            f"https://www.myschoolmenus.com/instance/{self.instance}/district/{self.district}/school/{self.school}/menu/{self.menu}")
        self.driver.implicitly_wait(10)
        dates = self.driver.find_elements(By.CLASS_NAME, "calendar-day")
        food = self.driver.find_elements(By.CLASS_NAME, "menu-entrees")
        lunches = [lunch.text for lunch in food]
        days = [date.text for date in dates]
        lunch_menu = {days[i]: lunches[i] for i in range(len(lunches))}
        lunch_menu = {YEAR_MONTH: [lunch_menu]}

        self.driver.quit()
        return lunch_menu
