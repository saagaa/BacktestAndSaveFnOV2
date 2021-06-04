
from nsepy import get_history
from nsepy.derivatives import get_expiry_date
import datetime
from dateutil.relativedelta import relativedelta


import pickle
from datetime import date
import time

expiryDatesIndex = {}
expiryDatesStock = {}
expiryDatesVix = {}


symbolPricesCurrentFutures = {}
symbolPricesCurrentOptions = {}
symbolPricesCurrentIndex = {}
expiries= {}
count_initialize =0

def setIndexData(indexData):
    global symbolPricesCurrentIndex
    symbolPricesCurrentIndex = indexData




def setOptionsData(optionsData):
    global symbolPricesCurrentOptions
    symbolPricesCurrentOptions = optionsData

def setFuturesData(futureData):
    global symbolPricesCurrentFutures
    symbolPricesCurrentFutures = futureData

def getOptionData():
    global symbolPricesCurrentOptions
    return symbolPricesCurrentOptions

def getFutureData():
    global symbolPricesCurrentFutures
    return symbolPricesCurrentFutures

def getIndexData():
    global symbolPricesCurrentIndex
    return symbolPricesCurrentIndex

def init():
    if(count_initialize!=0):
        return
    ++count_initialize
    global expiries
    expiries  = get_expiry_date(2010,1,index=True)
    print (expiries)

def get_expiry(year, month):
    return expiries[year][month]

def round_off(x, base=50):
    return base * round(x/base)


def get_index_price_futures(symbol, date, expiryDateTime, index):
    global symbolPricesCurrentFutures
    try:
        a = symbolPricesCurrentFutures[symbol][expiryDateTime][date]
        if(a!=None) :
            return a
    except:
        a=0

    # print("exception\n")
    if symbol not in symbolPricesCurrentFutures.keys():
        # print("adding symbol\n")
        symbolPricesCurrentFutures[symbol]={}
    if expiryDateTime not in symbolPricesCurrentFutures[symbol]:
        # print("adding expiry\n")
        symbolPricesCurrentFutures[symbol][expiryDateTime] = {}

    try:
        value= get_history(symbol,date,date,index=index,futures=True, expiry_date=expiryDateTime)['Close'][0]
        # print("future date: "+ str(date) + "price :" + str(value))
    except:
        value = 0
    # print(str(value) + "added")
    symbolPricesCurrentFutures[symbol][expiryDateTime][date] = value
    return value




def get_index_price_options(symbol, optionType, strikePrice, date, expiryDateTime, index):
    global symbolPricesCurrentOptions
    # print(str(optionType)  + " strike:" + str(strikePrice) + " date:"+str(date) + " expiry:" +str(expiryDateTime))
    try:
        a= symbolPricesCurrentOptions[symbol][expiryDateTime][strikePrice][optionType][date]
        #if a!=0:
        return a
    except:
        if symbol not in symbolPricesCurrentOptions.keys():
            symbolPricesCurrentOptions[symbol]={}
        if expiryDateTime not in symbolPricesCurrentOptions[symbol].keys():
            symbolPricesCurrentOptions[symbol][expiryDateTime]={}
        if strikePrice not in symbolPricesCurrentOptions[symbol][expiryDateTime].keys():
            symbolPricesCurrentOptions[symbol][expiryDateTime][strikePrice]={}
        if optionType not in symbolPricesCurrentOptions[symbol][expiryDateTime][strikePrice].keys():
            symbolPricesCurrentOptions[symbol][expiryDateTime][strikePrice][optionType]={}
        try:

            value  =get_history(symbol,date,date,index=index,option_type=optionType,strike_price=strikePrice, expiry_date=expiryDateTime  )['Close'][0]


        except:
            value =0
        symbolPricesCurrentOptions[symbol][expiryDateTime][strikePrice][optionType][date]= value
        return value


def get_index_prices(symbol, date, index):
    global symbolPricesCurrentIndex
    try:
        a = symbolPricesCurrentIndex[symbol][date]
        if(a!=None) :
            return a
    except:
        a=0

    # print("exception\n")
    if symbol not in symbolPricesCurrentIndex.keys():
        # print("adding symbol\n")
        symbolPricesCurrentIndex[symbol]={}

    try:
        value= get_history(symbol,date,date,index=index,futures=False)['Close'][0]
        # print("future date: "+ str(date) + "price :" + str(value))
    except:
        value = 0
    # print(str(value) + "added")
    symbolPricesCurrentIndex[symbol][date] = value
    return value