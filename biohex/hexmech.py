#!/usr/bin/env python3

import pickle
from os.path import exists
from os import mkdir

s = None
t = None
r = None
h = None
w = None

rings = {}

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
    setMetric('w', int(width))

def setMetric(name, value):
    globals()[name.lower()] = value

def getMetric(name):
    value = globals()[name.lower()]
    if value != None:
        return value
    else:
        raise HexagonMetricError("Hexagon metrics not set")

class VectorFakeBit(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def moveto(self, pos):
        self.x, self.y = pos

class Vector(object):
    def __init__(self, bit=None, direction=0, x=0, y=0):
        if bit:
            self.bit = bit
        else:
            self.bit = VectorFakeBit(x, y)
        self._direction = direction
        self._ahead = None

    def __serialize__(self):
        return (self._direction, self._ahead)

    def getAngleTowards(self, posVector):
        # TODO
        pass

    def moveAhead(self):
        self.bit.moveto(self.ahead)

    def getPosition(self):
        return (self.bit.x, self.bit.y)
    position = property(getPosition)

    def reverse(self):
        if self.angle != None:
            self.angle -= 3
    def turnLeft(self, units=1):
        self.angle -= units
    def turnRight(self, units=1):
        self.angle += units

    def getAhead(self):
        if self._direction != None:
            setOdd = (
                (-1, 0), (0, -1), (1, 0), (1, 1), (0, 1), (-1, 1))
            setEven = (
                (-1, -1), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 0))
            if isOdd(self.bit.x):
                setThis = setOdd
            else:
                setThis = setEven
            return (setThis[self._direction][0] + self.bit.x, setThis[self._direction][1] + self.bit.y)
        
        else:
            return (self._ahead[0] + self.bit.x, self._ahead[1] + self.bit.y)
    
    def setAhead(self, value):
        setOdd = (
            (-1, 0), (0, -1), (1, 0), (1, 1), (0, 1), (-1, 1))
        setEven = (
            (-1, -1), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 0))
        
        if value in setOdd and hexmech.isOdd(self.bit.x):
            self._direction = setOdd.index(value)
        elif value in setEven and hexmech.isEven(self.bit.x):
            self._direction = setEven.index(value)
        else:
            self._direction = None
            self._ahead = (self.bit.x + value[0], self.bit.y + value[1])

    ahead = property(getAhead, setAhead)

    def getBehind(self):
        self.angle -= 3
        value = self.getAhead()
        self.angle += 3
        return value

    behind = property(getBehind)

    def getAngle(self):
        if self._direction != None:
            return self._direction % 6
        else:
            return None
        
    def setAngle(self, value):
        if value != None:
            self._direction = value % 6
        else:
            self._direction = None
            
    angle = property(getAngle, setAngle)

def loadRing(distance, set):
    print("LOADING RING")
    try:
        file = open("assets/ringCache/{},{}.ringdat".format(distance, set), "rb")
        return pickle.load(file)
    except:
        return None

def loadRings(amount=20):
    global rings

    for i in range(amount):
        ringList = []
        for ii in range(2):
            ring = loadRing(i+1, ii)
            ringList.append(ring)
        if None not in ringList:
            rings[i + 1] = ringList

def getRing(x, y, distance):
    set = isOdd(x)
    newPos = []
    if distance in rings:
        for xi,yi in rings[distance][set]:
            newPos.append((xi+x, yi+y))
    else:
        rings[distance] = [(),()]
        for i in range(2):
            saveGridRing(distance, i)
            rings[distance][i] = loadRing(distance, i)

        return getRing(x, y, distance)
    return newPos

def getRings(x, y, amount):
    posList = []
    for i in range(amount):
        posList += getRing(x,y,i+1)
    return posList

def getAdjs(x, y):
        """ Return all adjacent coordinate sets """
        coord = (x,y)

        setOdd = (
            (-1, 0), (0, -1), (1, 0), (1, 1), (0, 1), (-1, 1))
        setEven = (
            (-1, -1), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 0))

        if isOdd(coord[0]):
            setThis = setOdd
        else:
            setThis = setEven

        prod = []
        for vector in setThis:
            prod.append((coord[0] + vector[0], coord[1] + vector[1]))

        return prod

def saveGridRing(distance=1, set=0):
    tiles = []
    if distance == 1:
        tiles = getAdjs(0,0)
    else:
        if not set:
            newVector = Vector(None, 0, 0, 0)
        else:
            newVector = Vector(None, 0, 1, 0)
            
        for i in range(distance):
                    newVector.moveAhead()
                
        tiles.append(newVector.position)

        newVector.turnRight(2)

        for e in range(6):
            for i in range(distance):
                newVector.moveAhead()
                if newVector.position not in tiles:
                    tiles.append(newVector.position)

            newVector.turnRight(1)

    if not exists("assets/ringCache/"):
        mkdir("assets/ringCache/")
    file = open("assets/ringCache/{},{}.ringdat".format(distance, set), "wb")
    pickle.dump(tiles, file)

def saveGridRings(amount=20):
    for i in range(amount):
        for ii in range(2):
            saveGridRing(i + 1, ii)

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

def main():
    saveGridRings(50)

if __name__ == "__main__":
    import traceback

    try:
        main()
    except:
        print(traceback.format_exc())
        input()
