import os
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

INSTANCE = os.getenv("INSTANCE")
DISTRICT = os.getenv("DISTRICT")
SCHOOL = os.getenv("SCHOOL")
MENU = os.getenv("MENU")

chrome_driver_path = "/Users/sethscott/Documents/python/chromedriver"
s = Service(chrome_driver_path)
driver = webdriver.Chrome(service=s)


driver.get(f"https://www.myschoolmenus.com/instance/{INSTANCE}/district/{DISTRICT}/school/{SCHOOL}/menu/{MENU}")
driver.implicitly_wait(10)
dates = driver.find_elements(By.CLASS_NAME, "calendar-day")
food = driver.find_elements(By.CLASS_NAME, "menu-entrees")


lunches = [lunch.text for lunch in food]
days = [date.text for date in dates]
lunch_menu = {days[i]: lunches[i] for i in range(len(lunches))}

current_day = datetime.datetime.now().strftime("%d")
print(current_day)
try:
    print(lunch_menu[current_day])
except KeyError:
    print("No lunch today 🤠")

driver.quit()
