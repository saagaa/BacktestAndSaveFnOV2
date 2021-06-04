from typing import *

index_names = [
    "NIFTY",
    "SENSEX"
]

def IsIndex( scrip : str) -> bool:
    if scrip.upper() in index_names:
        return True
    return False

def getNSEComponents() -> List[str]:
    return ['NIFTY', 'BAJAJ-AUTO.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS', 'BHARTIARTL.NS', 'BRITANNIA.NS', 'CIPLA.NS',
     'COALINDIA.NS', 'GAIL.NS', 'GRASIM.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'ICICIBANK.NS', 'INDUSINDBK.NS',
     'ITC.NS', 'KOTAKBANK.NS', 'LT.NS', 'MARUTI.NS', 'NESTLEIND.NS', 'NTPC.NS', 'ONGC.NS', 'RELIANCE.NS',
     'SHREECEM.NS', 'TATASTEEL.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS', 'ULTRACEMCO.NS', 'WIPRO.NS', 'ZEEL.NS',
     'AXISBANK.NS', 'ADANIPORTS.NS', 'ASIANPAINT.NS', 'BPCL.NS', 'INFRATEL.NS', 'DRREDDY.NS', 'EICHERMOT.NS',
     'HCLTECH.NS', 'HDFCBANK.NS', 'HDFC.NS', 'HINDUNILVR.NS', 'IOC.NS', 'INFY.NS', 'JSWSTEEL.NS', 'M&M.NS',
     'POWERGRID.NS', 'SBIN.NS', 'SPARC.NS', 'TATAMOTORS.NS', 'UPL.NS', 'VEDL.NS', 'YESBANK.NS']