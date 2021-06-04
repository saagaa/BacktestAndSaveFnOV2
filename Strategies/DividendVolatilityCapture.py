from DataFetcher.CommonTypes import *
from DataFetcher.DataBase.DataBaseAggregator import *
from pandas.tseries.offsets import *
from Strategies.StrategyUtils import *

class Context:
    def __init__(self):
        return

class PairTrading_AllCorrelations_FX:
    def __init__(self, stock:str, startDate:datetime, endDate:datetime, DB: DataBaseAggregator):
        self.startDate = startDate
        self.endDate = endDate
        self.DB = DB
        self.stock = stock
        return

    def RunStrategy(self, dividends: List[Tuple[datetime, int, datetime]]):
        firstDividend = dividends[0]
        lastDivident = dividends[len(dividends)-1]
        data = self.DB.get_index_prices(self.stock, (firstDividend[0], ),DataGranularity.Daily)
        for dividend in dividends:
            self.CalculateReturn( dividend[0], dividend[1], dividend[2])

    def CalculateReturn(self, DividendDate: datetime, DividentAmount: int, DividentExDate: datetime):
        volatility = self.FetchTrailing1YearVolatility( DividendDate -BDay(3) )
        startDate = DividendDate - BDay(1)
        startVolatility = StrategyUtils.FetchTodaysVolatility(self.stock, self.DB, startDate)
        if(startVolatility > volatility[0]):
            context, startCost = self.SellVolatility(startDate)
        else:
            return
        arr = []
        arr.append(startCost)
        startDate = DividendDate
        while startDate <= DividentExDate + BDay(5):
            costOfHoldings = self.CalculateCostOfHoldings(startDate, context)
            if costOfHoldings < startCost:
                self.BuyVolatility(startDate,context)
                self.DeltaFlatten(startDate,context)
                return
            #else
            self.DeltaFlatten(startDate,context)
            startDate = startDate + BDay(1)
        self.BuyVolatility(startDate, context)
        return

    # TODO: returns Volatility's mean, sigma
    def FetchTrailing1YearVolatility(self, startDateTime: datetime) -> Tuple[float,float]:

        return (0.0, 0.0)

    def SellVolatility(self, date:datetime):
        context = Context()
        df = self.DB.get_index_prices(self.stock, (date,date),DataGranularity.Daily)
        context.OptionsStrike = df[DataOptions.Close][date]
        df = self.DB.get_index_price_options(self.stock, OptionType.Call, context.OptionsStrike, (date, date),
                                             self.GetCorrespondingExpiry(date), DataGranularity.Daily)
        context.OptionPrice = df[DataOptions.Close][date]
        context.Delta = self.GetDelta(df[DataOptions.Close][date], OptionType.Call, context.OptionsStrike)

        df = self.DB.get_index_price_options(self.stock, OptionType.Put, context.OptionsStrike, (date, date),
                                             self.GetCorrespondingExpiry(date), DataGranularity.Daily)
        context.OptionPrice += df[DataOptions.Close][date]



        #returns context, cost
        pass

    def BuyVolatility(self, date:datetime, context:Context):
        pass

    def CalculateCostOfHoldings(self, date:datetime, context:Context):
        #returns float
        pass

    def DeltaFlatten(self, date:datetime, context:Context):
        pass

    def GetDelta(self):