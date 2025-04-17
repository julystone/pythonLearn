# encoding: utf-8
import re
from calendar import month
from datetime import datetime

GLOBAL_DICT = {}

class CalendarShfe:

    def __init__(self, date):
        self.date = date
        self.listings = {}
        self.expired = {}
        self.posLimit = {}
        self.bond = {}
        self.fee = {}

    def __repr__(self):
        return f"\n In __repr__：\n{repr(self.__dict__)}"


def monthly_calendar(month=None, year=None):
    import datetime
    import calendar

    today = datetime.date.today()

    if not month:
        month = today.month
    if not year:
        year = today.year

    last_day = calendar.monthrange(year, month)[1]
    for i in range(last_day):
        date = f"{year:04d}{month:02d}{i+1:02d}"
        calendar = CalendarShfe(date)
        GLOBAL_DICT.update({date: calendar})


def init_data_class(date):
    if not date:
        return
    calendar = GLOBAL_DICT.get(date, None)
    if not calendar:
        calendar = CalendarShfe(date)
        GLOBAL_DICT.update({date: calendar})
    return calendar

if __name__ == '__main__':
    monthly_calendar()