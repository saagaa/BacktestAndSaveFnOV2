from DataFetcher.DataAggregator.DataOptions import DataOptions
from DataFetcher.DataAggregator.DataAggregationTypes import DataAggregationType
from DataFetcher.DataAggregator.DataStruct import DataStruct
from DataFetcher.DataAggregator.DataCell import *
from Utils.AllUtils import *
from  Utils.PRECOMP import *
import pandas as pd

class DataAggregate:



    ### first n nodes
    #AggregationType = DataAggregationType.Empty
    #AggregationValueMap : Mapping[Any, 'DataAggregate'] = {}# recursive
                                                            # mapping of aggregationValue and InnerAggregation
    #AggregationValue = None
    #InnerAggregation = None

    ### last node
    #CellDataFrame = None

    def __init__(self, AggregationType:DataAggregationType):
        self.AggregationType:DataAggregationType = AggregationType
        self.AggregationValueMap:Mapping[Any, 'DataAggregate'] ={} # recursive mapping of aggreagtionValue and InnerAggregation
        self.CellDataFrame: pd.DataFrame = None  # lastNode
        self.CellDataFrameExists: bool = False

    def GetValue(self, dataAggregations: Mapping[DataAggregationType, Any]) -> pd.DataFrame:
        if( self.AggregationType > max(dataAggregations.keys())):
            if( self.CellDataFrameExists == True ):
                return self.CellDataFrame

        if( self.AggregationType in dataAggregations.keys() ):
            currAggregateValue = dataAggregations[self.AggregationType]
            currAggregationList: List = GetAggregateOptions( self.AggregationType, currAggregateValue )

            for aggregateValue in currAggregationList:
                if( aggregateValue in self.AggregationValueMap.keys() ):
                    return self.AggregationValueMap[currAggregateValue].GetValue(dataAggregations)
            else:
                raise Exception( "can't find the value " + str(dataAggregations[self.AggregationType]) +  " in the aggregation value map: " + str(self.AggregationValueMap) )
        else:
            if(self.AggregationType == DataAggregationType.AggregationCell ):
                return self.CellDataFrame
            else:
                raise Exception( "cannot query data from the dataAggregates for the data Aggregation mapping: " + str(dataAggregations) )


    def SetValue(self):
        pass

    ## summary: recursively sets the inner cell and in the last step sets the data frame
    def ForceSetValue(self, dataValue:DataStruct):

        if dataValue is None:
            a =0
            return
        # time to create a DataCell if the aggregation is the last level of aggregation
        if( self.AggregationType >  max( dataValue.AggregationTypes_map.keys() ) ):
            self.PopulateDataFrame( dataValue.DataCell_map )
            return

        if( self.AggregationType == DataAggregationType.Empty ):
            self.AggregationType = min( dataValue.AggregationTypes_map.keys() )

        #else populate the aggregation value and create another aggregation
        aggregationValueToAdd = dataValue.AggregationTypes_map[ self.AggregationType ];

        if( aggregationValueToAdd not in self.AggregationValueMap.keys() ):
            self.AggregationValueMap[ aggregationValueToAdd ] = DataAggregate(DataAggregationType.Empty)


        # search whats the next level of data aggregation to create
        aggregationTypeToCreate = DataAggregationType.AggregationCell
        for aggregationTypes_i in DataAggregationType:
            if( aggregationTypes_i > self.AggregationType and aggregationTypes_i in dataValue.AggregationTypes_map.keys() ):
                aggregationTypeToCreate = aggregationTypes_i
                break

        # if search completed successfully then aggregationTypeToCreate no more holds the value "DataAggregationType.Empty"
        if( aggregationTypeToCreate != DataAggregationType.Empty ):
            ## if the inner aggregation is None create a new data aggregate
            if( self.AggregationValueMap[ aggregationValueToAdd ] == None ):
                self.AggregationValueMap[ aggregationValueToAdd ] = DataAggregate( aggregationTypeToCreate )
            elif( self.AggregationValueMap[ aggregationValueToAdd ].AggregationType == DataAggregationType.Empty ):
                self.AggregationValueMap[ aggregationValueToAdd ].AggregationType = aggregationTypeToCreate
            # as the inner aggregation has already been created just pass on the values to it
            self.AggregationValueMap[ aggregationValueToAdd ].ForceSetValue( dataValue )
            return

        else:
            raise( "cannot find the next DataAggregate obj to create curr DataAggregate:" + str( self.ToString() ) + " ,aggregationTypes_map: "+ str( dataValue.AggregationTypes_map )  + " ,DataCell_mapping" + str(dataValue.DataCell_map))

        return

    ## internal method ##
    ##summary : Dataframe setter
    def PopulateDataFrame(self, DataCell_map: List[Mapping[DataOptions, Any]]):

        column_list = self.GetDataOptions(DataCell_map)
        if (self.CellDataFrameExists == False):
            df = pd.DataFrame(columns=column_list)
            df.index = df[DataOptions.Date]
            df = df.drop(DataOptions.Date, axis= 1) # axis = 1 means column
            self.CellDataFrame = df
            self.AggregationType = DataAggregationType.AggregationCell
            self.CellDataFrameExists = True

        #newDataSet = pd.DataFrame(DataCell_map, columns=DataOptions.GetOptionsList())
        newDataSet = pd.DataFrame(DataCell_map, columns=column_list)
        newDataSet.index = newDataSet[DataOptions.Date]
        newDataSet = newDataSet.drop(DataOptions.Date, axis=1)  # axis = 1 means column
        self.CellDataFrame = self.CellDataFrame.append(newDataSet)#DataFrameUtils.append_non_duplicates(self.CellDataFrame,newDataSet)
        self.CellDataFrame = self.CellDataFrame[~self.CellDataFrame.index.duplicated(keep='first')]

        return

    def GetDataOptions(self, DataCell_map: List[Mapping[DataOptions,Any]])->List[DataOptions]:
        options = set()
        for cell in DataCell_map:
            for key in cell.keys():
                options.add(key)

        return list(options)

class AggregationValuePair:
    AggregationValue: Any = None  # this is of Any type
    InnerAggregation: DataAggregate = None  # this is DataAggregation

    def __init__(self, AggregationValue, InnerAggregation):
        self.AggregationValue = AggregationValue
        self.InnerAggregation = InnerAggregation