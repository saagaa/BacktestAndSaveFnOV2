from unittest import TestCase
from DataFetcher.MarketDataAdapters.NSEpyMarketDataAdapter import *
from Utils.Expiries import *
from DataFetcher.DataAggregator.DataAggregate import *
from DataFetcher.DataAggregator.DataSecurityType import *
from DataFetcher.MarketDataAdapters.YahooFinanceMarketDataAdapter import *

class TestDataAggregate(TestCase):
    nsepyMarketAdapter = NSEpyMarketDataAdapter()
    yahoo = YahooFinanceMarketDataAdapter()
    def test_get_value(self):
        dates: DatePair = (datetime(year=2015, month=8, day=1), datetime(year=2015, month=10, day=1))
        value = self.nsepyMarketAdapter.get_price_futures("NIFTY", dates, get_month_expiry(year=2015, month=10))
        dataAggregator = DataAggregate(DataAggregationType.Empty)
        dataAggregator.ForceSetValue(value)
        value = self.nsepyMarketAdapter.get_price_options("NIFTY", OptionType.Call, 8000, dates,
                                                          get_month_expiry(year=2015, month=10))
        dataAggregator.ForceSetValue(value)

        dataAggregations = {DataAggregationType.Symbol: "NIFTY",
                            DataAggregationType.SecurityType: DataSecurityType.IsFuture,
                            DataAggregationType.Granularity: DataGranularity.Daily,
                            DataAggregationType.ExpiryDate: get_month_expiry(year=2015, month=10)}

        print(dataAggregator.GetValue(dataAggregations))

    def test_set_value(self):
        return

    def test_force_set_value(self):
        dates: DatePair = (datetime(year=2015, month=8, day=1), datetime(year=2015, month=10, day=1))
        value = self.nsepyMarketAdapter.get_price_futures("NIFTY", dates, get_month_expiry(year=2015, month=10))
        dataAggregator = DataAggregate(DataAggregationType.Empty)
        dataAggregator.ForceSetValue(value)
        value = self.nsepyMarketAdapter.get_price_options("NIFTY", OptionType.Call, 8000, dates,
                                                          get_month_expiry(year=2015, month=10))
        dataAggregator.ForceSetValue(value)
        # value = self.nsepyMarketAdapter.get_price_scrip("NIFTY", dates )
        # dataAggregator.ForceSetValue(value)
        print(str(dataAggregator))

    def test_populate_data_frame(self):
        dates: DatePair = (datetime(year=2015, month=8, day=1), datetime(year=2015, month=10, day=1))
        value = self.nsepyMarketAdapter.get_price_futures("NIFTY", dates, get_month_expiry(year=2015, month=10))
        dataAggregator = DataAggregate(DataAggregationType.Empty)
        dataAggregator.PopulateDataFrame(value.DataCell_map)


    def test_get_data_options(self):
        dates: DatePair = (datetime(year=2015, month=8, day=1), datetime(year=2015, month=10, day=1))
        value = self.nsepyMarketAdapter.get_price_futures("NIFTY", dates, get_month_expiry(year=2015, month=10))
        dataAggregator = DataAggregate(DataAggregationType.Empty)
        print(dataAggregator.GetDataOptions(value.DataCell_map))

        dates : DatePair = ( datetime(year=2020, month=9,day=20), datetime(year=2020, month=10,day=14) )
        value = self.yahoo.get_price_scrip( symbol="NIFTY", dates = dates, granularity=DataGranularity.Minutely)
        print(dataAggregator.GetDataOptions(value.DataCell_map))

