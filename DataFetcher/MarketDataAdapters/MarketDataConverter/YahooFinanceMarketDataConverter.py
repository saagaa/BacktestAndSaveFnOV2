from DataFetcher.CommonTypes import *
from DataFetcher.MarketDataAdapters.DataCleaner import  *

class YahooFinanceMarketDataConverter:
    def ConvertData(data: pd.DataFrame,
                    symbol: str,
                    granularity: DataGranularity,
                    index: bool = None,
                    future: bool = False,
                    option: bool = False,
                    optionType: OptionType = None,
                    expiry: datetime = None) -> DataStruct:

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
        AggregationTypes_map[DataAggregationType.Granularity] = granularity

        for row_i in range(0, len(data) ):
            data_cell_innerMap: Mapping[DataOptions, Any] = {}
            data_cell_innerMap[ DataOptions.Date ] = DataCleaner.CleanDateTime( data.index[row_i] )

            for column in data.columns:
                columnType = YahooFinanceMarketDataConverter.GetDataType(column)
                if (columnType != None):
                    data_cell_innerMap[columnType] = data[column][row_i]

            DataCell_map.append( data_cell_innerMap )

        return DataStruct( AggregationTypes_map, DataCell_map )

    @staticmethod
    def GetDataType(column_name: str):
        dataTypesMapping = {
            "CLOSE": DataOptions.Close,
            "HIGH": DataOptions.High,
            "LOW": DataOptions.Low,
            "OPEN": DataOptions.Open,
#            "VOLUME": DataOptions.Volume,
#            "TURNOVER": DataOptions.Turnover,
#            "SETTLE PRICE": DataOptions.SettlePrice,
#            "NUMBER OF CONTRACTS" : DataOptions.NumberOfContracts,
#            "OPEN INTEREST" : DataOptions.OpenInterest,
#            "CHANGE IN OI" : DataOptions.ChangeInOI,
#            "UNDERLYING" : DataOptions.Underlying,
#            "LAST" : DataOptions.Last
        }

        column_name = column_name.upper()
        if (column_name in dataTypesMapping.keys()):
            return dataTypesMapping[column_name]

        ignore_names = ["SYMBOL", "EXPIRY", "ADJ CLOSE", "VOLUME"]
        if(column_name in ignore_names):
            return
        print("YahooFinanceMArketDataConverter::GetDataType Unknown column name:" + str(column_name))
        return None
