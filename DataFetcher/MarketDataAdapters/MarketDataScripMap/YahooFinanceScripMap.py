import typing
class YahooFinanceScripMap:
    switcher = {
        "NIFTY" : "^NSEI"
    }

    @staticmethod
    def GetScripName( symbol : str) -> str:
        return YahooFinanceScripMap.switcher.get(symbol.upper(),symbol)

