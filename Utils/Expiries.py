from nsepy.derivatives import get_expiry_date
import datetime
expiries = {}
count_initialize = 0


def init():
    global expiries
    global count_initialize

    if (count_initialize != 0):
        return
    ++count_initialize
    expiries = get_expiry_date(2010, 1, index=True)
    print(expiries)


def get_expiry(year, month):
    global expiries

    init()
    return expiries[year][month]


def get_month_expiry(year, month):

    if( year==2016 and month == 11):
        return datetime.datetime(2016,11,24)

    if( year==2018 and month ==3):
        return datetime.datetime(2018,3,28)
    if(year==2018 and month ==11):
        return datetime.datetime(2018,11,29)
    if( year==2019 and month ==3):
        return datetime.datetime(2019,3,28)
    if( year==2020 and month ==3):
        return datetime.datetime(2020,3,26)

    #global expiries

    #init()
    return max( get_expiry_date( year, month) )
