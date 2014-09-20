
import random
import hexmech
import glob
from os import path

import bits

import math
import traceback
import experiment

# storage class for constants
class locals():
    class distanceLookup():
        RING_CACHE = 0
        BIT_LISTER = 1

# load up bit graphic asset names
bitList = []
for file in glob.glob("bitGraphics/*.png"):
    bitList.append(path.basename(file)[:-4])

def getBit(x, y):
    """Return the bit at this location.  If there is no bit, return False."""
    try:
        return Bit.world.bitPositions[x][y]
    except IndexError:
        return False

def isValid(x, y):
    """
    Return True if there is no bit at that 
    location and the location is not out of world range.
    """
    return (x >= 0 and x < Bit.world.width and \
           y >= 0 and y < Bit.world.height and \
            not getBit(x, y))

class Looper(object):
    """
    Paired with a Bit, creates a class that 
    will periodically run a command and repeat.
    """
    def __init__(self, bit, command, delay):
        self.timer = delay
        self.delay = delay
        self.command = command
        self.bit = bit
        self.bit.addLooper(self)
        self.start()
        
    def __serialize__(self):
        """Return a version of the looper that can be pickled."""
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
        """Destroy looper from bit memory."""
        self.bit.removeLooper(self)

def loadSavedBit(self, pickledBit, index):
    """Unpickle a serialized, pickled bit."""
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
    """
    The basic unit of matter in the Biohex simulations.
    Represents a single hexagon in the world.  Only one
    Bit can be in each tile at a given time.
    """
    world = None
    name = "Test"

    # stores a record of all bits, accessible to others.
    # stored on a 'name' basis.
    #  ex.: {"Test" : [Bit, Bit, ...], "Test 2" : [...]}
    lister = {}

    # ENTHALPY acts as a simulated unit of energy.
    #  Use a enthalpy looper to simulate a breakdown
    #  without a constant source of energy.
    #
    #  --- Note: only presented as a constant to signify default
    #       starting enthalpy.  Each Bit has its own 'enthalpy'
    #       attribute that changes with time.
    ENTHALPY = 0

    # ENTROPY acts as the simulated reality of
    #  the breakdown of complex, organized compounds
    #  into a more random state.  Use this as a guide
    #  to make sure that all reactions that take
    #  place result in total entropy increasing overall.
    ENTROPY = 0

    # THERMAL_RANGE is a two-element list
    # where the minimum temperature is first
    # and the maximum is second.  The bit will die
    # if the temperature at its location becomes
    # too high.  Set to None for no temperature breakdown.
    THERMAL_RANGE = None
    
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
        """Get all hexagon rings up to a distance around this bit's position."""
        return hexmech.getRings(self.x, self.y, distance)

    def getRing(self, distance):
        """Get a hexagon ring at a distance around this bit's position."""
        return hexmech.getRing(self.x, self.y, distance)

    def die(self):
        """Turn this bit into a Necrosis bit, prevserving current atoms and enthalpy."""
        self.becomeBit(bits.Necrosis, {}, True)

    def dieThermal(self):
        """Turn this bit into a DenaturedNecrosis bit, signifying that it overheated."""
        self.becomeBit(bits.DenaturedNecrosis, {}, True)
        
    def dieError(self):
        """Turn this bit into a CausticNecrosis bit, signifiying a critical internal error."""
        self.becomeBit(bits.CausticNecrosis, {}, False)

    def siphonEnthalpy(self, bitName, distance, amount=1, limit=None, technique=locals.distanceLookup.RING_CACHE):
        """
        Extract enthalpy in stages of amount from bits of bitName from a certain distance.  A limit
        can be set on the maximum level of enthalpy this bit should attempt to obtain before stopping.
        Technique is a class attribute from the life.locals.distanceLookup class.
        """
        for bit in self.lookout(bitName, distance, technique = technique):
            self._siphonEnthalpyBit(bit, amount, limit)

    def siphonAtoms(self, bitName, distance, amount=[1,1,1], limit=None, technique=locals.distanceLookup.RING_CACHE):
        """
        Extract atoms in stages of amount from bits of bitName from a certain distance.  A limit
        can be set on the maximum level of atoms this bit should attempt to obtain before stopping.
        Technique is a class attribute from the life.locals.distanceLookup class.
        """
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

    def siphonResources(self, bitName, distance, amountEnthalpy=1, amountAtoms=[1,1,1], limitEnthalpy=None, limitAtoms=None, technique=locals.distanceLookup.RING_CACHE):
        """
        Extract atoms and enthalpy in stages of amountEnthalpy and amountAtoms from bits of bitName from a certain distance.
        A limit can be set on the maximum level of atoms or enthalpy this bit should attempt to obtain before stopping.
        Technique is a class attribute from the life.locals.distanceLookup class.
        """
        for bit in self.lookout(bitName, distance, technique = technique):
            self._siphonEnthalpyBit(bit, amountEnthalpy, limitEnthalpy)
            self._siphonAtomsBit(bit, amountAtoms, limitAtoms)

    def grabAtoms(self, bit, amount=[1,1,1]):
        """Take atoms of amount from the bit.  Returns bool related to success of extraction."""
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
        """Take enthalpy of amount from the bit.  Returns bool related to success of extraction."""
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

    def checkTemperature(self):
        if self.THERMAL_RANGE:
            if self.world.getTemp(self.x, self.y) < self.THERMAL_RANGE[0] or \
                self.world.getTemp(self.x, self.y) > self.THERMAL_RANGE[1]:
                self.dieThermal()

    def tempRange(self, min, max):
        """Returns 1 if below minimum, returns 2 if above max, returns 0 if in range."""
        if self.world.getTemp(self.x, self.y) < min:
            return 1
        elif self.world.getTemp(self.x, self.y) > max:
            return 2
        else:
            return 0

    def becomeBit(self, bitclass, args={}, saveEnthalpy=True):
        """
        Turn this current bit into another bit, prevserving atoms in the process and
        optionally preserving enthalpy.  This will always be successful.
        """
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
        """
        Turn this current bit into multiple other bits, preserving atoms across
        all of them in the process and optionally preserving enthalpy.  At the
        end of the process, any remaining enthalpy or atoms from unsuccessful
        positions will be placed into the bit replacing the bit at this current
        position.
        """
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
        """
        Place multiple bits at positions, optionally giving that bit
        a certain amount of atoms and enthalpy from this bit.  If atoms
        and/or enthalpy amounts are not specified, the defaults inherited
        from bitclass will be used.  Returns 
        a list of bits placed if all the positions were valid.  If even
        one placement fails, None is returned and no bits are created.
        """
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

    def makeBit(self, bitclass, position, args={}, atoms=None, enthalpy=None):
        """
        Place a bit at a new position, optionally giving that bit
        a certain amount of atoms and enthalpy from this bit.  If atoms
        and/or enthalpy amounts are not specified, the defaults inherited
        from bitclass will be used.  Returns a placed bit if successful,
        and returns None of the placement was not valid.
        """ 
        if enthalpy == None:
            enthalpy = bitclass.ENTHALPY
        if atoms == None:
            atoms = list(bitclass.ATOMS)
        else:
            atoms = list(atoms)
            
        if len([i for i in range(len(self.atoms)) if \
                self.atoms[i] >= atoms[i]]) == len(self.atoms) and \
                self.enthalpy >= enthalpy and \
                not getBit(*position):
            for i in range(len(self.atoms)):
                self.atoms[i] -= atoms[i]
                
            self.enthalpy -= enthalpy

            newBit = bitclass(position[0], position[1], **args)
            newBit.enthalpy = enthalpy
            newBit.atoms = atoms

            return newBit

        else:
            return None

    def enthalpyDeath(self):
        """Same as die().  Can be overridden for special enthalpy deaths."""
        self.die()

    def startEnthalpy(self, multiplier=10):
        """Start an enthalpy looper with delay of multiplier ticks."""
        self.enthalpyLooper = Looper(self, self.enthalpyProgress, multiplier)

    def enthalpyUpdate(self):
        """Cause enthalpy death if conditions are satisfied."""
        if self.enthalpy <= 0:
            self.enthalpyDeath()
            if self.enthalpyLooper:
                self.enthalpyLooper.stop()

    def enthalpyProgress(self):
        """Decrease enthalpy by one and call enthalpyUpdate()."""
        self.enthalpy -= 1
        self.world.thermalTransfer(self.x, self.y, 1)
        self.enthalpyUpdate()
        self.checkTemperature()

    def getIndex(self):
        """Return index of bit in life.world.bits list."""
        if self in self.world.bits:
            return self.world.bits.index(self)
        else:
            return None
    index = property(getIndex)

    def makePickle(self):
        """Return data in the form of a serialized, picklable data piece."""
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

    def randomWalkTowardsType(self, bitName, searchRadius, technique = locals.distanceLookup.RING_CACHE):
        """
        Randomly walk the bit slowly over to any bit of bitName within the search radius.
        Technique is a class attribute of the life.locals.distanceLookup class.
        """
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

    def randomWalkTowards(self, bit, technique = locals.distanceLookup.RING_CACHE):
        """
        Randomly walk the bit slowly over to the bit.
        Technique is a class attribute of the life.locals.distanceLookup class.
        """
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
        """Move the bit through a vector pointing to the position."""
        i = 0
        for dim in pos:
            if dim < -1:
                pos[i] = -1
            elif dim > 1:
                pos[i] = 1

        return self.vector.getAngleTowards(pos)

    def lookout(self, bitName, searchRadius, technique = locals.distanceLookup.RING_CACHE):
        """
        Scan the area of searchRadius for a bit of bitName.  Technique is a 
        class attribute of the life.locals.distanceLookup class.
        """
        if not isinstance(bitName, str):
            bitName = bitName.name

        if technique == locals.distanceLookup.RING_CACHE:
            return [getBit(*i) for i in self.getRings(searchRadius) if getBit(*i) and \
                getBit(*i).name == bitName]

        elif technique == locals.DISTANCE_SEARCH:
            return [bit for bit in self.getList(bitName) if self.distance(bit) <= searchRadius]

    def addLooper(self, newLooper):
        """Add the looper to the list of loopers."""
        if newLooper not in self.loopers:
            self.loopers.append(newLooper)
    def removeLooper(self, looper):
        """Remove the looper from this bit."""
        if looper in self.loopers:
            self.loopers.remove(looper)

    def randomWalk(self):
        """Move to a random adjacent valid tile."""
        self.moveto(random.choice(self.getAdjValids(allowNull = False)))

    def distance(self, distantBit):
        """Get the distance to another bit using euclidean math."""
        return math.sqrt((self.x-distantBit.x)**2 + (self.y-distantBit.y)**2)

    def getAdjs(self, coord=None):
        """Return all adjacent coordinate sets """
        if not coord:
            coord = (self.x, self.y)

        return hexmech.getAdjs(self.x, self.y)

    def getAdjBits(self, coord=None):
        """Return all adjacent bits."""
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
        """Return all adjacent coordinate sets that are empty and valid."""
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
        """Move according to self.vector direction."""
        return self.moveto(self.vector.ahead)
    def moveBackward(self):
        """Move according to the opposite of self.vector direction."""
        return self.moveto(self.vector.behind)

    def getList(self, name=None):
        """Get the list of all bits of name.  If name is None, then the current name is used."""
        if name == None:
            name = self.name
        if name in __class__.lister:
            return __class__.lister[name]
        else:
            __class__.lister[name] = []
            return []
        
    def destroy(self):
        """Remove the bit from world and program memory."""
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
        """Mark the bit as a changed visible object."""
        self.world.markDirty(self)
    
    def moveto(self, x, y=None):
        """Move the bit to a coordinate set.  Return bool based on success."""
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

        self.checkTemperature()

        return val
            
    def move(self, dx, dy=None):
        """Move according to a coordinate vector.  Return bool based on success."""
        if dy == None:
            dy = dx[1]
            dx = dx[0]
        return self.moveto((self.x + dx, self.y + dy))

class World(object):
    """
    Represents the virtual space that Bits can move
    around in and interact with.
    """

    experiment = None

    AMBIENT_COOLING_FACTOR = 0.01
    _AMBIENT_TEMPERATURE_COOLING_DELAY = 10

    def __init__(self, width, height, passErrors = False):
        """
        Initialize a world with width and height in hexagon tiles.
        If passErrors is True, then when a Bit raises a fatal error,
        instead of crashing, it will decay into a special marker
        Bit and print the error in the command window.
        """

        self.width = width
        self.height = height

        self.area = self.width * self.height

        self.bits = []
        self.thermalData = []
        self.setAmbientTemperature(0)

        self._ambientTemperatureCoolingWait = 0

        # all the bits that have changed and need to be redrawn
        self.dirtyBits = []
        self.bitPositions = []
        for x in range(width):
            col = []
            for y in range(height):
                col.append(0)
            self.bitPositions.append(col)

        # all the positions that must be updated on the screen
        self.updatePositions = []

        self.passingErrors = passErrors

        Bit.world = self

        # tracks age in ticks
        self.tickNumber = 0

        # create new experiment object
        self.experiment = experiment.Experiment(self)

    def getTemp(self, x, y):
        return self.thermalData[y][x]
    def setTemp(self, x, y, value):
        self.thermalData[y][x] = value

    def ambientTemperatureAdjust(self, amount):
        for y in range(self.height):
            for x in range(self.width):
                self.thermalData[y][x] += amount

    def ambientCooling(self, factor=AMBIENT_COOLING_FACTOR):
        for y in range(self.height):
            for x in range(self.width):
                diff = self.thermalData[y][x] - self.ambientTemperature
                self.thermalData[y][x] -= diff * factor
                self.thermalDelta -= diff * factor

    def setAmbientTemperature(self, temperature):
        self.thermalData = []
        for y in range(self.height):
            self.thermalData.append([temperature] * self.width)
        self.thermalDelta = 0
        self.ambientTemperature = temperature

    def thermalTransfer(self, x, y, amount):
        self.thermalData[y][x] += amount
        self.thermalDelta += amount

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
        """Pickle entire current world experiment."""
        import pickle
        file = open(filename, 'wb')
        pickledBits = []
        for bit in self.bits:
            pickledBits.append(bit.makePickle())
        pickle.dump(pickledBits, file)
        file.close()

    def load(self, filename):
        """Load a pickled world experiment."""
        import pickle
        file = open(filename, 'rb')
        pickledBits = pickle.load(file)
        index = 0
        for pickle in pickledBits:
            loadSavedBit(pickle, index)
            index += 1

    # these are not needed for this instance of a World
    #  because they are graphical methods.  These are
    #  overridden by a graphical version of the World
    #  in graphics.py.
    def markDirty(self, bit): pass
    def unmarkDirty(self, bit): pass
    def markUpdate(self, x, y): pass
    def flush(self): pass
    
    #def drawEmpty(self, pos): None

    def erase(self, x, y):
        """Destroy the bit at this position if there is one."""
        for bit in self.bits:
            if bit.x == x and bit.y == y:
                bit.destroy()

    def addBit(self, bit):
        """If there is no bit in the bit's position, add the bit."""
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
        """Destroy the bit and remove all memory access."""
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
        self._ambientTemperatureCoolingWait -= 1
        if self._ambientTemperatureCoolingWait <= 0:
            self.ambientCooling()
            self._ambientTemperatureCoolingWait = self._AMBIENT_TEMPERATURE_COOLING_DELAY
                
    def tickNonPassErrors(self):
        self.tickNumber += 1
        for bit in self.bits:
            bit.tick()
        if self._ambientTemperatureCoolingWait <= 0:
            self.ambientCooling()
            self._ambientTemperatureCoolingWait = self._AMBIENT_TEMPERATURE_COOLING_DELAY

    def tick(self): pass
