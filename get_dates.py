import datetime


class GetDates:
    def __init__(self):
        # returns formatted date range for
        self.day = datetime.datetime.now().day
        self.month = datetime.datetime.now().month
        self.year = datetime.datetime.now().year

        self.iso_date = datetime.date(year=self.year, month=self.month, day=self.day)
        self.tomorrow_iso_date = datetime.date(year=self.year, month=self.month, day=self.day + 1)

