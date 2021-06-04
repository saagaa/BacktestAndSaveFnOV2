
import pandas as pd
from typing import Mapping

class StrategyMetrics:

    @staticmethod
    def CalculateStrategyMetrics(df_dailyReturn: pd.Series ) -> Mapping[str, int]:
        Metrics = {}
        returns = (df_dailyReturn+1).cumprod()
        Metrics['Calamar Ratio'] = StrategyMetrics.ComputeCalamarRatio(returns)
        std = returns.std()
        Metrics['Volatility'] = std
        if( std != 0):
            Metrics['Sharpe Ratio'] = returns[-1]/std
        else:
            Metrics['Sharpe Ratio'] = -1
        return Metrics

    @staticmethod
    def ComputeCalamarRatio(returns: pd.Series) -> float:
        mx = returns.cummax()
        mn = returns[::-1].cummin()[::-1]
        # diff = mx - mn
        # index = (mx - mn).argmax()
        # return mx[index], mn[index],
        maxDrawdown = (mx - mn).max()
        if maxDrawdown != 0:
            return returns[-1] / maxDrawdown
        else:
            return -999999999999

    @staticmethod
    def ComputeSharpe(df_dailyReturn: pd.Series) -> float:
        returns: pd.Series = (df_dailyReturn + 1).cumprod()
        std = returns.std()
        if (std != 0):
            return (returns) / std
        return -99999999999

    @staticmethod
    def ComputeVolatility(df_dailyReturn: pd.Series) -> float:
        returns: pd.Series = (df_dailyReturn + 1).cumprod()