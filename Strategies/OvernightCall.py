from DataFetcher.CommonTypes import *
from DataFetcher.DataBase.DataBaseAggregator import *
from pandas.tseries.offsets import *
from Strategies.StrategyUtils import *
import nsepy

class Context:
    def __init__(self):
        return

# class PyFolioHelper:
#     def __init__(self, symbols: List[str], cash: int):
#         self.transactions:pd.DataFrame = pd.DataFrame(columns=["symbol", "amount", "price"], index = pd.to_datetime([]))
#         self.transactions.index.name = "date"
#
#         self.positions:pd.DataFrame = pd.DataFrame( columns=symbols.append("cash"), index = pd.to_datetime([]))
#         self.positions.index.name = "date"
#
#         self.returns:pd.DataFrame = pd.DataFrame(columns=['returns'], index = pd.to_datetime([]))
#         self.returns.index.name = "date"
#
#         self.cash:int = cash
#
#     def buyStock(self, symbol:str, amount:float, price:float, transactionTime: datetime):
#         self.transactions.loc[transactionTime] pd.Series([symbol,amount, price], ["symbol", "amount", "price"])
#         self.transactions.append({"symbol":symbol, "amount:"})
#         self.positions.loc[transactionTime]
#
#     def sellStock(self, symbol:str, amount:float, price:float, transactionTime: datetime):
#         self.transactions.loc[transactionTime] = pd.Series([symbol,-amount, price], ["symbol", "amount", "price"])
#
#     def compute(self):
#         self.transactions = self.transactions.sort_index()
#         transactions_copy:pd.DataFrame = self.transactions
#         transactions_copy.groupby(["date","symbol"]).

class OvernightCallStrategy:
    def __init__(self, DB: DataBaseAggregator, stock: str, cash: float):
        self.DB = DB
        self.stock = stock
        self.cash = cash
        self.lotSize = 75
        return

    def findExpiry( self, curr_dt)->date:
        curr_dt = convertToDate(curr_dt)
        min_expiry_dt = convertToDate( curr_dt + relativedelta(days=+15) )
        expiries = nsepy.derivatives.get_expiry_date(year = min_expiry_dt.year, month = min_expiry_dt.month )
        return max(expiries)
        # min_expiry_dt =  convertToDate( curr_dt + relativedelta(days=+30) )
        # for dt in expiries:
        #     dt = convertToDate(dt)
        #     if( ( dt- curr_dt).days >=15 ):
        #         min_expiry_dt = min( convertToDate( min_expiry_dt ) , convertToDate( dt ) )
        # return min_expiry_dt

    def get_slight_OTM_price_from_curr_price( self,  curr_price )->int:
        lower_price = curr_price - curr_price%50
        upper_price = lower_price  + 50
        return upper_price

    def get_slight_OTM_price_from_date( self, curr_dt )->int:
        datePair: DatePair = (curr_dt, curr_dt+relativedelta(days=+1))
        curr_price = self.DB.get_index_prices( self.stock, datePair, DataGranularity.Daily )
        return self.get_slight_OTM_price_from_curr_price( curr_price[DataOptions.Close][curr_dt] )

    def CacheWarmUp(self, startDate, endDate):
        self.DB.get_index_prices(self.stock, (startDate, endDate), DataGranularity.Daily)
        self.DB.DataFetcherConfig.LookBack = 0
        self.DB.DataFetcherConfig.LookForward = 1

    def RunStrategy(self, startDate: date, endDate: date):
        self.CacheWarmUp(startDate,endDate)
        self.position = pd.DataFrame( columns=[ "cash", "Total", "BuyPrice", "SellPrice", "BuyStrike", "SellStrike"], index = pd.to_datetime([]))
        cash = self.cash
        boughtExpiry:date = None
        boughtStrike:int = 0
        boughtAmount:int = 0
        currDate = startDate
        while currDate <= endDate:
            try:
                if( currDate.weekday()>=5):
                    currDate= currDate+ relativedelta(days=+1)
                    continue

                self.position.loc[currDate] = pd.Series([0, 0, 0, 0, 0, 0], ["cash", "Total","BuyPrice","SellPrice", "BuyStrike", "SellStrike"])
                # first sell the call
                if boughtAmount > 0:
                    cost = self.DB.get_index_price_options(self.stock, OptionType.Call, boughtStrike, (currDate,currDate), convertToDateTime(boughtExpiry), DataGranularity.Daily)
                    if( DataFrameUtils.ValidateDataFrame(cost) == False):
                        cost = self.DB.get_index_price_options(self.stock, OptionType.Call, boughtStrike, (currDate,currDate), convertToDateTime(boughtExpiry), DataGranularity.Daily, forceDownloadData=True)
                    cash += boughtAmount*cost[DataOptions.Open][currDate]
                    self.position.loc[currDate]["SellPrice"] = cost[DataOptions.Open][currDate]
                    self.position.loc[currDate]["SellStrike"] =  boughtStrike

                boughtStrike = self.get_slight_OTM_price_from_date(currDate)
                boughtExpiry = self.findExpiry(currDate)
                costDF = self.DB.get_index_price_options(self.stock, OptionType.Call, boughtStrike, (currDate,currDate), convertToDateTime(boughtExpiry), DataGranularity.Daily)

                # while(True):
                #     if( DataFrameUtils.ValidateDataFrame(costDF)==False):
                #         costDF = self.DB.get_index_price_options(self.stock, OptionType.Call, boughtStrike,
                #                                                  (currDate, currDate), convertToDateTime(boughtExpiry),
                #                                                  DataGranularity.Daily, forceDownloadData=True)
                #     if( costDF[DataOptions.NumberOfContracts]>2000):
                #         break
                #     boughtExpiry = self.findExpiry(currDate+relativedelta(days=+1))

                cost = costDF[DataOptions.Close][currDate]
                boughtAmount = int( cash/ cost )
                # bought the call at the end of the day
                cash-=boughtAmount*cost
                self.position.loc[currDate]["BuyPrice"] = cost
                self.position.loc[currDate]["cash"] = cash
                self.position.loc[currDate]["Total"] = cash+(boughtAmount*cost)
                self.position.loc[currDate]["BuyStrike"] = boughtStrike

                #self.position.loc[currDate] = pd.Series( [ cash, cash+(boughtAmount*cost) ], [ "cash", "Total" ])
                currDate = currDate + relativedelta(days=+1)
            except Exception as e:
                traceback.print_exc()
                print(e)
                print( "neglected the date " + str( currDate ))
                currDate = currDate + relativedelta(days=+1)
        return self.position