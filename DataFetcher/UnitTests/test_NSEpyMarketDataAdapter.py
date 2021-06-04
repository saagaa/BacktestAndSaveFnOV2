from unittest import TestCase
from DataFetcher.MarketDataAdapters.NSEpyMarketDataAdapter import *
from Utils.Expiries import *
from Utils.PRECOMP import *

class TestNSEpyMarketDataAdapter(TestCase):

    nsepyMarketAdapter = NSEpyMarketDataAdapter()
    def test_get_price_futures(self):
        dates : DatePair = ( datetime(year=2015, month=8,day=1), datetime(year=2015, month=10,day=1) )
        value = self.nsepyMarketAdapter.get_price_futures("NIFTY", dates, get_month_expiry(year=2015, month=10) )

    def test_get_price_options(self):
        dates : DatePair = ( datetime(year=2015, month=8,day=1), datetime(year=2015, month=10,day=1) )
        index = self.nsepyMarketAdapter.get_price_scrip("NIFTY", dates, DataGranularity.Daily)
        price = index.DataCell_map[0][DataOptions.Close]
        value = self.nsepyMarketAdapter.get_price_options("NIFTY", OptionType.Call, price-price%100, dates, get_month_expiry(year=2015, month=10) )

    def test_get_price_scrip(self):
        dates : DatePair = ( datetime(year=2015, month=8,day=1), datetime(year=2015, month=10,day=1) )
        value = self.nsepyMarketAdapter.get_price_scrip("NIFTY", dates, DataGranularity.Daily )
