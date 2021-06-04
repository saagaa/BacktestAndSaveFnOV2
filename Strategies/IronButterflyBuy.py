from DataFetcher.DataSource.DataBase import *
import datetime
from dateutil.relativedelta import relativedelta
from Utils import OptionProbabilityCalc
from Utils import TradingDays,TradingMargins,OptionChainLeastCount,MathUtils
from joblib import Parallel, delayed
from  Structs.AtomicInteger import *
from Structs.Spread import *
import multiprocessing
import math


class IronButterflyBuy:
    symbol = ""
    index = False
    minProbOfProfit = 0
    minReturn = 0
    leastCount =100
    IndexValue = {}
    counter = 0
    inTheMoneyOptions = False
    atomicCounter = AtomicInteger()
    db = DataBase

    def __init__(self):
        return

    def load_dataSourceVars( self, DataBase ):
        self.db=DataBase
        return

    def ComputeStrategyReturns(self, startDates, endDates, expiryDates, minProbOfProfit, minReturn, index, symbol, inTheMoneyOptions):
        self.symbol = symbol
        self.index = index
        self.minProbOfProfit = minProbOfProfit
        self.minReturn = minReturn
        self.leastCount = OptionChainLeastCount.get_least_count(self.symbol)
        self.DownloadAllData(startDates,endDates)
        self.inTheMoneyOptions = inTheMoneyOptions
        length = min( len(startDates) , len(endDates) )
        num_cores = multiprocessing.cpu_count()
        results = Parallel(n_jobs=num_cores-1, prefer = "threads")(delayed(self.iron_butterfly_duration)(startDates[i],endDates[i], expiryDates[i]) for i in range(0,length) )
        print("=======================================================================================")
        print("========================================RESULTS========================================")
        print("=======================================================================================")
        lastDayValue =0
        for result in results:
            print (result)
            if( "lastDayProfit" in result.keys() ):
                lastDayValue+=result['lastDayProfit']
        return lastDayValue

    def iron_butterfly_duration(self, startDate,endDate, expiryDate ):
        margin = TradingMargins.get_Option_Margin( False )  # margin per sell option
        # strike price changes if cp ==0 //////////////////////7
        futureprice = self.db.get_index_prices( self.symbol, startDate, self.index)
        arr_profits = []


        strikeprice = MathUtils.round_off(futureprice, self.leastCount)
        ####
        ###print(
        ###    "underlying security price on Date: " + str(startDate) + " is " + str(futureprice) + " strikePrice " + str(
        ###        strikeprice))
        ####
        costPrice,sigmaDay = 0,0
        spread = Spread(0,0)
        if( strikeprice != 0):
            spread,sigmaDay = self.getSpreadFromProbability(startDate,expiryDate)
            costPrice = self.iron_butterfly_date_cost( strikeprice, spread, startDate, expiryDate )
        # print("date :"+str(startDate)+ "costPrice :" + str(costPrice))
        while costPrice == 0:
            if expiryDate == startDate:
                return {}
            startDate = startDate + datetime.timedelta(1)
            if( TradingDays.isWeekDay( startDate) ):
                futureprice = self.db.get_index_prices(self.symbol, startDate, self.index)
                if( futureprice != 0):
                    strikeprice = MathUtils.round_off(futureprice, self.leastCount)
                    ###print("underlying security price on Date: " + str(startDate) + " is " + str(
                    ###    futureprice) + " strikePrice " + str(strikeprice))
                    spread, sigmaDay = self.getSpreadFromProbability( startDate, expiryDate, sigmaDay )
                    costPrice = self.iron_butterfly_date_cost( strikeprice, spread, startDate, expiryDate )

        # print("startDate :" + str(startDate) + "expiry :" + str(expiryDate) + "spread :" + str(
        #     spread) + "costPrice :" + str(costPrice))
        # print("date :"+str(startDate)+ "costPrice :" + str(costPrice))
        # if cost price is negative that means
        setupcost = futureprice * 2 * margin + costPrice
        evaluationDate = startDate + datetime.timedelta(1)
        holidays = 0
        ProfitTillNow = 0
        costs = []
        costs.append(costPrice)
        while expiryDate >= evaluationDate:
            sellPrice = self.iron_butterfly_date_cost( strikeprice, spread, evaluationDate, expiryDate )
            #print("sellPrice at " + str(evaluationDate) + " : " + str(sellPrice))
            if (sellPrice != 0):
                arr_profits.append((sellPrice - costPrice) / setupcost)
                costs.append(sellPrice)
            else:
                ++holidays
            evaluationDate = evaluationDate + datetime.timedelta(1)
        arr_profits.reverse()
        obj = {}
        obj['startDate'] = startDate
        obj['expiry'] = expiryDate
        obj['strikePrice'] = strikeprice
        obj['lastDayProfit'] = 0
        obj['spread_upper'] = spread.upper
        obj['spread_lower'] = spread.lower
        obj['sigma'] = sigmaDay

        if len( arr_profits ) != 0:
            obj['min'] = min(arr_profits)
            obj['max'] = max(arr_profits)
            obj['holidays'] = holidays
            obj['profit_percentage'] = arr_profits
            obj['costs'] = costs
            obj['lastDayProfit'] = arr_profits[0]

        print(obj)
        return obj

    def doButterfly(self,startDate, yearLimit, expiries):
        output = []
        year = startDate.year
        try:
            while year != yearLimit:
                print(startDate)
                # nextmonth =month+1
                # nextyear=year
                # if(nextmonth==13):
                #     nextyear=year+1
                #     nextmonth=1

                nextmonthexpiry = expiries[startDate.year][startDate.month]

                if (nextmonthexpiry <= startDate):
                    newDate = startDate + relativedelta(months=+1)
                    nextmonthexpiry = expiries[newDate.year][newDate.month]
                # while get_index_price_futures('NIFTY',startDate,nextmonthexpiry) == 0 and (nextmonthexpiry - startDate) != datetime.timedelta(0):
                #     startDate = startDate + datetime.timedelta(1)
                print("startDate:" + str(startDate) + " expiry:" + str(nextmonthexpiry))
                output.append( self.iron_butterfly_month(startDate, nextmonthexpiry, index=True))
                startDate = nextmonthexpiry + datetime.timedelta(1)
                year = startDate.year
                month = startDate.month
        except:
            return output
        return output

    def iron_butterfly_date_cost(self, strikeprice, spread, currentDate, expiryDate):
        costPrice = 0
        try:
            if self.inTheMoneyOptions == False:
                costPrice += self.db.get_index_price_options(self.symbol, 'CE', strikeprice, currentDate, expiryDate, self.index)
                costPrice += self.db.get_index_price_options(self.symbol, 'PE', strikeprice, currentDate, expiryDate, self.index)
                costPrice -= self.db.get_index_price_options(self.symbol, 'CE', spread.upper, currentDate, expiryDate, self.index)
                costPrice -= self.db.get_index_price_options(self.symbol, 'PE', spread.lower, currentDate, expiryDate, self.index)
            else:
                costPrice += self.db.get_index_price_options(self.symbol, 'CE', strikeprice, currentDate, expiryDate, self.index)
                costPrice += self.db.get_index_price_options(self.symbol, 'PE', strikeprice, currentDate, expiryDate, self.index)
                costPrice -= self.db.get_index_price_options(self.symbol, 'CE', spread.lower, currentDate, expiryDate, self.index)
                costPrice -= self.db.get_index_price_options(self.symbol, 'PE', spread.upper, currentDate, expiryDate, self.index)

        except Exception as e:
            print( str(e) + "occured while iron_butterfly_date_cost(" + str(strikeprice) +","+ str(spread.upper) +"," + str(spread.lower) + ","+ str(currentDate) + "," +str(expiryDate))

        return costPrice


    def getSpreadFromProbability(self, currentDate, expiryDate , sigmaDay = 0):
        if( sigmaDay == 0):
            sigmaDay  = self.db.get_volatility(self.symbol, self.index, currentDate + relativedelta(months=-1 ) , currentDate)
        days = TradingDays.calculateTradingDays( currentDate,expiryDate )
        sigma = sigmaDay * math.sqrt(days)
        spread = OptionProbabilityCalc.getRangeWithLeastCountRoundOff(self.db.get_index_prices(self.symbol, currentDate, self.index),sigma,self.minProbOfProfit, self.leastCount)
        return spread,sigmaDay

    def DownloadAllData(self, startDates, endDates ):
        daysSet = set()
        for i in range (0,min(len(startDates), len(endDates))):
            daysSet.update( TradingDays.getWorkdays( startDates[i]+ relativedelta(months=-1), endDates[i]) )

        num_cores = multiprocessing.cpu_count()
        result  = Parallel(n_jobs=num_cores-1, prefer="threads")(delayed(self.DownloadIndexData)(dt) for dt in daysSet)
        return result

    def DownloadIndexData(self, date):
        self.IndexValue[date] = self.db.get_index_prices(self.symbol, date, self.index)
        self.atomicCounter.increment()
        print("done" + str(self.atomicCounter.value()))
        return