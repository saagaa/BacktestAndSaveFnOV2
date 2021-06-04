
from nsepy import get_history
from nsepy.derivatives import get_expiry_date
from nsepy.derivatives import SetProxyServer
import numpy as np
from dateutil.relativedelta import relativedelta
from Utils import TradingDays
from Utils.MathUtils import *
import pickle
import DataFetcher.DataSource.IDataBase


class DataBase (DataFetcher.DataSource.IDataBase):

    expiryDatesIndex = {}
    expiryDatesStock = {}
    expiryDatesVix = {}


    symbolPricesCurrentFutures = {}
    symbolPricesCurrentOptions = {}
    symbolPricesCurrentIndex = {}
    expiries= {}
    count_initialize =0


    def Initialize(self):
        try:
            pickle_in = open("futures.pickle", "rb")
            self.symbolPricesCurrentFutures = pickle.load(pickle_in)
        except:
            f = 0

        print(self.symbolPricesCurrentFutures)

        try:
            pickle_in = open("options.pickle", "rb")
            self.symbolPricesCurrentOptions = pickle.load(pickle_in)
        except:
            f = 0
        print(self.symbolPricesCurrentOptions)

        try:
            pickle_in = open("index.pickle", "rb")
            self.symbolPricesCurrentIndex = pickle.load(pickle_in)
        except:
            f = 0
        self.init()
        print(self.symbolPricesCurrentIndex)

    def OnCompleteSave(self):
        pickle_out = open("futures.pickle", "wb")
        pickle.dump(self.symbolPricesCurrentFutures, pickle_out)
        pickle_out.close()

        pickle_out = open("options.pickle", "wb")
        pickle.dump(self.symbolPricesCurrentOptions, pickle_out)
        pickle_out.close()

        pickle_out = open("index.pickle", "wb")
        pickle.dump(self.symbolPricesCurrentIndex, pickle_out)
        pickle_out.close()

    def init(self):
        if(self.count_initialize!=0):
            return
        ++self.count_initialize
        self.expiries  = get_expiry_date(2010,1,index=True)
        print (self.expiries)

    def get_expiry( self, year, month):
        return self.expiries[year][month]



    def get_index_price_futures(self, symbol, date, expiryDateTime, index):
        try:
            a = self.symbolPricesCurrentFutures[symbol][expiryDateTime][date]
            if IsValidDataPoint(a):
                return a
        except:
            a=0

        # print("exception\n")
        if symbol not in self.symbolPricesCurrentFutures.keys():
            # print("adding symbol\n")
            self.symbolPricesCurrentFutures[symbol]={}
        if expiryDateTime not in self.symbolPricesCurrentFutures[symbol]:
            # print("adding expiry\n")
            self.symbolPricesCurrentFutures[symbol][expiryDateTime] = {}

        try:
            value= get_history(symbol,date,date,index=index,futures=True, expiry_date=expiryDateTime)['Close'][0]
            # print("future date: "+ str(date) + "price :" + str(value))
        except Exception as e:
            print(str(e) + " occured while get_index_price_options("+ str(symbol) + "," +str(date) + "," + str(expiryDateTime) )
        # print(str(value) + "added")
        self.symbolPricesCurrentFutures[symbol][expiryDateTime][date] = value
        return value


    def get_index_price_options(self, symbol, optionType, strikePrice, date, expiryDateTime, index):
        # print(str(optionType)  + " strike:" + str(strikePrice) + " date:"+str(date) + " expiry:" +str(expiryDateTime))
        try:
            a= self.symbolPricesCurrentOptions[symbol][expiryDateTime][strikePrice][optionType][date]
            if IsValidDataPoint(a):
                return a
        except:
            if symbol not in self.symbolPricesCurrentOptions.keys():
                self.symbolPricesCurrentOptions[symbol]={}
            if expiryDateTime not in self.symbolPricesCurrentOptions[symbol].keys():
                self.symbolPricesCurrentOptions[symbol][expiryDateTime]={}
            if strikePrice not in self.symbolPricesCurrentOptions[symbol][expiryDateTime].keys():
                self.symbolPricesCurrentOptions[symbol][expiryDateTime][strikePrice]={}
            if optionType not in self.symbolPricesCurrentOptions[symbol][expiryDateTime][strikePrice].keys():
                self.symbolPricesCurrentOptions[symbol][expiryDateTime][strikePrice][optionType]={}
            try:
                value  =get_history(symbol,date,date,index=index,option_type=optionType,strike_price=strikePrice, expiry_date=expiryDateTime  )['Close'][0]


            except Exception as e:
                print(str(e) + " occured while get_index_price_options("+ str(symbol) + "," + str(optionType) +","  + str(strikePrice) +"," +str(date) + "," + str(expiryDateTime) )
                value =0

            self.symbolPricesCurrentOptions[symbol][expiryDateTime][strikePrice][optionType][date]= value
            return value


    def get_index_prices(self, symbol, date, index):
        try:
            a = self.symbolPricesCurrentIndex[symbol][date]
            if IsValidDataPoint(a) :
                return a
        except:
            a=0

        # print("exception\n")
        if symbol not in self.symbolPricesCurrentIndex.keys():
            # print("adding symbol\n")
            self.symbolPricesCurrentIndex[symbol]={}

        try:
            value= get_history(symbol,date,date,index=index,futures=False)['Close'][0]
            # print("future date: "+ str(date) + "price :" + str(value))
        except Exception as e:
            print(str(e) + " occured while get_index_price(" + str(symbol) +"," + str(date) )
            value = 0

        # print(str(value) + "added")
        self.symbolPricesCurrentIndex[symbol][date] = value
        return value

    def get_volatility(self, symbol , index , currentDate , endDate):
        arr = []
        while currentDate <= endDate:
            if( TradingDays.isWeekDay( currentDate ) ):
                v = self.get_index_prices(symbol, currentDate, index)
                if( v!=0 and v!= None):
                    arr.append( v )
            currentDate= currentDate + relativedelta(days=+1)
        return np.std( arr )

def SetProxy( url ):
    SetProxyServer(url)