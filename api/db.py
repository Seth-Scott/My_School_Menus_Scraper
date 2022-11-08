import pymongo
from get_dates import GetDates
import os


class DatabaseIntegration:
    def __init__(self):
        self.mongo_ip = os.getenv("mongo_ip")
        self.mongo_port = 27017

        self.get_date = GetDates()

        # MongoDB integration
        self.myclient = pymongo.MongoClient(f"mongodb://{self.mongo_ip}:{self.mongo_port}/")
        self.mongodb_db = self.myclient["schoolmenu"]
        self.mongodb_collection = self.mongodb_db["lunch"]

    def get_all_lunches(self):
        # TODO exception handling
        return {db_item["date"]: db_item['lunch'] for db_item in self.mongodb_collection.find()}

    def get_lunch_today(self):
        try:
            return self.mongodb_collection.find_one({"date": str(self.get_date.iso_date)})['lunch']
        except TypeError:
            return "Unknown"

    def get_lunch_tomorrow(self):
        try:
            return self.mongodb_collection.find_one({"date": str(self.get_date.tomorrow_iso_date)})['lunch']
        except TypeError:
            return "Unknown"

