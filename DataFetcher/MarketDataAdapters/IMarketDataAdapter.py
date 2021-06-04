from abc import ABC, abstractmethod
from typing import *
from datetime import *
from Structs.OptionTypes import OptionType
from DataFetcher.DataAggregator.DataGranularity import *

DatePair = Tuple[datetime, datetime]

class IMarketDataAdapter( ABC ):

    @abstractmethod
    def get_price_futures(self, symbol:str, dates:DatePair, expiryDateTime:datetime):
        pass

    @abstractmethod
    def get_price_options(self, symbol:str, optionType:OptionType, strikePrice:int, dates:DatePair, expiryDateTime:datetime):
        pass

    @abstractmethod
    def get_price_scrip(self, symbol:str, dates:DatePair, granularity: DataGranularity):
        pass
