from FuturesOptions.PriceFindLibrary import *


def calender_get_day_values(symbol, current_date, current_expiry, next_expiry, index):
    out = {}

    out['current_date'] = current_date.strftime("%d-%b-%Y")
    out['current_expiry_date'] = current_expiry.strftime("%d-%b-%Y")
    out['next_expiry_date'] = next_expiry.strftime("%d-%b-%Y")
    out['current_expiry_price'] = get_index_price_futures(symbol, current_date, current_expiry, index)
    out['next_expiry_price']=get_index_price_futures(symbol, current_date, next_expiry, index)
    out['underlying_security'] = get_index_prices(symbol,current_date, index)
    return out

def calender_get_month_values(symbol,start_date, current_expiry, next_expiry, index):
    out =[]
    metrics = {}
    count =0
    entryCost =0.0
    profits_arr=[]
    marginPercentage=2/75
    dataAnal = {}
    while start_date!=current_expiry+datetime.timedelta(1):
        priceToday =calender_get_day_values(symbol,start_date,current_expiry,next_expiry, index)
        out.append(priceToday)
        if(entryCost==0.0 or entryCost==0):
            entryCost = priceToday['next_expiry_price'] - priceToday['current_expiry_price']
            margin = priceToday['underlying_security']*marginPercentage
            dataAnal['StartDate'] = start_date
            dataAnal['CurrentExpiryDate'] = priceToday['current_expiry_date']
            dataAnal['NextExpiryDate'] = priceToday['next_expiry_date']
        else:
            priceToday = priceToday['next_expiry_price'] - priceToday['current_expiry_price']
            profit = (priceToday - entryCost) / margin
            profits_arr.append(profit)
        start_date=start_date+datetime.timedelta(1)

    dataAnal['profit_arr']=profits_arr
    dataAnal['min'] = min(profits_arr)
    dataAnal['max'] = max(profits_arr)

    print(out)
    return out,dataAnal

def doCalender(symbol, start_date, year_limit, expiries, index = True):
    out =[]
    datas = []
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
            output, dataAnal =  calender_get_month_values(symbol,start_date,currentexpiry,nextexpiry, index)
            out.append(output)
            datas.append(dataAnal)
            start_date=currentexpiry + datetime.timedelta(1)
            year = start_date.year
    except:
        return datas
    return datas


