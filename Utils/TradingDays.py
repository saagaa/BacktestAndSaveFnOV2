import datetime as dt
import numpy as np
from dateutil.relativedelta import relativedelta

def calculateTradingDays( startDate, endDate):
    return np.busday_count( startDate, endDate + relativedelta(days=+1))

def getWorkdays(start, end, excluded=(6, 7)):
    days = []
    while start <= end:
        if start.isoweekday() not in excluded:
            days.append(start)
        start =start + relativedelta(days=+1)
    return days

def isWeekDay( date, excluded=(6, 7) ):
    if date.isoweekday() not in excluded:
        return True
    return False