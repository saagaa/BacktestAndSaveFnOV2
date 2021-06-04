from unittest import TestCase
from DataFetcher.DataBase.DataBaseAggregator import *
from Utils.Expiries import *
from Utils.PRECOMP import *

class TestDataBaseAggregator(TestCase):
    DB = DataBaseAggregator()

    def test_populate_market_data_adapters(self):
        self.fail()

    def test_initialise(self):
        self.fail()

    def test_on_complete_save(self):
        dates : DatePair = ( datetime(year=2015, month=8,day=1), datetime(year=2015, month=10,day=1) )
        val = self.DB.get_index_price_futures("NIFTY", dates, get_month_expiry(year=2015, month=10) , DataGranularity.Daily)
        self.DB.OnCompleteSave()

    def test_get_expiry(self):
        self.fail()

    def test_get_index_price_futures(self):
        dates : DatePair = ( datetime(year=2015, month=8,day=1), datetime(year=2015, month=10,day=1) )
        val = self.DB.get_index_price_futures("NIFTY", dates, get_month_expiry(year=2015, month=10) , DataGranularity.Daily)
        print(str(val))

    def test_get_index_price_options(self):
        self.fail()

    def test_get_index_prices(self):
        dates : DatePair = ( datetime(year=2020, month=9,day=20), datetime(year=2020, month=10,day=14) )
        val  = self.DB.get_index_prices("NIFTY", dates, DataGranularity.Daily);
        print(val)

        val  = self.DB.get_index_prices("BAJAJ-AUTO.NS", dates, DataGranularity.Minutely);
        print("got prices")
        val  = self.DB.get_index_prices("NIFTY", dates, DataGranularity.Minutely);
        print("got prices")
        val  = self.DB.get_index_prices("BAJAJ-AUTO.NS", dates, DataGranularity.Minutely);
        print("got prices")
        val  = self.DB.get_index_prices("NIFTY", dates, DataGranularity.Minutely);
        print("got prices")
        print(val)


    def test_duplicate_old_data_files(self):
        self.DB.DuplicateOldDataFilesInternal()
