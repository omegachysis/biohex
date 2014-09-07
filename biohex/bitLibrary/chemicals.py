
from biohex import life
from biohex import bits

class AminoAcid(life.Bit):
    """ Used as a building block for life. """
    ATOMS = [7,6,2]

    ENTROPY = 3
    ENTHALPY = 15
    
    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        self.randomWalk()

class Water(life.Bit):
    ATOMS = [1,1,0]

    ENTROPY = 5
    ENTHALPY = 0

    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        self.randomWalk()

class Necrosis(life.Bit):
    ATOMS = [0,0,0]

    ENTROPY = 4
    ENTHALPY = 0

    def __init__(self, x, y):
        super().__init__(x,y)

        life.Looper(self, self.randomWalk, 5)

    def tick(self):
        super().tick()

class LipidSalt(life.Bit):
    ATOMS = [5,5,1]

    ENTROPY = 5
    ENTHALPY = 10

    def __init__(self, x, y):
        super().__init__(x,y)

        life.Looper(self, self.randomWalk, 5)

    def tick(self):
        super().tick()

class Lipid(life.Bit):
    ATOMS = [5,5,1]

    ENTROPY = 4
    ENTHALPY = 50

    def __init__(self, x, y):
        super().__init__(x,y)

        life.Looper(self, self.randomWalk, 2)

    def enthalpyDeath(self):
        self.becomeBit(LipidSalt)

    def tick(self):
        super().tick()
    
class CausticNecrosis(life.Bit):
    ATOMS = [0,0,0]

    ENTROPY = 10
    ENTHALPY = 0

    def __init__(self, x, y):
        super().__init__(x,y)

        life.Looper(self, self.randomWalk, 5)

    def tick(self):
        super().tick()
