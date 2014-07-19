
import life
import bits

class ProteinCellMembrane(life.Bit):

    atoms = [3,1,0]

    ENTROPY = 2
    ENTHALPY = 10

    def __init__(self, x, y):
        super().__init__(x,y)

        self.enthalpyLooper(100)

    def enthalpyZero(self):
        self.die()

    def tick(self):
        super().tick()
