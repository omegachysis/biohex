
import random
import biohex

class GolgiComplex(biohex.life.Bit):
    ATOMS = [1,1,1]

    ENTROPY = 2
    ENTHALPY = 10

    def __init__(self, x, y):
        super().__init__(x,y)

        self.startEnthalpy(500)

    def tick(self):
        super().tick()

class OrganelleMatrix(biohex.life.Bit):
    ATOMS = [1,1,1]

    ENTROPY = 1
    ENTHALPY = 10
    
    def __init__(self, x, y):
        super().__init__(x,y)

        self.startEnthalpy(100)

        self.epigene = 0

    def getEpigene(self):
        return self._epigene
    def setEpigene(self, value):
        self._epigene = value
        self.epicode = value % 10
    epigene = property(getEpigene, setEpigene)

    def tick(self):
        super().tick()

        if self.epicode == 0:
            self.becomeBit(GolgiComplex, {}, True)

class Ribosome(biohex.life.Bit):
    """ Turns genetic code and raw materials into proteins. """
    
    ATOMS = [800,500,300]

    ENTROPY = 1
    ENTHALPY = 1000

    REPORT = ["frame", "matrixEpigene", "codeType", "chemicalIdentifier"]

    def __init__(self, x, y, dna):
        super().__init__(x,y)

        self.rna = biohex.bits.functions._convertDNA(dna)
        self.frame = 0

        self.codeType = self.rna[0]
        self.frame += 1

        self.chemicalIdentifier = random.randrange(0,100000)

        self.vector.angle = random.randrange(6)

        self.startEnthalpy(100)

        self.temperature = 100

    def tick(self):
        super().tick()
        
        codon = self.rna[self.frame]
        
        if self.codeType == 'A':
            if not hasattr(self, "matrixEpigene"):
                self.matrixEpigene = 0
            
            if codon == 'g':
                self.frame += 1
                codonArg1 = self.rna[self.frame]
                self.frame += 1
                codonArg2 = self.rna[self.frame]

                growthAmount = ord(codonArg1)
                giveAtoms = [i * growthAmount * 2 for i in biohex.bits.ProteinCellMembrane.ATOMS]
                giveEnthalpy = biohex.bits.ProteinCellMembrane.ENTHALPY * growthAmount * 2

                extraAmounts = ord(codonArg2) + growthAmount

                giveMoreAtoms = [i*(extraAmounts+growthAmount) for i in biohex.bits.ProteinCellMembrane.ATOMS]
                giveMoreEnthalpy = biohex.bits.ProteinCellMembrane.ENTHALPY * (growthAmount + extraAmounts)
                
                self.makeBit(biohex.bits.ProteinMembraneGrower, self.vector.behind,
                             enthalpy = giveEnthalpy, atoms = giveAtoms,
                             args = {"growingAngle" : self.vector.angle - 3, "outwardLength" : growthAmount})

                self.vector.turnRight()
                
                self.makeBit(biohex.bits.ProteinMembraneGrower, self.vector.behind,
                             enthalpy = giveMoreEnthalpy, atoms = giveMoreAtoms,
                             args = {"growingAngle" : self.vector.angle - 3, "outwardLength" : growthAmount})

                self.vector.turnLeft(2)
                
                self.makeBit(biohex.bits.ProteinMembraneGrower, self.vector.behind,
                             enthalpy = giveEnthalpy, atoms = giveAtoms,
                             args = {"growingAngle" : self.vector.angle - 3, "outwardLength" : growthAmount})

                self.vector.turnRight()

            elif codon == 'r':
                self.vector.turnRight()
            elif codon == 'l':
                self.vector.turnLeft()

            elif codon == 'm':
                if self.moveForward():
                    newMatrix = self.makeBit(biohex.bits.OrganelleMatrix, self.vector.behind)
                    if not newMatrix:
                        self.frame -= 1
                        self.moveto(self.vector.behind)
                    else:
                        newMatrix.epigene = self.matrixEpigene
                        self.matrixEpigene += 1

            elif codon == ' ':
                self.moveto(self.vector.ahead)
                    
            elif codon == 'Q':
                self.becomeBits(biohex.bits.ATP, self.getAdjValids(), {}, True)

            else:
                self.frame += 1
        
        self.frame += 1
