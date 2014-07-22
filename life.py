
import random
import hexmech
import glob
from os import path

import bits

import math
import traceback

class locals():
    RING_LOAD = 0
    DISTANCE_SEARCH = 1

bitList = []
for file in glob.glob("bitGraphics/*.png"):
    bitList.append(path.basename(file)[:-4])

def getBit(x, y):
        try:
            return Bit.world.bitPositions[x][y]
        except:
            return False

def isValid(x, y):
    return (x >= 0 and x < Bit.world.width and \
           y >= 0 and y < Bit.world.height and \
            not getBit(x, y))

class Looper(object):
    def __init__(self, bit, command, delay):
        self.timer = delay
        self.delay = delay
        self.command = command
        self.bit = bit
        self.bit.addLooper(self)
        self.start()
        
    def __serialize__(self):
        # NOTE: THIS MEANS COMMANDS CAN ONLY BE DERIVED FROM THE CURRENT BIT!
        serializedCommand = self.command.__name__
        return (self.timer, self.delay, serializedCommand, self.paused)
    
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

def loadSavedBit(self, pickledBit, index):
    newBit = Bit(pickledBit['x'], pickledBit['y'])
    for variableName, value in pickledBit.items():
        if variableName != "index":
            eval("newBit.{} = {}".format(variableName, value))
    for pickledLooper in newBit.loopers:
        looperCommand = eval("newBit." + pickledLooper[2])
        newLooper = Looper(newBit, looperCommand, pickledLooper[1])
        newLooper.timer = pickledLooper[0]
        newLooper.paused = pickledLooper[3]

    pickledVector = newBit.vector
    newBit.vector = Vector(newBit, pickledVector[0])
    newBit._ahead = pickledVector[1]

class Bit(object):
    world = None
    name = "Test"
    lister = {}

    ENTHALPY = 0
    ENTROPY = 0
    
    def __init__(self, x, y):
        self.name = self.__class__.__name__

        self.enthalpy = self.ENTHALPY
        if self.ATOMS != None:
            self.atoms = list(self.ATOMS)
        else:
            self.atoms = None
        
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

        self.vector = hexmech.Vector(self, 0)

        self.enthalpyLooper = None
        self.loopers = []

    def getPosition(self):
        return (self.x, self.y)
    def setPosition(self, newPosition):
        self.moveto(newPosition)
    position = property(getPosition, setPosition)

    def getRings(self, distance):
        return hexmech.getRings(self.x, self.y, distance)

    def getRing(self, distance):
        return hexmech.getRing(self.x, self.y, distance)

    def die(self):
        self.becomeBit(bits.Necrosis, {}, True)
        
    def dieError(self):
        self.becomeBit(bits.CausticNecrosis, {}, False)

    def siphonEnthalpy(self, bitName, distance, amount=1, limit=None, technique=locals.RING_LOAD):
        for bit in self.lookout(bitName, distance, technique = technique):
            self._siphonEnthalpyBit(bit, amount, limit)

    def siphonAtoms(self, bitName, distance, amount=[1,1,1], limit=None, technique=locals.RING_LOAD):
        for bit in self.lookout(bitName, distance, technique = technique):
            self._siphonAtomsBit(bit, amount, limit)

    def _siphonEnthalpyBit(self, bit, amount=1, limit=None):
        maxCanGrab = limit - self.enthalpy
        if not limit:
            self.grabEnthalpy(bit, amount)
        else:
            if amount >= maxCanGrab:
                self.grabEnthalpy(bit, maxCanGrab)
            else:
                self.grabEnthalpy(bit, amount)
    def _siphonAtomsBit(self, bit, amount=[1,1,1], limit=None):
        if limit:
            diffs = [0]*len(amount)
            for atomIndex in range(len(amount)):
                diffs[atomIndex] = limit[atomIndex] - self.atoms[atomIndex]
                if diffs[atomIndex] > amount[atomIndex]:
                    diffs[atomIndex] = amount[atomIndex]

            self.grabAtoms(bit, diffs)
        else:
            self.grabAtoms(bit, bit.atoms)

    def siphonResources(self, bitName, distance, amountEnthalpy=1, amountAtoms=[1,1,1], limitEnthalpy=None, limitAtoms=None, technique=locals.RING_LOAD):
        for bit in self.lookout(bitName, distance, technique = technique):
            self._siphonEnthalpyBit(bit, amountEnthalpy, limitEnthalpy)
            self._siphonAtomsBit(bit, amountAtoms, limitAtoms)

    def grabAtoms(self, bit, amount=[1,1,1]):
        amount = list(amount)

        condition = []
        i = 0
        for atomAmount in bit.atoms:
            if atomAmount >= amount[i]:
                condition.append(True)
            i += 1

        if len(condition) == len(bit.atoms):
            for atomIndex in range(len(amount)):
                bit.atoms[atomIndex] -= amount[atomIndex]
                self.atoms[atomIndex] += amount[atomIndex]
            return True
        else:
            return False
        
    def grabEnthalpy(self, bit, amount=1):
        if bit.enthalpy >= amount:
            bit.enthalpy -= amount
            self.enthalpy += amount
            self.enthalpyUpdate()
            bit.enthalpyUpdate()
            return True
        elif bit.enthalpy < amount and bit.enthalpy > 0:
            self.enthalpy += bit.enthalpy
            bit.enthalpy = 0
            self.enthalpyUpdate()
            bit.enthalpyUpdate()
            return True
        else:
            return False

    def becomeBit(self, bitclass, args={}, saveEnthalpy=True):
        self.destroy()
        
        # We know that this will be successful 100% of the time.
        # you cannot fail making a bit where you just destroyed one.

        madeBit = None
        
        if saveEnthalpy:
            madeBit = self.makeBit(bitclass, (self.x, self.y), args, enthalpy = self.enthalpy,
                         atoms = self.atoms)
        else:
            madeBit = self.makeBit(bitclass, (self.x, self.y), args, enthalpy = None,
                         atoms = self.atoms)
            
    def becomeBits(self, bitclass, positions, args={}, saveEnthalpy=True):
        self.destroy()

        filteredPositions = []
        # remove repeated positions
        for pos in positions:
            if pos not in filteredPositions:
                filteredPositions.append(tuple(pos))

        if self.position in positions:
            positions.remove(self.position)

        amount = len(positions) + 1
        if isinstance(args, dict):
            args = [args] * amount

        i = 0
        for position in positions:
            if saveEnthalpy:
                if not self.makeBit(bitclass, position, args[i], enthalpy = bitclass.ENTHALPY,
                                    atoms = bitclass.ATOMS):
                    break
            else:
                if not self.makeBit(bitclass, position, args[i], enthalpy = None,
                                    atoms = bitclass.ATOMS):
                    break

        if saveEnthalpy:
            self.makeBit(bitclass, self.position, args[-1], enthalpy = self.enthalpy,
                         atoms = self.atoms)
        else:
            self.makeBit(bitclass, self.position, args[-1], enthalpy = None,
                         atoms = self.atoms)

    def makeBits(self, bitclass, positions, args=[], atoms=None, enthalpy=None):
        filteredPositions = []
        # remove repeated positions
        for pos in positions:
            if pos not in filteredPositions:
                filteredPositions.append(tuple(pos))
        
        if enthalpy == None:
            enthalpy = bitclass.ENTHALPY
        if atoms == None:
            atoms = list(bitclass.ATOMS)
        else:
            atoms = list(atoms)

        amount = len(positions)
        if isinstance(args, type(dict)):
            args = [args]*amount

        totalAtoms = [i*amount for i in atoms]
        totalEnthalpy = enthalpy * amount

        valids = [i for i in positions if not getBit(*i)]

        if args == [] or args == {}:
            args = [{}]*amount

        # this will completely fail if even ONE of the positions
        # is not valid (i.e. a bit is there).  Use becomeBits()
        # if it is important that it happens.  becomeBits() always
        # works because if anything is leftover from being invalid,
        # the "becoming" will take the missing value.

        if len([i for i in range(len(self.atoms)) if \
                self.atoms[i] >= totalAtoms[i]]) == len(self.atoms) and \
                self.enthalpy >= totalEnthalpy and \
                len(valids) == len(positions):
            for i in range(len(totalAtoms)):
                self.atoms[i] -= totalAtoms[i]

            self.enthalpy -= totalEnthalpy
            newBits = []
            i = 0
            for pos in positions:
                argSet = args[i]
                newBit = bitclass(pos[0], pos[1], **argSet)
                newBits.append(newBit)
                i += 1

            return newBits
        else:
            return None

    def makeBit(self, bitclass, pos, args={}, atoms=None, enthalpy=None):
        if enthalpy == None:
            enthalpy = bitclass.ENTHALPY
        if atoms == None:
            atoms = list(bitclass.ATOMS)
        else:
            atoms = list(atoms)
            
        if len([i for i in range(len(self.atoms)) if \
                self.atoms[i] >= atoms[i]]) == len(self.atoms) and \
                self.enthalpy >= enthalpy and \
                not getBit(*pos):
            for i in range(len(self.atoms)):
                self.atoms[i] -= atoms[i]
                
            self.enthalpy -= enthalpy

            newBit = bitclass(pos[0], pos[1], **args)
            newBit.enthalpy = enthalpy
            newBit.atoms = atoms

            return newBit

        else:
            return None

    def enthalpyDeath(self):
        self.die()

    def startEnthalpy(self, multiplier=10):
        self.enthalpyLooper = Looper(self, self.enthalpyProgress, multiplier)

    def enthalpyUpdate(self):
        if self.enthalpy <= 0:
            self.enthalpyDeath()
            if self.enthalpyLooper:
                self.enthalpyLooper.stop()

    def enthalpyProgress(self):
        self.enthalpy -= 1
        self.enthalpyUpdate()

    def getIndex(self):
        if self in self.world.bits:
            return self.world.bits.index(self)
        else:
            return None
    def setIndex(self, newIndex):
        pass
    index = property(getIndex)

    def makePickle(self):
        data = {}
        
        for key, value in vars(self).items():
            
            if key == "vector":
                value = value.__serialize__()
                
            elif isinstance(value, Bit):
                value = value.getIndex()
                
            elif key == "loopers":
                value = [i.__serialize__() for i in value]

            data[key] = value

        return data

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

    def moveTowards(self, pos):
        i = 0
        for dim in pos:
            if dim < -1:
                pos[i] = -1
            elif dim > 1:
                pos[i] = 1

        return self.vector.getAngleTowards(pos)

    def lookout(self, bitName, searchRadius, technique = locals.RING_LOAD):
        if not isinstance(bitName, str):
            bitName = bitName.name

        if technique == locals.RING_LOAD:
            return [getBit(*i) for i in self.getRings(searchRadius) if getBit(*i) and \
                getBit(*i).name == bitName]

        elif technique == locals.DISTANCE_SEARCH:
            return [bit for bit in self.getList(bitName) if self.distance(bit) <= searchRadius]

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

        return hexmech.getAdjs(self.x, self.y)

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
    def __init__(self, width, height, passErrors = False):
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

        self.passingErrors = passErrors

        Bit.world = self

        self.tickNumber = 0

    def getPassingErrors(self):
        return self._passingErrors
    def setPassingErrors(self, value):
        self._passingErrors = value
        if value:
            self.tick = self.tickPassErrors
        else:
            self.tick = self.tickNonPassErrors
    passingErrors = property(getPassingErrors, setPassingErrors)

    def save(self, filename):
        import pickle
        file = open(filename, 'wb')
        pickledBits = []
        for bit in self.bits:
            pickledBits.append(bit.makePickle())
        pickle.dump(pickledBits, file)
        file.close()

    def load(self, filename):
        import pickle
        file = open(filename, 'rb')
        pickledBits = pickle.load(file)
        index = 0
        for pickle in pickledBits:
            loadSavedBit(pickle, index)
            index += 1

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

    def tickPassErrors(self):
        self.tickNumber += 1
        for bit in self.bits:
            try:
                bit.tick()
            except:
                print("----------------------------")
                print(self), " DIED BY FATAL ERROR:"
                print(traceback.format_exc())
                print("----------------------------\n")
                bit.dieError()
                
    def tickNonPassErrors(self):
        self.tickNumber += 1
        for bit in self.bits:
            bit.tick()

    def tick(self): pass
