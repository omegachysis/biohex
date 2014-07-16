
import random
import hexmech
import glob
from os import path

bitList = []
for file in glob.glob("bits/*.png"):
    bitList.append(path.basename(file)[:-4])

def headingVector(bit, heading):
    """ Return a vector according to a direction to move. """
    setOdd = (
        (-1, 0), (0, -1), (1, 0), (1, 1), (0, 1), (-1, 1))
    setEven = (
        (-1, -1), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 0))
    if hexmech.isOdd(bit.x):
        setThis = setOdd
    else:
        setThis = setEven

    return setThis[heading]

def headingVectorReverse(heading):
    """ Return a vector going in the opposite heading direction. """
    return (heading + 3) % 6

def getAdjacent(bit):
    """ Return all adjacent coordinate sets """
    setOdd = (
        (-1, 0), (0, -1), (1, 0), (1, 1), (0, 1), (-1, 1))
    setEven = (
        (-1, -1), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 0))

    if hexmech.isOdd(bit.x):
        setThis = setOdd
    else:
        setThis = setEven

    prod = []
    for vector in setThis:
        prod.append((bit.x + vector[0], bit.y + vector[1]))

    return prod

def getAdjacentBits(bit):
    bits = []
    for position in getAdjacent(bit):
        ibit = Bit.world.bitPositions[position[0]][position[1]]
        if ibit:
            bits.append(ibit)
    return bits

def isBitHere(x, y):
    return bool(Bit.world.bitPositions[x][y])
    
def isValid(x, y):
    return (x >= 0 and x < Bit.world.width and \
           y >= 0 and y < Bit.world.height and \
            not isBitHere(x, y))

def getAdjacentValids(bit):
    prod = getAdjacent(bit)
    newprod = []
    for coord in prod:
        if isValid(coord[0], coord[1]):
            newprod.append(coord)
    return newprod

class Bit(object):
    world = None
    name = "Test"
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.world.addBit(self)
        self.dirty()
        
    def destroy(self):
        Bit.world.removeBit(self)
        Bit.world.bitPositions[self.x][self.y] = 0
        Bit.world.markUpdate(self.x, self.y)
        Bit.world.unmarkDirty(self)
        
    def tick(self): pass

    def dirty(self):
        self.world.markDirty(self)
    
    def moveto(self, x, y=None):
        if y == None:
            y = x[1]
            x = x[0]

        val = False

        Bit.world.bitPositions[self.x][self.y] = 0
        if isValid(x, y):
            Bit.world.markUpdate(self.x,self.y)
            self.x = x
            self.y = y
            self.dirty()
            val = True
            
        Bit.world.bitPositions[self.x][self.y] = self

        return val
            
    def move(self, dx, dy=None):
        if dy == None:
            dy = dx[1]
            dx = dx[0]
        return self.moveto((self.x + dx, self.y + dy))

class World(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.bits = []

        self.dirtyBits = []
        self.bitPositions = []
        for x in range(width):
            col = []
            for y in range(height):
                col.append(0)
            self.bitPositions.append(col)

        self.updatePositions = []

        Bit.world = self

    def markDirty(self, bit): None
    def unmarkDirty(self, bit): None
    def markUpdate(self, x, y): None

    def erase(self, x, y):
        for bit in self.bits:
            if bit.x == x and bit.y == y:
                bit.destroy()

    def addBit(self, bit):
        if bit not in self.bits and not isBitHere(bit.x, bit.y):
            self.bits.append(bit)
            self.bitPositions[bit.x][bit.y] = bit
            
    def removeBit(self, bit):
        if bit in self.bits:
            self.bits.remove(bit)
            self.bitPositions[bit.x][bit.y] = 0

    def tick(self):
        for bit in self.bits:
            bit.tick()
