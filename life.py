
import random
import hexmech

bitList = [

    "Test",

    ]

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

def isValid(x, y, world):
    return (x >= 0 and x < world.width and \
           y >= 0 and y < world.height)

def getAdjacentValids(bit):
    prod = getAdjacent(bit)
    newprod = []
    for coord in prod:
        if isValid(coord[0], coord[1], bit.world):
            newprod.append(coord)
    return newprod

class Bit(object):
    world = None
    name = "Test"
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.world.addBit(self)
        
    def destroy(self):
        self.world.removeBit(self)
    def tick(self): pass
    
    def moveto(self, x, y=None):
        if y == None:
            y = x[1]
            x = x[0]
            
        if isValid(x, y, self.world):
            self.x = x
            self.y = y
            
    def move(self, dx, dy=None):
        if dy == None:
            dy = dx[1]
            dx = dx[0]
            
        self.moveto((self.x + dx, self.y + dy))

class Walker(Bit):
    name = "Test"
    
    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        print(self.x, self.y, end = "")
        self.moveto(random.choice(getAdjacentValids(self)))
        print(" ->", self.x, self.y)

class World(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.bits = []

        Bit.world = self

    def erase(self, x, y):
        for bit in self.bits:
            if bit.x == x and bit.y == y:
                bit.destroy()

    def addBit(self, bit):
        if bit not in self.bits:
            self.bits.append(bit)
    def removeBit(self, bit):
        if bit in self.bits:
            self.bits.remove(bit)

    def tick(self):
        for bit in self.bits:
            bit.tick()
