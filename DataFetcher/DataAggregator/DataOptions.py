import enum

class DataOptions( enum.Enum ):
    Date = 0
    Open = 1
    High = 2
    Low = 3
    Close = 4
    Volume = 5
    Turnover = 6
    AdjClose = 7
    Volatility = 8
    SettlePrice = 9
    NumberOfContracts = 10
    OpenInterest = 11
    ChangeInOI = 12
    Underlying = 13
    Last = 14
    PremiumTurnover = 15

    @staticmethod
    def GetOptionsList():
        options = []
        for option in DataOptions:
            options.append( option )
        return options
