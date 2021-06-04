
from FuturesOptions.PriceFindLibrary import *


#cost to buy
def iron_contour_date_cost(symbol,strikeprice,spreadSmall, spreadBig,currentDate,expiryDate, index):
    costPrice=0
    costPrice += get_index_price_options(symbol, 'CE',strikeprice+spreadSmall,currentDate,expiryDate, index)
    costPrice += get_index_price_options(symbol,'PE', strikeprice-spreadSmall,currentDate,expiryDate, index)
    costPrice -= get_index_price_options(symbol, 'CE', strikeprice + spreadBig, currentDate,expiryDate , index)
    costPrice -= get_index_price_options(symbol, 'PE', strikeprice - spreadBig, currentDate,expiryDate, index)
    return costPrice


def iron_contour_month(startDate, expiryDate, index):
    cost =0
    symbol = 'BANKNIFTY'

    farSpreadPercent=0.05
    nearSpreadPercent = 0.015
    leastCount =100
    percentageProfitAim = 0.03
    margin=0.125 #margin per sell option
    #strike price changes if cp ==0 //////////////////////7
    futureprice = get_index_price_futures(symbol, startDate, expiryDate, index)
    arr_profits=[]
    strikeprice = round_off(futureprice, leastCount)
    print("underlying security price on Date: "+str(startDate)+ " is " + str(futureprice)+ " strikePrice " + str(strikeprice))
    nearSpread=round_off(futureprice*nearSpreadPercent,leastCount)
    farSpread = round_off(futureprice*farSpreadPercent,leastCount)
    costPrice=iron_contour_date_cost(symbol,strikeprice,nearSpread,farSpread,startDate,expiryDate, index)
    # print("date :"+str(startDate)+ "costPrice :" + str(costPrice))
    while costPrice==0 :
        if expiryDate == startDate :
            return {}
        startDate = startDate+datetime.timedelta(1)
        futureprice = get_index_price_futures(symbol, startDate, expiryDate, index  )
        strikeprice = round_off(futureprice, leastCount)
        print("underlying security price on Date: "+str(startDate)+ " is " + str(futureprice)+ " strikePrice " + str(strikeprice))
        nearSpread=round_off(futureprice*nearSpreadPercent,leastCount)
        farSpread = round_off(futureprice*farSpreadPercent,leastCount)
        costPrice=iron_contour_date_cost(symbol,strikeprice,nearSpread,farSpread,startDate,expiryDate, index)

    print("startDate :"+str(startDate)+ "expiry :" +str(expiryDate)+ "nearSpread :"+str(nearSpread)+ "farSpread :" +str(farSpread)+ "costPrice :" + str(costPrice))
    # print("date :"+str(startDate)+ "costPrice :" + str(costPrice))
    # if cost price is negative that means
    setupcost = futureprice*2*margin + costPrice
    evaluationDate = startDate + datetime.timedelta(1)
    holidays=0
    ProfitTillNow  =0
    costs=[]
    costs.append(costPrice)
    while expiryDate >= evaluationDate:
        sellPrice = iron_contour_date_cost(symbol,strikeprice,nearSpread,farSpread,evaluationDate,expiryDate, index )
        print("sellPrice at " + str(evaluationDate) + " : " + str(sellPrice))
        if(sellPrice!=0):
           arr_profits.append((sellPrice-costPrice)/setupcost)
           costs.append(sellPrice)
        else:
            ++holidays
        evaluationDate = evaluationDate + datetime.timedelta(1)
    arr_profits.reverse()
    obj ={}
    obj['startDate']=startDate
    obj['expiry']=expiryDate
    obj['strikePrice'] = strikeprice
    obj['min']=min(arr_profits)
    obj['max']=max(arr_profits)
    obj['holidays'] = holidays
    obj['profit_percentage'] = arr_profits
    obj['costs'] = costs
    obj['nearSpread']=nearSpread
    obj['farSpread'] = farSpread
    print(obj)
    return obj


def doIronContour(startDate, yearLimit,expiries):
    output = []
    year = startDate.year
    #try:
    while year!=yearLimit:
        print(startDate)
        # nextmonth =month+1
        # nextyear=year
        # if(nextmonth==13):
        #     nextyear=year+1
        #     nextmonth=1

        nextmonthexpiry = expiries[startDate.year][startDate.month]

        if( nextmonthexpiry <= startDate ):
            newDate = startDate+relativedelta(months=+1)
            nextmonthexpiry = expiries[newDate.year][newDate.month]
        # while get_index_price_futures('NIFTY',startDate,nextmonthexpiry) == 0 and (nextmonthexpiry - startDate) != datetime.timedelta(0):
        #     startDate = startDate + datetime.timedelta(1)
        print("startDate:" + str(startDate) + " expiry:" + str(nextmonthexpiry))
        output.append(iron_contour_month(startDate,nextmonthexpiry, index =True))
        startDate = nextmonthexpiry+datetime.timedelta(1)
        year=startDate.year
        month = startDate.month
    #except:
        #return output
    return output