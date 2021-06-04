from DataFetcher.MarketDataAdapters.MarketDataConverter.YahooFinanceMarketDataConverter import *
from DataFetcher.MarketDataAdapters.MarketDataScripMap.YahooFinanceScripMap import *
from datetime import timedelta
import yfinance as yf

class YahooFinanceMarketDataAdapter(IMarketDataAdapter):

    def get_price_futures(self, symbol: str, dates: DatePair, expiryDateTime: datetime):
        raise("yahoo finance doesnt give API for fetching futures")

    def get_price_options(self, symbol: str, optionType: OptionType, strikePrice: int, dates: DatePair,
                          expiryDateTime: datetime):
        raise("yahoo finance doesnt give API for fetching options")

    def get_price_scrip(self, symbol: str, dates: DatePair, granularity: DataGranularity):
        try:
            df = None
            df_populated = False
            startDate = dates[0]
            while(dates[1]> startDate+ timedelta(days=+6)):
                nextDate =  startDate+ timedelta(days=+6)
                df2 = self.get_price_scrip_helper(symbol, (startDate,nextDate), granularity)
                if(df_populated == False):
                    df = df2
                    df_populated = True
                else:
                    df = df.append(df2)
                startDate = nextDate

            df2 = self.get_price_scrip_helper(symbol, (startDate, dates[1]), granularity)
            if (df_populated==False):
                df = df2
                df_populated = True
            else:
                df = df.append(df2)

            return YahooFinanceMarketDataConverter.ConvertData(df, symbol=symbol, index=True, granularity= granularity)

        except Exception as e:
            print("YahooFinanceMarketDataAdapter::get_price_scrip" + str(e))
            value = 0
            return None

    def get_price_scrip_helper(self, symbol: str, dates: DatePair, granularity: DataGranularity):
        df = yf.download( YahooFinanceScripMap.GetScripName(symbol), dates[0], dates[1], interval=self.GranularityString(granularity), threads=1)
        return df


    def GranularityString(self, granularity: DataGranularity):
        switcher = {
            DataGranularity.Minutely: '1m',
            DataGranularity.Hourly: '1h',
            DataGranularity.Daily: '1d'
        }
        return switcher.get(granularity, None)