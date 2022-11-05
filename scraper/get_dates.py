import datetime
from datetime import timedelta
import calendar


class GetDates:
    def __init__(self):
        # returns formatted date range for
        self.day = datetime.datetime.now().day
        self.month = datetime.datetime.now().month
        self.year = datetime.datetime.now().year
        # ISO 8601 format
        self.iso_date = datetime.date(year=self.year, month=self.month, day=self.day)
        self.tomorrow_iso_date = self.iso_date + timedelta(1)
        # first day of the month
        self.first_dom = datetime.date(year=self.year, month=self.month, day=1)
        # last day of the month
        self.last_dom = self.iso_date.replace(day=calendar.monthrange(self.iso_date.year, month=self.iso_date.month)[1])




