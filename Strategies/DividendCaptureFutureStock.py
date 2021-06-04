from DataFetcher.CommonTypes import *
from DataFetcher.DataBase.DataBaseAggregator import *
from pandas.tseries.offsets import *
from Strategies.StrategyUtils import *

class Context:
    def __init__(self):
        return

class DividendCaptureFutureStock:
    def __init__(self, stock:str, DB: DataBaseAggregator):
        self.DB = DB
        self.stock = stock
        return

    def RunStrategy(self, dividends: List[Tuple[datetime, float]]):
        for dividend in dividends:
            returns = self.RunStrategyOnSingleDividend( dividend[0], dividend[1])
            print( "returns on dividendDate: " + str( dividend[0] ) + " = " +str( returns.item() ) )


    def RunStrategyOnSingleDividend(self, exDate: datetime, dividendAmount: float):
        buyDate = exDate-BDay(1)
        sellDate = exDate+BDay(3)
        buyDate = datetime.combine( buyDate.date() , datetime.min.time())
        sellDate = datetime.combine( sellDate.date(), datetime.min.time() )
        underlying = self.DB.get_index_prices(self.stock, ( buyDate, sellDate ), DataGranularity.Daily )
        futureExpiry = get_month_expiry( sellDate.year, sellDate.month )
        future = self.DB.get_index_price_futures( self.stock, (buyDate, sellDate), futureExpiry, DataGranularity.Daily )

        stockBuy = underlying[DataOptions.Close][buyDate]
        futureSell = future[DataOptions.Close][buyDate]

        if( futureSell- stockBuy <= dividendAmount ):
            stockSell = underlying[DataOptions.Close][sellDate]
            futureBuy = future[DataOptions.Close][sellDate]

            returns = ( ( futureSell - futureBuy ) + ( stockSell - stockBuy) + dividendAmount ) / (1.2* ( stockBuy))

            return returns
        else:
            print( "cant do" + self.stock + " on dividend " + str(exDate) + " expiry:" + str(futureExpiry) )
        return

