
import life
import bits

class ProteinCellMembrane(life.Bit):

    atoms = [3,1,0]

    ENTROPY = 2
    ENTHALPY = 5

    def __init__(self, x, y):
        super().__init__(x,y)

        self.startEnthalpy(100)

    def tick(self):
        super().tick()
