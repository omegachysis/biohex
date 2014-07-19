
import life
import bits

class AminoAcid(life.Bit):
    ATOM1 = 7
    ATOM2 = 2
    ATOM3 = 6

    ENTROPY = 1
    ENTHALPY = 3
    
    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        pass

class Water(life.Bit):
    ATOM1 = 1
    ATOM2 = 1
    ATOM3 = 0

    ENTROPY = 3
    ENTHALPY = 0

    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        self.randomWalk()
