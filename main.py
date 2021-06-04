from DataFetcher.DataBase.DataBaseAggregator import *
from Strategies.PairTrading_AllCorrelations import *
from Strategies.DividendCaptureFutureStock import *
from Strategies.OvernightCall import *
import traceback

DB = DataBaseAggregator()

try:
    # stocks = ['NIFTY','BAJAJ-AUTO.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS', 'BHARTIARTL.NS', 'BRITANNIA.NS', 'CIPLA.NS',
    #           'COALINDIA.NS', 'GAIL.NS', 'GRASIM.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'ICICIBANK.NS', 'INDUSINDBK.NS',
    #           'ITC.NS', 'KOTAKBANK.NS', 'LT.NS', 'MARUTI.NS', 'NESTLEIND.NS', 'NTPC.NS', 'ONGC.NS', 'RELIANCE.NS',
    #           'SHREECEM.NS', 'TATASTEEL.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS', 'ULTRACEMCO.NS', 'WIPRO.NS', 'ZEEL.NS',
    #           'AXISBANK.NS', 'ADANIPORTS.NS', 'ASIANPAINT.NS', 'BPCL.NS', 'INFRATEL.NS', 'DRREDDY.NS', 'EICHERMOT.NS',
    #           'HCLTECH.NS', 'HDFCBANK.NS', 'HDFC.NS', 'HINDUNILVR.NS', 'IOC.NS', 'INFY.NS', 'JSWSTEEL.NS', 'M&M.NS',
    #           'POWERGRID.NS', 'SBIN.NS', 'SPARC.NS', 'TATAMOTORS.NS', 'UPL.NS', 'VEDL.NS', 'YESBANK.NS']
    start = datetime(2015, 9, 20)
    end = datetime(2017, 12, 15)
    #strategy = PairTrading_AllCorrelations(stocks,start,end,DB )
    #strategy.CacheWarmUp()
    #ans = strategy.runStrategy()
    # import yfinance as yf

    # vedl = yf.Ticker('VEDL.NS')
    # strat = DividendCaptureFutureStock('VEDL', DB)
    # divdends = []
    # d = vedl.dividends[30:]
    # for div in range(0, len(d)):
    #     divdends.append(( datetime.combine(d.index[div].date(),datetime.min.time()), 0.67*d[div]))
    # strat.RunStrategy(divdends)
    #print(ans)
    strategy = OvernightCallStrategy(DB,'NIFTY', 1000000 )
    strategy.RunStrategy(start, end)

except Exception as e:
    traceback.print_exc()
    print(e)
    DB.OnCompleteSave()