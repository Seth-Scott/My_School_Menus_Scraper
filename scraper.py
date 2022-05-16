# MAKE SURE ENVIRONMENT VARIABLES ARE LOADED INTO VENV
import os
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json

INSTANCE = os.getenv("INSTANCE")
DISTRICT = os.getenv("DISTRICT")
SCHOOL = os.getenv("SCHOOL")
MENU = os.getenv("MENU")

CHROME_DRIVER_PATH = "/Users/sethscott/Documents/python/chromedriver"
SERVICE = Service(CHROME_DRIVER_PATH)

CURRENT_DAY = datetime.datetime.now().strftime("%d")
CURRENT_MONTH = datetime.datetime.now().strftime("%m")
YEAR_MONTH = datetime.datetime.now().strftime("%Y%m")
ISO_DATE = datetime.datetime.now().strftime("%Y-%m-%d")


class Scraper:
    def __init__(self):
        self.DRIVER = webdriver.Chrome(service=SERVICE)
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
