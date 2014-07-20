
import life
import bits

class ProteinMembraneGrower(life.Bit):
    ATOMS = None

    ENTROPY = 1
    ENTHALPY = 0

    def __init__(self, x, y, growingAngle):
        super().__init__(x,y)

        self.vector.angle = growingAngle

        self.startEnthalpy(300)

    def tick(self):
        super().tick()

        if self.moveto(self.vector.ahead):
            if not self.makeBit(ProteinCellMembrane, self.vector.behind):
                self.die()

class ProteinCellMembrane(life.Bit):

    ATOMS = [3,1,0]

    ENTROPY = 2
    ENTHALPY = 3

    def __init__(self, x, y):
        super().__init__(x,y)

        self.startEnthalpy(300)

    def enthalpyProgress(self):
        super().enthalpyProgress()
        
        self.siphonEnthalpy("Lipid", 20, amount = 3, limit = True)

    def tick(self):
        super().tick()
