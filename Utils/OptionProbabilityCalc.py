
import scipy
import scipy.stats
from Structs.Spread import *
from Utils import MathUtils

def getRange( middle_value, sigma, probability_we_want ):
    upper = 1 - ((1-probability_we_want)/2)
    lower = (1 - probability_we_want)/2
    upperMul = scipy.stats.norm.ppf( upper )
    lowerMul = scipy.stats.norm.ppf( lower )
    return Spread((middle_value + (sigma*lowerMul)), (middle_value + (sigma*upperMul)))

def getRangeWithLeastCountRoundOff( middle_value, sigma, probability_we_want, leastCount ):
    spread = getRange( middle_value, sigma, probability_we_want )
    return Spread( MathUtils.round_off(spread.lower, leastCount) , MathUtils.round_off(spread.upper,leastCount) )