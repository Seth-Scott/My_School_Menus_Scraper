import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from get_dates import GetDates
import time

get_date = GetDates()
WEBDRIVER_ADDRESS = os.getenv("WEBDRIVER_ADDRESS")


class Scraper:
    def __init__(self):
        self.instance = os.getenv("INSTANCE")
        self.district = os.getenv("DISTRICT")
        self.school = os.getenv("SCHOOL")
        # it looks like menu changes between school years?
        self.menu = os.getenv("MENU")

        self.options = webdriver.FirefoxOptions()
        self.options.add_argument('--ignore-ssl-errors=yes')
        self.options.add_argument('--ignore-certificate-errors')

        while True:
            try:
                print(f"Connecting to Selenium remote webdriver on {WEBDRIVER_ADDRESS}")
                self.driver = webdriver.Remote(command_executor=WEBDRIVER_ADDRESS, options=self.options)
            # TODO exception handling not specific enough
            except:
                print("ERROR! It's likely Selenium remote webdriver is not running (yet). Trying again in 10s")
                time.sleep(10)
                continue
            else:
                print("Successfully connected to Selenium remote webdriver..")
                break

    def scrape(self, desired_scrape_date):
        self.driver.get(
            f"https://www.myschoolmenus.com/instance/{self.instance}/district/{self.district}/school/{self.school}/menu/{self.menu}/?date={desired_scrape_date}")
        self.driver.implicitly_wait(10)
        dates = self.driver.find_elements(By.CLASS_NAME, "calendar-day")
        food = self.driver.find_elements(By.CLASS_NAME, "menu-entrees")
        lunches = [lunch.text.replace("Goldkist ", "").replace("Entree\n", "").replace("Vegetables\n", "").replace("Fruit and Vegetable Variety\n", "").replace("Grains\n", "").replace("Milk Choice\n", "").replace("Misc.\n", "").replace("Milk\n", "").replace("\nCondiments", "").replace("\n", " & ") for lunch in food]
        # create a list of days and remove the empties
        days = [date.text for date in dates if date.text != ""]
        #  below creates a faux-ISO date with "i" (in the dictionary comprehension) rather than the hardcoded date, remove empties
        lunch_menu = {f"{desired_scrape_date}-{days[i]}": lunches[i] for i in range(len(lunches)) if lunches[i] != ""}
        # lunch_menu = {datetime.date(year=get_date.year, month=get_date.month, day=int(days[i])): lunches[i] for i in range(len(lunches))}

        self.driver.quit()
        return lunch_menu
