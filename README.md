# Library for Backtesting strategies and saving queried data for future use

This library can do the following things for you
1. Query data from NSE/Yahoo
2. Save the data to a local DB
3. querying data is as simple as calling simple APIs
4. the DataModel is extensible to include all kind of data, ranging from various granularity, instrument type, etc.
5. Many inbuilt methods to calculate moving volatilities, mathematical manipulations
6. You can set the data that you want to cache by adjusting the params for lookAhead days , and lookBackDays

<h2> Table of Contents </h2>
1. Strategies <br>
2. How to integrate new online Databases <br>
3. Aggregation of data <br>
4. Columns in each Table ( panda's dataframe ) <br>

<hr>

<h3>Strategies: </h3>
The folder Strategies has the following pre-made strategies: <br>
1. Dividend Capture : `DividendCaptureFutureStock.py` <br>
2. Buying IronButterfly for a particular probability of winning : `BuyIronButterfly.py` <br>
3. Buy Overnight Calls : `OvernightCall.py` <br>
4. Pair Trade most stationary looking stock pairs: `PairTrading_AllCorrelations.py` <br>
5. Pair Trade most stationary looking FX pairs: `PairTrading_AllCorrelations_FX.py` <br>
6. Buy Straddles : `Straddle.py` <br>

<h3>Integrating new online Database:</h3>
Integrating a databases like quandl/ nsepy/ yfinance is extremely simple you just need to create an adapter that  calls the other available databases and transform the response into the type "DataCell"
try to follow the examples: NSEpyMarketDataAdapter, YahooFinanceMarketDataAdapter.
These reside in DataFetcher\MarketDataAdapters

<h3>Aggregation of data: </h3>
The data is aggregated based on the following:<br>
1. Symbol <br>
2. SecurityType ( currently, stock, option, future, you can add more values here ) <br>
3. ExpiryData (if any)<br>
4. OptionType (if)<br>
5. StrikePrice (if)<br>
6. Granularity (minute, hourly, daily, you can add more values in this enum )<br>

To edit checkout "DataFetcher\DataAggregator\DataAggregateTypes.py"

<h3>Columns in each Table</h3>
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

To edit checkout "DataFetcher\DataAggregator\DataOptions.py"


