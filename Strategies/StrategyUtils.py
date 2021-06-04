import pandas as pd
import numpy as np
from DataFetcher.DataBase.DataBaseAggregator import *
from pandas.tseries.offsets import *

class StrategyUtils:

    @staticmethod
    def DoBollingerBands( df: pd.DataFrame, lookback: int, sigma: float, constTradingCost: float ):
        df['moving_average'] = df.spread.ewm(halflife=lookback).mean()  # df.spread.rolling(lookback).ewma()
        df['moving_std_dev'] = df.spread.ewm(halflife=lookback).std()  # df.spread.rolling(lookback).std()

        # df['moving_average'] = df.spread.rolling(lookback).mean()
        # df['moving_std_dev'] = df.spread.rolling(lookback).std()

        df['upper_band'] = df.moving_average + sigma * df.moving_std_dev + constTradingCost
        df['lower_band'] = df.moving_average - sigma * df.moving_std_dev - constTradingCost

        df['long_entry'] = df.spread < df.lower_band
        df['long_exit'] = df.spread >= df.moving_average
        df['positions_long'] = np.nan
        df.loc[df.long_entry, 'positions_long'] = 1
        df.loc[df.long_exit, 'positions_long'] = 0
        df.positions_long = df.positions_long.fillna(method='ffill')

        df['short_entry'] = df.spread > df.upper_band
        df['short_exit'] = df.spread <= df.moving_average
        df['positions_short'] = np.nan
        df.loc[df.short_entry, 'positions_short'] = -1
        df.loc[df.short_exit, 'positions_short'] = 0
        df.positions_short = df.positions_short.fillna(method='ffill')

        df['positions'] = df.positions_long + df.positions_short
        # df.positions.loc[vix.Close<12] = 0
        df['spread_difference'] = df.spread - df.spread.shift(1)
        df['trade'] = ( (df.positions.shift(1) - df.positions ) != 0).astype(int)
        df['pnl'] = df.positions.shift(1) * df.spread_difference - (df.trade*constTradingCost)
        # df['costToTrade']=cost
        df['cumpnl'] = df.pnl.cumsum()
        df.drop(['upper_band','lower_band','long_entry','long_exit','short_entry','short_exit','positions_long','positions_short'], axis = 1)


    @staticmethod
    def FetchTodaysVolatility(stock:str, DB: DataBaseAggregator, date: datetime, days=7):
        datePair :DatePair = (date-BDay(days), date)
        data = DB.get_index_prices(stock, datePair, DataGranularity.Daily)
        return data.std()