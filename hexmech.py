
s = None
t = None
r = None
h = None

def isOdd(num):
    return bool(num & 0x1)
def isEven(num):
    return not (num & 0x1)

class HexagonMetricError(Exception): pass

def setMetrics(width, height, t):
    setMetric('s', int(width - 2 * t))
    setMetric('r', int(height / 2))
    setMetric('h', int(height))
    setMetric('t', int(t))

def setMetric(name, value):
    globals()[name.lower()] = value

def getMetric(name):
    value = globals()[name.lower()]
    if value != None:
        return value
    else:
        raise HexagonMetricError("Hexagon metrics not set")

def coordsToPixels(xgrid, ygrid, xpixeloffset=0, ypixeloffset=0):
    """
    Convert the grid coordinate location of a hexagon
    to pixel a position on the screen.
    """
    
    t = getMetric('t')
    s = getMetric('s')
    h = getMetric('h')
    r = getMetric('r')
    
    xcoord = xgrid * (t + s)
    ycoord = ygrid * h

    if isOdd(xgrid):
        ycoord += r

    xcoord += xpixeloffset
    ycoord += ypixeloffset

    return (xcoord, ycoord)

def pixelsToCoords(x, y):
    """
    Convert the pixel coordinates of a mouse cursor to find
    which hexagon on the coordinate grid it lies on.
    """

    pass
