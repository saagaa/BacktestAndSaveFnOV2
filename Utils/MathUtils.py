def round_off(x, base=50):
    return base * round(x/base)

def IsValidDataPoint( x ):
    if( x!=None):
        return True
    return False