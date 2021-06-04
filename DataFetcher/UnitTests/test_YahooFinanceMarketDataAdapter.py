from unittest import TestCase
from DataFetcher.CommonTypes import *
from DataFetcher.MarketDataAdapters.YahooFinanceMarketDataAdapter import *

class TestYahooFinanceMarketDataAdapter(TestCase):
    yahooFinanceAdapter = YahooFinanceMarketDataAdapter()
    def test_get_price_scrip(self):
        dates : DatePair = ( datetime(year=2020, month=9,day=20), datetime(year=2020, month=10,day=14) )
        value = self.yahooFinanceAdapter.get_price_scrip( symbol="NIFTY", dates = dates, granularity=DataGranularity.Minutely)
        print(value)

    def test_get_price_scrip_helper(self):

        self.fail()

    def test_granularity_string(self):

        self.fail()
