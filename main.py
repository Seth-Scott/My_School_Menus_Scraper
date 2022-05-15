import os
import datetime
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

INSTANCE = os.getenv("INSTANCE")
DISTRICT = os.getenv("DISTRICT")
SCHOOL = os.getenv("SCHOOL")
MENU = os.getenv("MENU")


CHROME_DRIVER_PATH = "/Users/sethscott/Documents/python/chromedriver"
SERVICE = Service(CHROME_DRIVER_PATH)
DRIVER = webdriver.Chrome(service=SERVICE)

CURRENT_DAY = datetime.datetime.now().strftime("%d")
ISO_DATE = datetime.datetime.now().strftime("%Y-%m-%d")

def scrape():
    DRIVER.get(f"https://www.myschoolmenus.com/instance/{INSTANCE}/district/{DISTRICT}/school/{SCHOOL}/menu/{MENU}")
    DRIVER.implicitly_wait(10)

    dates = DRIVER.find_elements(By.CLASS_NAME, "calendar-day")
    food = DRIVER.find_elements(By.CLASS_NAME, "menu-entrees")

    lunches = [lunch.text for lunch in food]
    days = [date.text for date in dates]
    lunch_menu = {days[i]: lunches[i] for i in range(len(lunches))}

    return lunch_menu


menu = scrape()
print(menu)

try:
    print(menu[str(CURRENT_DAY)])
except KeyError:
    print("No lunch today")
DRIVER.quit()

