from DataFetcher.DataAggregator.DataStruct import *
from DataFetcher.DataAggregator.DataGranularity import *
from DataFetcher.DataAggregator.DataSecurityType import *
import pandas as pd
from datetime import *
from Structs.OptionTypes import *
from DataFetcher.MarketDataAdapters.DataCleaner import *

class NSEpyMarketDataConverter:

    @staticmethod
    def ConvertData(nse_data: pd.DataFrame,
                    symbol: str,
                    index: bool = None,
                    future: bool = False,
                    option: bool = False,
                    optionType: OptionType = None,
                    expiry: datetime = None,
                    strikePrice: int = None) -> DataStruct:

        AggregationTypes_map: Mapping[DataAggregationType, Any] = {}
        DataCell_map: List[Mapping[DataOptions, Any]] = []

        AggregationTypes_map[DataAggregationType.Symbol] = symbol

        dataSecurityType = DataSecurityType.IsStock
        if (future != None and future == True):
            dataSecurityType = DataSecurityType.IsFuture
        if (option != None and option == True):
            dataSecurityType = DataSecurityType.IsOption
        AggregationTypes_map[DataAggregationType.SecurityType] = dataSecurityType
        if ( expiry != None ):
            AggregationTypes_map[DataAggregationType.ExpiryDate] = expiry
        if ( optionType != None ):
            AggregationTypes_map[DataAggregationType.OptionType] = optionType
        AggregationTypes_map[DataAggregationType.Granularity] = DataGranularity.Daily

        if( strikePrice != None ):
            AggregationTypes_map[DataAggregationType.StrikePrice] = strikePrice

        for row_i in range(0, len(nse_data) ):
            data_cell_innerMap: Mapping[DataOptions, Any] = {}
            data_cell_innerMap[ DataOptions.Date ] = DataCleaner.CleanDateTime( datetime.combine( nse_data.index[row_i], datetime.min.time()) )

            for column in nse_data.columns:
                columnType = NSEpyMarketDataConverter.GetDataType(column)
                if (columnType != None):
                    data_cell_innerMap[columnType] = nse_data[column][row_i]

            DataCell_map.append( data_cell_innerMap )

        return DataStruct( AggregationTypes_map, DataCell_map )

    @staticmethod
    def GetDataType(column_name: str):
        dataTypesMapping = {
            "CLOSE": DataOptions.Close,
            "HIGH": DataOptions.High,
            "LOW": DataOptions.Low,
            "OPEN": DataOptions.Open,
            "VOLUME": DataOptions.Volume,
            "TURNOVER": DataOptions.Turnover,
            "SETTLE PRICE": DataOptions.SettlePrice,
            "NUMBER OF CONTRACTS" : DataOptions.NumberOfContracts,
            "OPEN INTEREST" : DataOptions.OpenInterest,
            "CHANGE IN OI" : DataOptions.ChangeInOI,
            "UNDERLYING" : DataOptions.Underlying,
            "LAST" : DataOptions.Last,
            "PREMIUM TURNOVER": DataOptions.PremiumTurnover
        }

        column_name = column_name.upper()
        if (column_name in dataTypesMapping.keys()):
            return dataTypesMapping[column_name]

        ignore_names = ["SYMBOL", "EXPIRY", "OPTION TYPE", "STRIKE PRICE"]
        if(column_name in ignore_names):
            return
        print("NSEpyMarketDataConverter::GetDataType Unknown column name:" + str(column_name))
        return None
