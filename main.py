from scraper import Scraper
from mqtt_integration import MqttClient
import json

# make sure environment variables are accessible
# TODO build docker with dependencies (unraid)
# TODO run api program on cronjob

scraper = Scraper()
menu = scraper.scrape()


with open('data.json', mode='w') as menu_api:
    json.dump(menu, menu_api, indent=4)

print(menu)

#  MQTT integration
mqtt = MqttClient()

while True:
    mqtt.post_message('asdfasdfasdfd', 3, 'school/food/lunch')


