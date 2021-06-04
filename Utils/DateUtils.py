from Utils.PRECOMP import *

def convertToDateTime( var )->datetime:
    if type(var) is date:
        return datetime.combine( var, datetime.min.time() )
    if type(var) is datetime:
        return var
    raise( PrintWithObject("unable to convertToDateTime ", var) )

def convertToDate( var ) ->date:
    if type(var) is datetime:
        return var.date()
    if type(var) is date:
        return var
    raise( PrintWithObject("unable to convertToDate ", var) )

def PrintWithObject( message: str, var):
    printMessage = message+" ,var: " + str( var ) + ", type:" + str(type(var))
    print( printMessage )
    return printMessage