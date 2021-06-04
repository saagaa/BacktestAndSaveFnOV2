from DataFetcher.DataAggregator.DataAggregate import *
from DataFetcher.IDataFetch import *
from datetime import datetime
from Structs.OptionTypes import OptionType
from Utils.ScripUtils import *
import pickle
import os
from DataFetcher.MarketDataAdapters.IMarketDataAdapter import *
from DataFetcher.DataAggregator.DataGranularity import *
from shutil import copyfile
from DataFetcher.MarketDataAdapters.NSEpyMarketDataAdapter import *
from DataFetcher.MarketDataAdapters.YahooFinanceMarketDataAdapter import *
import logging

logging.basicConfig(filename='app.log', filemode='wb')
logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s')

class DataFetcherConfig:
    LookBack: int = 1
    LookForward: int = 20
    DataInputPath = "C:\\Anshul\\money\\stockAndOptions\\AllData\\DataAggregator_v1.pickle"
    DataBackupFolder = "C:\\Anshul\\money\\stockAndOptions\\AllData\\Backup\\"

class DataBaseAggregator(IDataFetch):
    #dataAggregator : DataAggregate
    #fIsInitialised : bool = False
    def __init__(self):
        self.fIsInitialised : bool = False
        self.dataAggregator : DataAggregate =  DataAggregate(DataAggregationType.Empty)
        self.DataFetcherConfig = DataFetcherConfig
        self.marketDataAdaptors : Mapping[DataGranularity, IMarketDataAdapter] = {}
        self.PopulateMarketDataAdapters()
        self.Initialize()
        return

    def PopulateMarketDataAdapters(self):
        self.marketDataAdaptors[DataGranularity.Daily]  = NSEpyMarketDataAdapter()
        self.marketDataAdaptors[DataGranularity.Hourly] = YahooFinanceMarketDataAdapter()
        self.marketDataAdaptors[DataGranularity.Minutely] = YahooFinanceMarketDataAdapter()
        return

    def Initialize(self):
        if self.fIsInitialised == True:
            return
        self.fIsInitialised = True
        try:
            pickle_in = open(DataFetcherConfig.DataInputPath, "rb")
            self.dataAggregator = pickle.load(pickle_in)
        except:
            f = 0
        print(str(self.dataAggregator))


    def OnCompleteSave(self):
        self.DuplicateOldDataFiles()
        pickle_out = open(DataFetcherConfig.DataInputPath, "wb")
        pickle.dump(self.dataAggregator, pickle_out)
        pickle_out.close()
        return

    def get_expiry( self, year, month):
        pass

    def get_index_price_futures(self, symbol: str, dates: DatePair, expiryDateTime: datetime, granularity: DataGranularity, shouldDownloadData:bool = True)-> pd.DataFrame:
        marketDataAdapter : IMarketDataAdapter= self.marketDataAdaptors.get(granularity,None)
        if( marketDataAdapter == None):
            raise ("UnknownGranularity: " + str(granularity))

        dataAggregations = { DataAggregationType.Symbol: symbol,
                             DataAggregationType.SecurityType: DataSecurityType.IsFuture,
                             DataAggregationType.Granularity: granularity,
                             DataAggregationType.ExpiryDate : expiryDateTime}
        valuesInDB :pd.DataFrame = None
        valuesInDBBool :bool = False

        try:
            valuesInDB = self.dataAggregator.GetValue(dataAggregations)
            valuesInDBBool = True
        except:
            valuesInDB = None

        shouldDownloadData2 = True
        if valuesInDBBool == True:
            shouldDownloadData2 = self.ShouldIDownload(valuesInDB,dates[0], dates[1] )

        if( shouldDownloadData == False or shouldDownloadData2 == False):
            logging.debug('will not download data')
            return valuesInDB

        delta: timedelta = granularity.GetTimeDelta()
        dates2 = self.GetDataRetrievalTime(dates, granularity, expiryDateTime)

        if( valuesInDBBool == True ):
            try:
                if( len( valuesInDB.index ) > 0):
                    datesPair1 = (dates2[0], self.getSmallestIndex(valuesInDB).to_pydatetime() - delta)
                    datesPair2 = ( self.getMaximumIndex(valuesInDB).to_pydatetime() + delta, dates2[1])
                    logging.warning("will download data for " + str(datesPair1) +" and " + str(datesPair2) )
                    if(datesPair1[0] <= datesPair1[1]):
                        value = marketDataAdapter.get_price_futures(symbol=symbol, dates=datesPair1, expiryDateTime=expiryDateTime)
                        self.dataAggregator.ForceSetValue(value)

                    if(datesPair2[0] <= datesPair2[1]):
                        value = marketDataAdapter.get_price_futures(symbol=symbol, dates=datesPair2, expiryDateTime=expiryDateTime)
                        self.dataAggregator.ForceSetValue(value)
                else:
                    valuesInDBBool = False
            except Exception as e:
                print("DataBaseAggreagtor expection" + str(e))
                #valuesInDBBool = False

        if( valuesInDBBool==False):
            logging.warning("will download data for whole period as not data in DB")
            value = marketDataAdapter.get_price_futures(symbol=symbol, dates=dates2, expiryDateTime=expiryDateTime)
            self.dataAggregator.ForceSetValue(value)

        return self.SearchDataFrame(self.dataAggregator.GetValue(dataAggregations),dates[0], dates[1]+delta )

    def get_index_price_options(self, symbol: str, optionType: OptionType, strikePrice: int, dates: DatePair,
                          expiryDateTime: datetime, granularity: DataGranularity, forceDownloadData:bool = False)-> pd.DataFrame:
        marketDataAdapter : IMarketDataAdapter= self.marketDataAdaptors.get(granularity,None)
        if (marketDataAdapter == None):
            raise ("UnknownGranularity: " + str(granularity))

        expiryDateTime = convertToDateTime(expiryDateTime)
        dataAggregations = {DataAggregationType.Symbol: symbol,
                            DataAggregationType.SecurityType: DataSecurityType.IsOption,
                            DataAggregationType.Granularity: granularity,
                            DataAggregationType.ExpiryDate: expiryDateTime,
                            DataAggregationType.OptionType: optionType,
                            DataAggregationType.StrikePrice: strikePrice}
        valuesInDB: pd.DataFrame = None
        valuesInDBBool: bool = False

        try:
            valuesInDB = self.dataAggregator.GetValue(dataAggregations)
            valuesInDBBool = True
        except:
            valuesInDB = None

        shouldDownloadData = True
        if valuesInDBBool == True:
            shouldDownloadData = self.ShouldIDownload(valuesInDB,dates[0], dates[1] )

        if( forceDownloadData == False and shouldDownloadData == False):
            return valuesInDB

        delta: timedelta = granularity.GetTimeDelta()
        dates2 = self.GetDataRetrievalTime(dates, granularity, expiryDateTime)

        if (valuesInDBBool == True and forceDownloadData==False):
            try:
                if (len(valuesInDB.index) > 0):
                    datesPair1 = (dates2[0], self.getSmallestIndex(valuesInDB).to_pydatetime() - delta)
                    datesPair2 = ( self.getMaximumIndex(valuesInDB).to_pydatetime() + delta, dates2[1])
                    logging.debug("will download data for " + str(datesPair1) +" and " + str(datesPair2) )

                    if (datesPair1[0] <= datesPair1[1]):
                        value = marketDataAdapter.get_price_options(symbol=symbol,
                                                                    optionType=optionType,
                                                                    strikePrice=strikePrice,
                                                                    dates=datesPair1,
                                                                    expiryDateTime=expiryDateTime)
                        self.dataAggregator.ForceSetValue(value)

                    if (datesPair2[0] <= datesPair2[1]):
                        value = marketDataAdapter.get_price_options(symbol=symbol,
                                                                    optionType=optionType,
                                                                    strikePrice=strikePrice,
                                                                    dates=datesPair2,
                                                                    expiryDateTime=expiryDateTime)
                        self.dataAggregator.ForceSetValue(value)
                else:
                    valuesInDBBool = False
            except Exception as e:
                print("DataBaseAggreagtor expection" + str(e))
                #valuesInDBBool = False

        if valuesInDBBool == False or forceDownloadData == True:
            value = marketDataAdapter.get_price_options(symbol=symbol,
                                                        optionType=optionType,
                                                        strikePrice=strikePrice,
                                                        dates=dates2,
                                                        expiryDateTime=expiryDateTime)
            self.dataAggregator.ForceSetValue(value)

        return self.SearchDataFrame(self.dataAggregator.GetValue(dataAggregations),dates[0], dates[1]+delta )

    def get_index_prices(self, symbol: str, dates: DatePair, granularity: DataGranularity, shouldDownloadData:bool = True) -> pd.DataFrame:
        marketDataAdapter: IMarketDataAdapter = self.marketDataAdaptors.get(granularity, None)
        if (marketDataAdapter == None):
            raise ("UnknownGranularity: " + str(granularity))

        dataAggregations = {DataAggregationType.Symbol: symbol,
                            DataAggregationType.SecurityType: DataSecurityType.IsStock,
                            DataAggregationType.Granularity: granularity,}
        valuesInDB: pd.DataFrame = None
        valuesInDBBool: bool = False

        try:
            valuesInDB = self.dataAggregator.GetValue(dataAggregations)
            valuesInDBBool = True
        except:
            valuesInDB = None

        shouldDownloadData2 = True
        if valuesInDBBool == True:
            shouldDownloadData2 = self.ShouldIDownload(valuesInDB,dates[0], dates[1] )

        if( shouldDownloadData == False or shouldDownloadData2 == False):
            return valuesInDB


        delta: timedelta = granularity.GetTimeDelta()
        dates2 = self.GetDataRetrievalTime(dates, granularity, expiryDateTime=None)

        if (valuesInDBBool == True):
            try:
                if (len(valuesInDB.index) > 0):
                    datesPair1 = (dates2[0], self.getSmallestIndex(valuesInDB).to_pydatetime() - delta)
                    datesPair2 = ( self.getMaximumIndex(valuesInDB).to_pydatetime() + delta, dates2[1])

                    logging.debug("will download data for " + str(datesPair1) +" and " + str(datesPair2) )

                    if (datesPair1[0] <= datesPair1[1]):
                        value = marketDataAdapter.get_price_scrip(symbol=symbol, dates=datesPair1, granularity=granularity)
                        self.dataAggregator.ForceSetValue(value)

                    if (datesPair2[0] <= datesPair2[1]):
                        value = marketDataAdapter.get_price_scrip(symbol=symbol, dates=datesPair2, granularity=granularity)
                        self.dataAggregator.ForceSetValue(value)
                else:
                    valuesInDBBool = False
            except Exception as e:
                print("DataBaseAggreagtor expection" + str(e))
                #valuesInDBBool = False

        if valuesInDBBool == False:
            value = marketDataAdapter.get_price_scrip(symbol=symbol, dates=dates2, granularity=granularity)
            self.dataAggregator.ForceSetValue(value)

        return self.SearchDataFrame(self.dataAggregator.GetValue(dataAggregations),dates[0], dates[1]+delta )


    def DuplicateOldDataFiles(self):
        try:
            os.mkdir("Backup")
        except:
            a=0
        try:
            self.DuplicateOldDataFilesInternal()
        except Exception as e:
            print("Copying contents of input data failed, exception:" + str(e))

    def DuplicateOldDataFilesInternal(self):
        copyfile(DataFetcherConfig.DataInputPath, self.CreateBackupPath())

    def CreateBackupPath(self)->str:
        # pathFinal = "Backup\\" + \
        #             DataFetcherConfig.DataInputPath.split(".")[0] + "_" + \
        #             str(datetime.now()).replace(" ","_").replace(":","_").replace("-","_") + \
        #             ".pickle"
        pathFinal = DataFetcherConfig.DataBackupFolder + \
                    str(datetime.now().strftime("%Y-%m-%dT%H-%M-%S")) + \
                    DataFetcherConfig.DataInputPath.split(".")[0].split("\\")[-1] + \
                    ".pickle"
        return pathFinal

    def GetDataRetrievalTime(self,dates: DatePair, granularity: DataGranularity, expiryDateTime:datetime) -> DatePair:
        delta: timedelta = granularity.GetTimeDelta()
        dates2_0 = dates[0] - self.DataFetcherConfig.LookBack * delta
        dates2_1 = dates[1] + self.DataFetcherConfig.LookForward*delta

        if( expiryDateTime != None ):
            if (dates[1] + self.DataFetcherConfig.LookForward * delta >= datetime.combine(expiryDateTime,
                                                                                           datetime.max.time())):
                dates2_1 = expiryDateTime

        dates2 = (dates2_0, dates2_1)
        return dates2


    def SearchDataFrame(self, df: pd.DataFrame, startTime: datetime,endTime: datetime ) -> pd.DataFrame:
        return df.iloc[df.index.searchsorted(startTime): df.index.searchsorted(endTime)]

    def ShouldIDownload(self, valuesInDB: pd.DataFrame, start: datetime, end: datetime) -> bool:
        #DBstart = valuesInDB.index[0].to_pydatetime()
        #DBend = valuesInDB.index[len(valuesInDB) - 1].to_pydatetime()

        DBstart = self.getSmallestIndex(valuesInDB).to_pydatetime()
        DBend = self.getMaximumIndex(valuesInDB).to_pydatetime()

        if ( DBstart <= start and end<=DBend):
            return False
        ## if the end- 2days is greater than DBend we will anyways have to check...
        ## 2 days for sat and sunday
        elif DBstart >= start + timedelta(days=+2) or ( DBend <= end - timedelta(days=+2)):
            return True

        time1 = start

        for delta in range(0,2):
            time1 = time1 + timedelta(days=+1)
            if time1.weekday() <= 5 and time1<DBstart:
                return True
        time1 = start

        time1 = DBend
        for delta in range(0, 2):
            time1 = time1 + timedelta(days=+1)
            if time1.weekday() <= 5 and time1<=end:
                return True
        return False

    def getSmallestIndex(self, df: pd.DataFrame):
        return df.index.min()

    def getMaximumIndex(self, df:pd.DataFrame):
        return df.index.max()