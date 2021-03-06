# Library for Backtesting strategies and saving queried data for future use

The purpose of this Library is to make simple APIs that can query the data from internet and save it in DB. The API will automatically pull data from the DB if it has been pulled before. <br>
This library can do the following things for you
1. Query data from NSE/Yahoo and easy to add new data sources
2. Save the data to a local DB
3. Querying data is as simple as calling simple APIs
4. the DataModel is extensible to include all kind of data, ranging from various granularity, instrument type, etc.
5. Many inbuilt methods to calculate moving volatilities, mathematical manipulations
6. You can set the data that you want to cache by adjusting the params for lookAhead days , and lookBackDays

## Table of Contents 
1. [Strategies](#strategies) <br>
2. [How to integrate new online Databases](#integrating-new-online-database)<br>
3. [Aggregation of data](#aggregation-of-data) <br>
4. [Columns in each Table ( pandas dataframe )](#columns-in-each-table-pandas-dataframe) <br>

<hr>

### Strategies:
The folder Strategies has the following pre-made strategies: <br>
1. Dividend Capture : `DividendCaptureFutureStock.py` <br>
2. Buying IronButterfly for a particular probability of winning : `BuyIronButterfly.py` <br>
3. Buy Overnight Calls : `OvernightCall.py` <br>
4. Pair Trade most stationary looking stock pairs: `PairTrading_AllCorrelations.py` <br>
5. Pair Trade most stationary looking FX pairs: `PairTrading_AllCorrelations_FX.py` <br>
6. Buy Straddles : `Straddle.py` <br>

### Integrating new online Database:
Integrating a databases like quandl/ nsepy/ yfinance is extremely simple you just need to create an adapter that  calls the other available databases and transform the response into the type "DataCell"
try to follow the examples: NSEpyMarketDataAdapter, YahooFinanceMarketDataAdapter.
These reside in `DataFetcher\MarketDataAdapters`

### Aggregation of data:
The data is aggregated based on the following:<br>
1. Symbol <br>
2. SecurityType ( currently, stock, option, future, you can add more values here ) <br>
3. ExpiryData (if any)<br>
4. OptionType (if)<br>
5. StrikePrice (if)<br>
6. Granularity (minute, hourly, daily, you can add more values in this enum )<br>

To edit checkout `DataFetcher\DataAggregator\DataAggregateTypes.py`

### Columns in each Table (pandas DataFrame):
Each cell you reach on the basis of the aggregation above will have a table which is a PANDAS DataFrame.
Currently it contains following values: <br>
1. Date<br>
2. Open<br>
3. High<br>
4. Low<br>
5. Close<br>
6. Volume<br>
7. Turnover<br>
8. AdjClose<br>
9. Volatility<br>
10. SettlePrice<br>
11. Volume<br>
12. OpenInterest<br>
13. ChangeInOI<br>
14. Underlying<br>
15. Last<br>
16. PremiumTurnover<br>

To edit checkout `DataFetcher\DataAggregator\DataOptions.py`


