
import biohex

class ATP(biohex.life.Bit):
    ATOMS = [5,5,5]

    ENTROPY = 4
    ENTHALPY = 30

    def __init__(self, x, y):
        super().__init__(x,y)

    def enthalpyDeath(self):
        self.becomeBit(ADP)

    def tick(self):
        self.randomWalk()

class ADP(biohex.life.Bit):
    ATOMS = [5,5,5]
    ENTROPY = 5
    ENTHALPY = 0

    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        self.randomWalk()

class AminoAcid(biohex.life.Bit):
    """ Used as a building block for life. """
    ATOMS = [7,6,2]

    ENTROPY = 3
    ENTHALPY = 15
    
    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        self.randomWalk()

class Water(biohex.life.Bit):
    ATOMS = [1,1,0]

    ENTROPY = 5
    ENTHALPY = 0

    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        self.randomWalk()

class DenaturedNecrosis(biohex.life.Bit):
    ATOMS = [0,0,0]

    ENTROPY = 4
    ENTHALPY = 0

    def __init__(self, x, y):
        super().__init__(x,y)

        biohex.life.Looper(self, self.randomWalk, 5)

    def tick(self):
        super().tick()

class Necrosis(biohex.life.Bit):
    ATOMS = [0,0,0]
    ENTROPY = 4
    ENTHALPY = 0

    def __init__(self, x, y):
        super().__init__(x,y)

        biohex.life.Looper(self, self.randomWalk, 5)

    def tick(self):
        super().tick()

class LipidSalt(biohex.life.Bit):
    ATOMS = [5,5,1]

    ENTROPY = 5
    ENTHALPY = 0

    def __init__(self, x, y):
        super().__init__(x,y)

        biohex.life.Looper(self, self.randomWalk, 5)

    def tick(self):
        super().tick()

class Lipid(biohex.life.Bit):
    ATOMS = [5,5,1]

    ENTROPY = 4
    ENTHALPY = 100

    def __init__(self, x, y):
        super().__init__(x,y)

        biohex.life.Looper(self, self.randomWalk, 2)

    def enthalpyDeath(self):
        self.becomeBit(LipidSalt)

    def tick(self):
        super().tick()
    
class CausticNecrosis(biohex.life.Bit):
    ATOMS = [0,0,0]

    ENTROPY = 10
    ENTHALPY = 0

    def __init__(self, x, y):
        super().__init__(x,y)

        biohex.life.Looper(self, self.randomWalk, 5)

    def tick(self):
        super().tick()
