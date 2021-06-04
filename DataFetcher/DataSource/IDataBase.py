from abc import ABC, abstractmethod


class IDataBase( ABC ):

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
    def get_index_price_futures(self, symbol, date, expiryDateTime, index):
        pass

    @abstractmethod
    def get_index_price_options(self, symbol, optionType, strikePrice, date, expiryDateTime, index):
        pass

    @abstractmethod
    def get_index_prices(self, symbol, date, index):
        pass
