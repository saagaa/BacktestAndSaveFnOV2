from FuturesOptions.PriceFindLibrary import *


def calender_get_day_values(symbol, current_date, current_expiry, next_expiry):
    out = {}

    out['current_date'] = current_date.strftime("%d-%b-%Y")
    out['current_expiry_date'] = current_expiry.strftime("%d-%b-%Y")
    out['next_expiry_date'] = next_expiry.strftime("%d-%b-%Y")
    out['current_expiry_price'] = get_index_price_futures(symbol, current_date, current_expiry)
    out['next_expiry_price']=get_index_price_futures(symbol, current_date, next_expiry)
    out['underlying_security'] = get_index_prices(symbol,current_date)
    return out

def calender_get_month_values(symbol,start_date, current_expiry, next_expiry):
    out =[]
    while start_date!=current_expiry+datetime.timedelta(1):
        out.append(calender_get_day_values(symbol,start_date,current_expiry,next_expiry))
        start_date=start_date+datetime.timedelta(1)
    print(out)
    return out

def doCalender(symbol, start_date, year_limit, expiries):
    out =[]
    year = start_date.year
    try:
        while year <year_limit:
            currentexpiry = expiries[start_date.year][start_date.month]
            newdate = start_date
            while currentexpiry < start_date:
                newdate= newdate + datetime.timedelta(1)
                currentexpiry = expiries[newdate.year][newdate.month]

            nextdate  = currentexpiry + relativedelta(months=+1)
            nextexpiry = expiries[nextdate.year][nextdate.month]
            print("startDate:" + str(start_date) + " expiry:" + str(currentexpiry) + " expiry2:" + str(nextexpiry))
            out.append(calender_get_month_values(symbol,start_date,currentexpiry,nextexpiry))
            start_date=currentexpiry + datetime.timedelta(1)
            year = start_date.year
    except:
        return out
    return out


