from abc import ABC, abstractmethod


class IDataFetch( ABC ):

    @abstractmethod
    def Initialize(self):
        pass

    @abstractmethod
    def OnCompleteSave(self):
        pass

    @abstractmethod
    def get_expiry( self, year, month):
        pass

    @abstractmethod
    def get_index_price_futures(self, symbol, date, expiryDateTime, granularity):
        pass

    @abstractmethod
    def get_index_price_options(self, symbol, optionType, strikePrice, date, expiryDateTime, granularity):
        pass

    @abstractmethod
    def get_index_prices(self, symbol, date, granularity):
        pass
