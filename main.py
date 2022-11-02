from scraper import Scraper
from get_dates import GetDates
import pymongo
import os

get_date = GetDates()
scraper = Scraper()

mongo_ip = os.getenv("mongo_ip")
mongo_port = os.getenv("mongo_port")

menu = scraper.scrape(get_date.tomorrow_iso_date.strftime("%Y-%m"))

# MongoDB integration
myclient = pymongo.MongoClient(f"mongodb://{mongo_ip}:{mongo_port}/")
mongodb_db = myclient["schoolmenu"]
mongodb_collection = mongodb_db["lunch"]

# TEMPORARY - FOR DEV PRIOR TO DEPLOY
# mongodb_collection.drop()

# the "upsert" argument prevents already existing items to be added to the database
for date, food_item in menu.items():
    mongo_format = {"date": date, "lunch": food_item}
    mongodb_collection.update_one(mongo_format, {"$set": mongo_format},
                                  upsert=True)
for x in mongodb_collection.find():
    print(x)





