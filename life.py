
import random
import hexmech
import glob
from os import path

import math

bitList = []
for file in glob.glob("bitGraphics/*.png"):
    bitList.append(path.basename(file)[:-4])

def getBit(x, y):
        try:
            return bool(Bit.world.bitPositions[x][y])
        except:
            return False

def isValid(x, y):
    return (x >= 0 and x < Bit.world.width and \
           y >= 0 and y < Bit.world.height and \
            not getBit(x, y))

class Vector(object):
    def __init__(self, bit, direction=0):
        self.bit = bit
        self._direction = direction
        self._ahead = None

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
            if hexmech.isOdd(self.bit.x):
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

class Looper(object):
    def __init__(self, bit, command, delay):
        self.timer = delay
        self.delay = delay
        self.command = command
        self.bit = bit
        self.bit.addLooper(self)
        self.start()
    def pause(self):
        self.paused = True
    def start(self):
        self.paused = False
    def tick(self):
        if not self.paused:
            self.timer -= 1
            if self.timer <= 0:
                self.timer = self.delay
                self.command()
    def stop(self):
        self.bit.removeLooper(self)

class Bit(object):
    world = None
    name = "Test"
    lister = {}
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        placed = self.world.addBit(self)
        
        if placed:
            self.dirty()
            self.destroyed = False
            if self.name in __class__.lister:
                __class__.lister[self.name].append(self)
            else:
                __class__.lister[self.name] = [self]
        else:
            self.destroyed = True

        self.vector = Vector(self, 0)

        self.loopers = []

    def randomWalkTowardsType(self, bitName, searchRadius):
        try:
            bit = random.choice(self.lookout(bitName, searchRadius))
            walkX = random.randrange(3) - 1
            walkY = random.randrange(3) - 1
            if self.x < bit.x:
                walkX = 1
            else:
                walkX = -1

            if self.y < bit.y:
                walkY = 1
            else:
                walkY = -1

            return self.move(walkX, walkY)
        except IndexError as e:
            return False

    def randomWalkTowards(self, bit):
        walkX = random.randrange(3) - 1
        walkY = random.randrange(3) - 1
        if self.x < bit.x:
            walkX = 1
        else:
            walkX = -1

        if self.y < bit.y:
            walkY = 1
        else:
            walkY = -1

        return self.move(walkX, walkY)

    def lookout(self, bitName, searchRadius):
        return [i for i in self.getList(bitName) if self.distance(i) <= searchRadius]

    def addLooper(self, newLooper):
        if newLooper not in self.loopers:
            self.loopers.append(newLooper)
    def removeLooper(self, looper):
        if looper in self.loopers:
            self.loopers.remove(looper)

    def randomWalk(self):
        self.moveto(random.choice(self.getAdjValids(allowNull = False)))

    def distance(self, distantBit):
        return math.sqrt((self.x-distantBit.x)**2 + (self.y-distantBit.y)**2)

    def getAdjs(self, coord=None):
        """ Return all adjacent coordinate sets """
        if not coord:
            coord = (self.x, self.y)

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

    def getAdjBits(self, coord=None):
        if not coord:
            coord = (self.x, self.y)
        bits = []
        for position in self.getAdjs(coord):
            try:
                ibit = Bit.world.bitPositions[position[0]][position[1]]
            except:
                ibit = None
            if ibit:
                bits.append(ibit)
        return bits

    def getAdjValids(self, coord=None, allowNull=True):
        if not coord:
            coord = (self.x, self.y)
            
        prod = self.getAdjs(coord)
        newprod = []
        for coord in prod:
            if isValid(coord[0], coord[1]):
                newprod.append(coord)

        if not newprod and not allowNull:
            newprod=[coord]
                
        return newprod

    def moveForward(self):
        return self.moveto(self.vector.ahead)
    def moveBackward(self):
        return self.moveto(self.vector.behind)

    def getList(self, name):
        if name in __class__.lister:
            return __class__.lister[name]
        else:
            __class__.lister[name] = []
            return []
        
    def destroy(self):
        Bit.world.removeBit(self)
        Bit.world.bitPositions[self.x][self.y] = 0
        Bit.world.markUpdate(self.x, self.y)
        Bit.world.unmarkDirty(self)
        self.destroyed = True

        if self in __class__.lister[self.name]:
            __class__.lister[self.name].remove(self)
        
    def tick(self):
        for looper in self.loopers:
            looper.tick()

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

    def save(self, filename):
        import pickle
        for bit in self.bits:
            

    def markDirty(self, bit): pass
    def unmarkDirty(self, bit): pass
    def markUpdate(self, x, y): pass
    def flush(self): pass
    
    #def drawEmpty(self, pos): None

    def erase(self, x, y):
        for bit in self.bits:
            if bit.x == x and bit.y == y:
                bit.destroy()

    def addBit(self, bit):
        if bit not in self.bits and not getBit(bit.x, bit.y):
            try:
                self.bitPositions[bit.x][bit.y] = bit
                self.bits.append(bit)
                return True
            except:
                return False
        else:
            return False
            
    def removeBit(self, bit):
        if bit in self.bits:
            self.bits.remove(bit)
            #self.drawEmpty((bit.x, bit.y))
            self.bitPositions[bit.x][bit.y] = 0

    def tick(self):
        for bit in self.bits:
            bit.tick()
