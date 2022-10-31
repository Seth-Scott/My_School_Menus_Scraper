import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from get_dates import GetDates

get_date = GetDates()


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

        self.current_day = get_date.day
        self.current_month = get_date.month
        self.current_year = get_date.year
        self.iso_date = get_date.iso_date

    def scrape(self):
        self.driver.get(
            f"https://www.myschoolmenus.com/instance/{self.instance}/district/{self.district}/school/{self.school}/menu/{self.menu}")
        self.driver.implicitly_wait(10)
        dates = self.driver.find_elements(By.CLASS_NAME, "calendar-day")
        food = self.driver.find_elements(By.CLASS_NAME, "menu-entrees")
        lunches = [lunch.text.replace("Goldkist ", "").replace("Entree\n", "").replace("Vegetables\n", "").replace("Fruit and Vegetable Variety\n", "").replace("Grains\n", "").replace("Milk Choice\n", "").replace("Misc.\n", "").replace("Milk\n", "").replace("\nCondiments", "").replace("\n", " & ") for lunch in food]
        days = [date.text for date in dates]
        #  below creates a faux-ISO date with "i" (in the dictionary comprehension) rather than the hardcoded date
        lunch_menu = {f"{self.current_year}-{self.current_month}-{days[i]}": lunches[i] for i in range(len(lunches))}
        # lunch_menu = {self.current_year: [lunch_menu]}

        self.driver.quit()
        return lunch_menu
