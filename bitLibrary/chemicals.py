
import life
import bits

class AminoAcid(life.Bit):
    """ Used as a building block for life. """
    atoms = [7,6,2]

    ENTROPY = 3
    ENTHALPY = 3
    
    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        self.randomWalk()

class Water(life.Bit):
    atoms = [1,1,0]

    ENTROPY = 5
    ENTHALPY = 0

    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        self.randomWalk()

class Necrosis(life.Bit):
    atoms = [0,0,0]

    ENTROPY = 4
    ENTHALPY = 0

    def __init__(self, x, y, atoms):
        super().__init__(x,y)

        self.atoms = list(atoms)

        life.Looper(self, self.randomWalk, 5)

    def tick(self):
        super().tick()
    
class CausticNecrosis(life.Bit):
    atoms = [0,0,0]

    ENTROPY = 10
    ENTHALPY = 0

    def __init__(self, x, y, atoms):
        super().__init__(x,y)

        self.atoms = list(atoms)

        life.Looper(self, self.randomWalk, 5)

    def tick(self):
        super().tick()
