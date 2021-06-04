
import pandas as pd
from DataFetcher.CommonTypes import *

class DataFrameUtils:
    
    @staticmethod
    def SearchDataFrame( df: pd.DataFrame, startTime: datetime,endTime: datetime ) -> pd.DataFrame:
        return df.iloc[df.index.searchsorted(startTime): df.index.searchsorted(endTime)]

    @staticmethod
    def DropDuplicates(df: pd.DataFrame) -> pd.DataFrame:
        return df[~df.index.duplicated(keep='first')]
        #return pd.concat([a, b]).drop_duplicates().reset_index(drop=True)
        # if ((a is not None and type(a) is not pd.core.frame.DataFrame) or (
        #         b is not None and type(b) is not pd.core.frame.DataFrame)):
        #     raise ValueError('a and b must be of type pandas.core.frame.DataFrame.')
        # if (a is None):
        #     return (b)
        # if (b is None):
        #     return (a)
        # if (col is not None):
        #     aind = a.iloc[:, col].values
        #     bind = b.iloc[:, col].values
        # else:
        #     aind = a.index.values
        #     bind = b.index.values
        # take_rows = list(set(bind) - set(aind))
        # take_rows = [i in take_rows for i in bind]
        # return (a.append(b.iloc[take_rows, :]))
    @staticmethod
    def ValidateDataFrame(df: pd.DataFrame) -> bool:
        zeroCells = 0
        totalCells = 0
        for val in df[DataOptions.Open]:
            if (val == 0):
                zeroCells += 1
            totalCells += 1

        for val in df[DataOptions.Close]:
            if (val == 0):
                zeroCells += 1
            totalCells += 1
        # if 20% cells are invalid then return false
        if (zeroCells / totalCells > 0.2):
            return False
        return True