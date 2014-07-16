
bitList = [

    "Test",

    ]

def getAdjacent(x, y):
    """ Return all adjacent coordinate sets """
    sets = (
        (-1, 0), (0, -1), (1, 0),
        (1,  1), (0,  1), (-1,1),)

    prod = []
    for set in sets:
        prod.append((x + set[0], y + set[1]))

    return prod

class Bit(object):
    world = None
    
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

        self.world.addBit(self)

    def destroy(self):
        self.world.removeBit(self)

    def update(self):
        pass

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

    def update(self):
        for bit in self.bits:
            bit.update()
