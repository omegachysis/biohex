
s = None
t = None
r = None
h = None

def isOdd(num):
    return bool(num & 0x1)
def isEven(num):
    return not (num & 0x1)

class HexagonMetricError(Exception): pass

def setMetric(name, value):
    globals()[name.lower()] = value

def getMetric(name):
    value = globals()[name.lower()]
    if value != None:
        return value
    else:
        raise HexagonMetricError("Hexagon metrics not set")

def gridToPixels(xgrid, ygrid):
    xcoord = xgrid * (getMetric('t') + getMetric('s'))
