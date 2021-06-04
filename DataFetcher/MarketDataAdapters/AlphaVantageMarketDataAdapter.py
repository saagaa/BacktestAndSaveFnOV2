
from DataFetcher.CommonTypes import *


class AlphaVantageMarketDataAdapter(IMarketDataAdapter):
    AlphaVantageAPIKey = "3W2ZX6J5XD6W1SIZ"

    @abstractmethod
    def get_price_futures(self, symbol:str, dates:DatePair, expiryDateTime:datetime):
        raise ("Cant use Alphavantage for futures data")
        pass

    @abstractmethod
    def get_price_options(self, symbol:str, optionType:OptionType, strikePrice:int, dates:DatePair, expiryDateTime:datetime):
        raise ("Cant use Alphavantage for options data")
        pass

    @abstractmethod
    def get_price_scrip(self, symbol:str, dates:DatePair, granularity: DataGranularity):

        pass
