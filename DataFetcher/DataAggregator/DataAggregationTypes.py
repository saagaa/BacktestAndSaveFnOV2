import enum
from Utils.PRECOMP import *
from Utils.DateUtils import *

class DataAggregationType(enum.IntEnum):
    Empty = -100
    Symbol = 100
    SecurityType = 300
    ExpiryDate = 500
    OptionType = 600
    StrikePrice = 700
    Granularity = 800
    AggregationCell = 900

def GetAggregateOptions( dataAggregationType: DataAggregationType, var ) -> List:
    list=[var]
    if(DataAggregationType.ExpiryDate==dataAggregationType):
        list.append(convertToDate(var))
        list.append(convertToDateTime(var))
    return list