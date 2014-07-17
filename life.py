
import random
import hexmech
import glob
from os import path

import math

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

def getAdjacent(bit=None, coord=None):
    """ Return all adjacent coordinate sets """
    if bit:
        coord = (bit.x, bit.y)

    setOdd = (
        (-1, 0), (0, -1), (1, 0), (1, 1), (0, 1), (-1, 1))
    setEven = (
        (-1, -1), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 0))

    if hexmech.isOdd(coord[0]):
        setThis = setOdd
    else:
        setThis = setEven

    prod = []
    for vector in setThis:
        prod.append((coord[0] + vector[0], coord[1] + vector[1]))

    return prod

def distance(bit0, bit1):
    return math.sqrt((bit0.x-bit1.x)**2 + (bit0.y-bit1.y)**2)

def getAdjacentBits(bit):
    bits = []
    for position in getAdjacent(bit):
        ibit = Bit.world.bitPositions[position[0]][position[1]]
        if ibit:
            bits.append(ibit)
    return bits

def isBitHere(x, y):
    return bool(Bit.world.bitPositions[x][y])
getBit = isBitHere
    
def isValid(x, y):
    return (x >= 0 and x < Bit.world.width and \
           y >= 0 and y < Bit.world.height and \
            not isBitHere(x, y))

def getAdjacentValids(bit=None, coord=None):
    prod = getAdjacent(bit, coord)
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

        self.destroyed = False
        
    def destroy(self):
        Bit.world.removeBit(self)
        Bit.world.bitPositions[self.x][self.y] = 0
        Bit.world.markUpdate(self.x, self.y)
        Bit.world.unmarkDirty(self)
        self.destroyed = True
        
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
    
    #def drawEmpty(self, pos): None

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
            #self.drawEmpty((bit.x, bit.y))
            self.bitPositions[bit.x][bit.y] = 0

    def tick(self):
        for bit in self.bits:
            bit.tick()
