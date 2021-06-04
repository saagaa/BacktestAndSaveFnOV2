from Strategies.Straddle import *
from DataFetcher.DataSource.DataBase import *
from dateutil.relativedelta import relativedelta

# print('start')
# DataAggregator.Initialize()
#
# year =2019
# month =1
# startDate = date(year,month,1)
# print(startDate)
# # nd = startDate+relativedelta(months=+1)
# output = []
# yearLimit=2020
# expiries  = get_expiry_date(2018,1,index=False, stock=True)
#print( doCalender('NIFTY',startDate,yearLimit,expiries, index = True) )

#
#
#a = expiries[2007][1]
# print((expiries[2007][1]))
#
#a = dobuyStrangle(date(2016, 1, 1), 2020, expiries)
from Strategies.IronButterflyBuy import IronButterflyBuy

#SetProxy('103.73.183.28')
db = DataBase()
db.Initialize()
butterfly: IronButterflyBuy = Straddle()
butterfly.load_dataSourceVars(db)
endDates = set()
startDates =set()
for year in range( 2019,2020):
    for month in range( 3,13):
        endDates.update(db.get_expiry(year,month))
for dt in endDates:
    startDates.add( dt + relativedelta(days=-3))


    #expiryDates =
startDates = list(sorted(startDates))
endDates = list(sorted(endDates))

map = {}
try:
    #for i in range( 50,100):
    print("=====================================================================================")
    #print("=================================" + str(i)+"=============================================")
    print("=====================================================================================")
    out =  butterfly.ComputeStrategyReturns( startDates, endDates, endDates, 0/100, 0, True, "NIFTY",False)
    db.OnCompleteSave()
    map['NIFTY'] = out
    #a = doButterfly(date(2010, 1, 1), 2020, expiries)
    #print(a)
#
except Exception as e:
    print("Exception occured " + str(e))
    b = 0

print( " NETTTT" )
print( map )
db.OnCompleteSave()

