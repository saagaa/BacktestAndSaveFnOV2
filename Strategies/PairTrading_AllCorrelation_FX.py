import multiprocessing
from typing import Mapping
from typing import Any
from typing import List

from joblib import Parallel, delayed

from DataFetcher.CommonTypes import *
from DataFetcher.DataBase.DataBaseAggregator import *
from statsmodels.api import OLS
from Utils.AllUtils import *
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm
import numpy as np
from Strategies.StrategyUtils import *
import pyfolio as pf
import traceback
from pandas.tseries.offsets import BDay
from Strategies.StrategyMetrics import *

class PairTrading_AllCorrelations_FX:

    def __init__(self, stocks: List[str], startDate:datetime, endDate:datetime, DB: DataBaseAggregator):
        self.stocks = stocks
        self.startDate = startDate
        self.endDate = endDate
        self.DB = DB
        self.TradingCostPErcentage = 0.001#0.005 # 0.1%
        self.ADFPassValue = -3.5
        self.MinSharpe = 1
        self.MinCalamar = 1
        self.ChoosingMetric = 'Annual volatility'
        self.Leverage = 0.5
        self.StandardDeviations = 1
        self.ShouldTrainWithoutCost = False
        self.SpreadDeviationRatio  =1/10
        self.ShouldDownloadData = False

    def CacheWarmUp(self):
        i=0
        dfs = []
        for stock in self.stocks:
            val = self.DB.get_index_prices(stock, ( self.startDate, self.endDate ), DataGranularity.Minutely, shouldDownloadData=self.ShouldDownloadData)
            print( str(i) + " of " + str(len(self.stocks)) + "downloaded")
            i=i+1
            dfs.append(val)

        print("Cache Warmed Up")

        d2 = []
        for d in dfs:
            d = d.loc[~d.index.duplicated(keep='first')]
            d2.append(d[DataOptions.Close])

        df = pd.concat(d2, axis=1)
        df.columns = self.stocks
        self.Data = DataFrameUtils.DropDuplicates(df)
        return

    def runStrategy(self):
        durations = self.CalcTrainTestDurations()

        num_cores = multiprocessing.cpu_count()
        results = Parallel(n_jobs=num_cores)(delayed(self.runStrategyEachDay)(self.Data, duration[0], duration[1], duration[2]) for duration in durations )
        self.Data['Return'] = 0
        self.Data['Count'] = 0
        for result in results:
            self.Data['Return'] += result['Return']
            self.Data['Count'] += result['Count']
        return self.Data

    def runStrategyEachDay(self, data:pd.DataFrame, startDateTime: datetime, endTrainDateTime:datetime, endDateTime: datetime):
        data['Return'] = 0
        data['Count'] = 0

        pair_list = {}
        for stock2 in self.stocks:
            for stock1 in self.stocks:
                if stock1 == stock2:
                    continue
                val = self.StrategiseOnStock(self.Data, stock1, stock2,startDateTime,endTrainDateTime, endDateTime)

                if(val[0] == 1):
                    df_dash = val[1]
                    adf_stat = val[2]
                    metrics = val[3]
                    #sharpe = metrics['Sharpe ratio']
                    #calamar = metrics['Calmar ratio']
                    # annual = metrics['Annual return']
                    # kurtosis = metrics['Kurtosis']
                    # volatility = metrics['Annual volatility']
                    #choiceMetric = metrics[self.ChoosingMetric]
                    #if( sharpe > 1 and calamar > 1):
                    #    pair_list[choiceMetric] = ( stock1, stock2, df_dash)

                    if(self.ShouldTrainWithoutCost):
                        stratMetrics = StrategyMetrics.CalculateStrategyMetrics(df_dash['NoCostReturn'][:endTrainDateTime])

                    else:
                        stratMetrics = StrategyMetrics.CalculateStrategyMetrics(df_dash['return'][:endTrainDateTime])

                    calamar = stratMetrics['Calamar Ratio']
                    sharpe = stratMetrics['Sharpe Ratio']
                    volatility = stratMetrics['Volatility']
                    if(calamar >=1 ):
                        pair_list[volatility] = (stock1,stock2,df_dash)

        #choose top 5 pairs
        for key in sorted(pair_list.keys())[-5:]:
            df_dash = pair_list[key][2].fillna(0)
            data['Return'][endTrainDateTime:endDateTime]+= df_dash['return'][endTrainDateTime:endDateTime]
            data['Count'][endTrainDateTime:endDateTime] += 1
        print("ran complete on duration:" + str(startDateTime))
        return data

    def CalcTrainTestDurations(self):
        starting = datetime(2020, 9, 20, hour=10, minute= 30)
        ending = datetime(2020, 10, 16, hour=15, minute=30)
        durations = []
        while True:
            if( starting.weekday()<5):
                end =  starting + timedelta(hours=+4, minutes=+20) #timedelta(days=+2, hours=+5, minutes = +20)
                train_end = starting + timedelta(hours=+1, minutes=+30)   #timedelta(days=+1, hours=+5, minutes = +20)
                if (end >= ending):
                    #    durations.append((start,train_end,yr2020))
                    break
                durations.append((starting, train_end, end))
            starting = starting + timedelta(days=+1)
        return durations

    def StrategiseOnStock(self, dataDF, stock1, stock2, startDateTime: datetime, endTrainDateTime:datetime, endDateTime: datetime)\
            ->Tuple[int,pd.DataFrame, int,Mapping[str,int]]:

        myDF:pd.DataFrame = dataDF[[stock1,stock2]][startDateTime:endDateTime]
        myDF = myDF.replace([np.inf, -np.inf], np.nan)
        myDF = myDF.dropna()
        if(len(myDF) <5):
            return (0, 0, 0, 0)


        adf = [5]
        try:
            model = OLS(DataFrameUtils.SearchDataFrame(myDF[stock1], startDateTime, endTrainDateTime),
                        DataFrameUtils.SearchDataFrame(myDF[stock2], startDateTime, endTrainDateTime))
            ## optimisation: model.AddConstant can be done

            model = model.fit()
            beta = model.params[0]
            myDF['Spread'] = myDF[stock1] - beta * myDF[stock2]
            myDF['spread'] = myDF['Spread']
            adf = adfuller(myDF.Spread[:endTrainDateTime], maxlag=1)
        except Exception as e:
            traceback.print_exc()
            print("skipping " + str(stock1) + ", "+ str(stock2) + " || " + str(startDateTime) +",," + str(endDateTime)  +"dueToException " + str(e) )
            adf[0] = 5

        if adf[0] <= self.ADFPassValue and beta is not None:
            halflife = self.GetHalfLife(myDF.Spread[:endTrainDateTime])
            myDF['cost'] = self.Leverage* myDF[stock1] + beta * myDF[stock2]

            if self.ShouldTrainWithoutCost:
                StrategyUtils.DoBollingerBands(myDF, halflife, self.StandardDeviations, 0)
                myDF['NoCostReturn'] = (myDF.pnl / myDF.cost)

            StrategyUtils.DoBollingerBands(myDF, halflife, self.StandardDeviations, myDF['cost'][0]*self.TradingCostPErcentage)
            myDF['return'] = (myDF.pnl / myDF.cost)
            #metrics = pf.timeseries.perf_stats(myDF['return'][:endTrainDateTime].dropna())

            metrics = myDF.Spread[:endTrainDateTime].std() / myDF['cost'][0]
            trades = myDF.trade[:endTrainDateTime].dropna().sum()
            if( metrics > self.SpreadDeviationRatio ):
                return (1, myDF, adf[0],metrics)

        return (0, 0, adf[0], 0)

    def GetHalfLife(self, series):
        z_lag = np.roll(series, 1)
        z_lag[0] = 0
        z_ret = series - z_lag
        z_ret[0] = 0
        # adds intercept terms to X variable for regression
        z_lag2 = sm.add_constant(z_lag)
        model2 = sm.OLS(z_ret, z_lag2)
        res2 = model2.fit()
        halflife = -np.log(2) / res2.params[1]
        return int(halflife) + 1
