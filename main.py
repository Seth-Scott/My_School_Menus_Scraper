from scraper import Scraper
from mqtt_integration import MqttClient
from get_dates import GetDates
import json

# make sure environment variables are accessible
# TODO build docker with dependencies (unraid)
# TODO run api program on cronjob

scraper = Scraper()
menu = scraper.scrape()
get_date = GetDates()

with open('data.json', mode='w') as menu_api:
    json.dump(menu, menu_api, indent=4)

lunch_tomorrow = menu[get_date.year][0][str(get_date.tomorrow_iso_date)]


#  MQTT integration
mqtt = MqttClient()

while True:
    mqtt.post_message(lunch_tomorrow, 3, 'school/food/lunch')


