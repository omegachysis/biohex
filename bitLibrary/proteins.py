
import life
import bits

class ProteinMembraneGrower(life.Bit):
    ATOMS = None

    ENTROPY = 1
    ENTHALPY = 0

    def __init__(self, x, y, growingAngle, outwardLength):
        super().__init__(x,y)

        self.vector.angle = growingAngle
        self.outwardLength = outwardLength

        self.outwardAmount = 0

        self.placingType = ProteinConnectiveMembrane

        self.startEnthalpy(300)

    def tick(self):
        super().tick()

        if self.moveto(self.vector.ahead):
            
            if not self.makeBit(self.placingType, self.vector.behind):
                self.die()
            else:
                self.outwardAmount += 1

        if self.outwardAmount == self.outwardLength:
            self.vector.turnRight(2)
            self.placingType = ProteinCellMembrane
            self.outwardAmount += 1

class ProteinCellMembrane(life.Bit):

    ATOMS = [3,1,0]

    ENTROPY = 2
    ENTHALPY = 3

    def __init__(self, x, y):
        super().__init__(x,y)

        self.startEnthalpy(300)

    def enthalpyProgress(self):
        super().enthalpyProgress()
        
        self.siphonEnthalpy("Lipid", 20, amount = 5, limit = 5)

    def tick(self):
        super().tick()

class ProteinConnectiveMembrane(life.Bit):

    ATOMS = [3,1,0]

    ENTROPY = 2
    ENTHALPY = 3

    def __init__(self, x, y):
        super().__init__(x,y)

        self.startEnthalpy(300)

    def enthalpyProgress(self):
        super().enthalpyProgress()
        
        self.siphonEnthalpy("Lipid", 20, amount = 5, limit = 5)

    def tick(self):
        super().tick()