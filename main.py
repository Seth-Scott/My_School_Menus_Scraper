import os
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from flask import Flask, jsonify

# TODO separate flask and API into different classes in different files
# TODO run selenium headless
# TODO build docker with dependencies (unraid)
# TODO run api program on cronjob


app = Flask(__name__)


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


try:
    today = menu[str(CURRENT_DAY)]
except KeyError:
    print("No lunch today")
DRIVER.quit()


@app.route('/')
def api():
    return jsonify(menu)


if __name__ == '__main__':
    app.run(port=5001, host="0.0.0.0")
