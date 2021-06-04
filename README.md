# Library for Backtesting strategies and saving queried data for future use

This library can do the following things for you
1. Query data from NSE/Yahoo
2. Save the data to a local DB
3. querying data is as simple as calling simple APIs
4. the DataModel is extensible to include all kind of data, ranging from various granularity, instrument type, etc.
5. Many inbuilt methods to calculate moving volatilities, mathematical manipulations
6. You can set the data that you want to cache by adjusting the params for lookAhead days , and lookBackDays

<h2>Integrating new online Database:</h2>
Integrating a databases like quandl/ nsepy/ yfinance is extremely simple you just need to create an adapter that  calls the other available databases and transform the response into the type "DataCell"
try to follow the examples: NSEpyMarketDataAdapter, YahooFinanceMarketDataAdapter.
These reside in DataFetcher\MarketDataAdapters

<h3>Aggregation of data: </h3>
The data is aggregated based on the following:
1. Symbol
2. SecurityType ( currently, stock, option, future, you can add more values here )
3. ExpiryData (if any)
4. OptionType (if)
5. StrikePrice (if)
6. Granularity (minute, hourly, daily, you can add more values in this enum )
To edit checkout "DataFetcher\DataAggregator\DataAggregateTypes.py"

<h3>Columns in each Table</h3>
Each cell you reach on the basis of the aggregation above will have a table which is a PANDAS DataFrame.
Currently it contains following values ( :
1. Date
2. Open
3. High
4. Low
5. Close
6. Volume
7. Turnover
8. AdjClose
9. Volatility
10. SettlePrice
11. Volume
12. OpenInterest
13. ChangeInOI
14. Underlying
15. Last
16. PremiumTurnover
To edit checkout "DataFetcher\DataAggregator\DataOptions.py"


