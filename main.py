from scraper import Scraper
from mqtt_integration import MqttClient
from get_dates import GetDates
import json
import pymongo

# make sure environment variables are accessible
# TODO build docker with dependencies (unraid)
# TODO run api program on cronjob

scraper = Scraper()
menu = scraper.scrape()
get_date = GetDates()

# MongoDB integration
myclient = pymongo.MongoClient("mongodb://192.168.0.16:27017/")
mongodb_db = myclient["schoolmenu"]
mongodb_collection = mongodb_db["lunch"]
# the "upsert" argument prevents already existing items to be added to the database
for date, food_item in menu.items():
    mongo_format = {"date": date, "lunch": food_item}
    mongodb_collection.update_one(mongo_format, {"$set": mongo_format},
                                  upsert=True)

# for x in mongodb_collection.find():
#     print(x)


# with open('data.json', mode='w') as menu_api:
#     json.dump(menu, menu_api, indent=4)


lunch_tomorrow = mongodb_collection.find_one({"date": f"{get_date.tomorrow_iso_date}"})['lunch']
print(lunch_tomorrow)


#  MQTT integration
mqtt = MqttClient()

while True:
    mqtt.post_message(lunch_tomorrow, 3, 'school/food/lunch')
