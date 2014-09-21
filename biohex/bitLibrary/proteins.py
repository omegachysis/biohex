
import life
import bits
import random

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

        if self.moveForward():
            
            if not self.makeBit(self.placingType, self.vector.behind):
                self.die()
            else:
                self.outwardAmount += 1

        else:
            if life.getBit(*self.vector.ahead).name == "ProteinCellMembrane":
                self.becomeBit(ProteinCellMembrane, args={}, saveEnthalpy=True)

        if self.outwardAmount == self.outwardLength:
            self.vector.turnRight(2)
            self.placingType = ProteinCellMembrane
            self.outwardAmount += 1

class ProteinCellMembrane(life.Bit):

    ATOMS = [3,1,0]

    ENTROPY = 2
    ENTHALPY = 3

    THERMAL_RANGE = [30,70]

    def __init__(self, x, y):
        super().__init__(x,y)

        self.startEnthalpy(random.randrange(100,500))

    def multiply(self):
        positions = self.getAdjValids()
        self.becomeBits(ProteinCellMembrane, positions, args={}, saveEnthalpy=True)

    def enthalpyProgress(self):
        super().enthalpyProgress()

        self.siphonResources("Lipid", 20, amountEnthalpy=self.ENTHALPY, amountAtoms=self.ATOMS,
                             limitEnthalpy=self.ENTHALPY*5, limitAtoms=[i*5 for i in self.ATOMS],
                             technique=life.locals.distanceLookup.RING_CACHE)

        if self.enthalpy >= self.ENTHALPY * 5:
            self.multiply()

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