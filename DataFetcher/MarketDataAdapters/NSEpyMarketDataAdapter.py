from DataFetcher.MarketDataAdapters.IMarketDataAdapter import *
from nsepy import get_history
from Structs.OptionTypes import OptionType
from Utils.ScripUtils import *
from DataFetcher.MarketDataAdapters.MarketDataConverter.NSEpyMarketDataConverter import *
from DataFetcher.MarketDataAdapters.MarketDataScripMap.YahooFinanceScripMap import *
from Utils.DateUtils import *
import traceback

class NSEpyMarketDataAdapter(IMarketDataAdapter):

    def get_price_futures(self, symbol: str, dates: DatePair, expiryDateTime: datetime):
        try:
            dates = self.SanitizeDates(dates)
            expiryDateTime = self.SanitizeDate(expiryDateTime)
            value = get_history(symbol, dates[0], dates[1], index=IsIndex(symbol), futures=True,
                                expiry_date=expiryDateTime)
            return NSEpyMarketDataConverter.ConvertData(value, symbol=symbol, future=True, expiry=expiryDateTime)

        except Exception as e:
            traceback.print_exc()
            print("NSEpyMarketDataAdapter::get_price_futures" + str(e))
            return None

    def get_price_options(self, symbol: str, optionType: OptionType, strikePrice: int, dates: DatePair,
                          expiryDateTime: datetime):
        try:
            expiryDateTime = self.SanitizeDate(expiryDateTime)
            dates = self.SanitizeDates(dates)
            value = get_history(symbol, dates[0], dates[1], index=IsIndex(symbol), option_type=optionType.ToString(),
                                strike_price=strikePrice,
                                expiry_date=expiryDateTime)
            return NSEpyMarketDataConverter.ConvertData(value, symbol=symbol, option=True, expiry=expiryDateTime,
                                                        optionType=optionType, strikePrice=strikePrice)

        except Exception as e:
            print("NSEpyMarketDataAdapter::get_price_options" + str(e))
            return None

    def get_price_scrip(self, symbol: str, dates: DatePair, granularity: DataGranularity):
        try:
            dates = self.SanitizeDates(dates)
            value = get_history(symbol, dates[0], dates[1], index=IsIndex(symbol) )
            return NSEpyMarketDataConverter.ConvertData(value, symbol=symbol, index=True)

        except Exception as e:
            print("NSEpyMarketDataAdapter::get_price_scrip" + str(e))
            value = 0
            return None

    def SanitizeDate(self, mydate: datetime):
        #if isinstance(mydate, date):
        #    return datetime.combine( mydate, datetime.min.time() )

        # if isinstance(mydate, datetime):
        #     return mydate.date()
        return convertToDateTime(mydate)

    def SanitizeDates(self, dates: DatePair):
        return (convertToDate(dates[0]), convertToDate(dates[1]))
        # date0 = dates[0]
        # date1 = dates[1]
        #
        # if isinstance(date0, datetime):
        #     date0 = date0.date()
        # if isinstance(date1, datetime):
        #     date1 = date1.date()
        # return (date0,date1)