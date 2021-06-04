
from typing import *
from DataFetcher.DataAggregator.DataOptions import *
from DataFetcher.DataAggregator.DataAggregationTypes import *

class DataStruct:
    AggregationTypes_map: Mapping[DataAggregationType, Any]
    DataCell_map: List[Mapping[DataOptions, Any] ]

    def __init__(self,aggregationTypes_map: Mapping[DataAggregationType, Any], DataCell_map: List[Mapping[DataOptions, Any] ] ):
        self.AggregationTypes_map = aggregationTypes_map
        self.DataCell_map = DataCell_map