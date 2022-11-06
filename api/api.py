from flask import Flask
from flask_restful import abort, Api, Resource
from db import DatabaseIntegration
from get_dates import GetDates

app = Flask(__name__)
api = Api(app)

db = DatabaseIntegration()
get_dates = GetDates()

# TODO refactor to avoid global variables if possible
DATES = db.get_all_lunches()


def abort_if_date_doesnt_exist(date):
    if date not in DATES:
        abort(404, message="ERROR: NO DATA".format(date))


# shows a list of all lunches
class DateList(Resource):
    """ Displays a list of all lunches """
    def get(self):
        return DATES


# shows a lunch, ISO format
class Date(Resource):
    """ Displays the lunch for a specific date """
    def get(self, date):
        abort_if_date_doesnt_exist(date)
        return DATES[date]


# shows today's lunch
class Today(Resource):
    """ Displays today's lunch """
    def get(self):
        return db.get_lunch_today()


class Tomorrow(Resource):
    """ Displays tomorrow's lunch """
    def get(self):
        return db.get_lunch_tomorrow()


# API routing
api.add_resource(DateList, '/date')
api.add_resource(Date, '/date/<date>')
api.add_resource(Today, '/date/today/')
api.add_resource(Tomorrow, '/date/tomorrow/')

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5863)
