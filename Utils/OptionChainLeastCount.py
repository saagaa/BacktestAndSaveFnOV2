def get_least_count( symbol ):
    if( symbol == "NIFTY" ):
        return 50
    if( symbol == "BANKNIFTY" ):
        return 100
    raise ValueError("Least count data unavailable for" + str( symbol ) )