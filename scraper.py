# MAKE SURE ENVIRONMENT VARIABLES ARE LOADED INTO VENV
import os
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import json

INSTANCE = os.getenv("INSTANCE")
DISTRICT = os.getenv("DISTRICT")
SCHOOL = os.getenv("SCHOOL")
# it looks like menu changes between school years?
MENU = os.getenv("MENU")

CHROME_DRIVER_PATH = "/Users/sethscott/Documents/python/chromedriver"
SERVICE = Service(CHROME_DRIVER_PATH)

CURRENT_DAY = datetime.datetime.now().strftime("%d")
CURRENT_MONTH = datetime.datetime.now().strftime("%m")
YEAR_MONTH = datetime.datetime.now().strftime("%Y%m")
ISO_DATE = datetime.datetime.now().strftime("%Y-%m-%d")


class Scraper:
    def __init__(self):
        # below makes chrome run in headless mode, sets an emulated resolution
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--window-size=1920x1080")
        # remove chrome_options kwarg below to disable headless mode
        # TODO DeprecationWarning below - "chrome_options" should be "options"
        self.DRIVER = webdriver.Chrome(service=SERVICE, chrome_options=self.chrome_options)

        self.DRIVER.get(
            f"https://www.myschoolmenus.com/instance/{INSTANCE}/district/{DISTRICT}/school/{SCHOOL}/menu/{MENU}")
        self.DRIVER.implicitly_wait(10)
        self.dates = self.DRIVER.find_elements(By.CLASS_NAME, "calendar-day")
        self.food = self.DRIVER.find_elements(By.CLASS_NAME, "menu-entrees")
        self.lunches = [lunch.text for lunch in self.food]
        self.days = [date.text for date in self.dates]
        self.lunch_menu = {self.days[i]: self.lunches[i] for i in range(len(self.lunches))}
        self.lunch_menu = {YEAR_MONTH: [self.lunch_menu]}

    def scrape(self):
        self.DRIVER.quit()
        return self.lunch_menu


scraper = Scraper()
menu = scraper.scrape()

with open('data.json', mode='w') as menu_api:
    json.dump(menu, menu_api, indent=4)

print(menu)
