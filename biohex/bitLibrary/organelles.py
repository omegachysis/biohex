
from biohex import life
from biohex import bits
import random

class OrganelleMatrix(life.Bit):
    ATOMS = [1,1,1]

    ENTROPY = 1
    ENTHALPY = 10
    
    def __init__(self, x, y):
        super().__init__(x,y)

        self.startEnthalpy(100)

    def tick(self):
        super().tick()

class Ribosome(life.Bit):
    """ Turns genetic code and raw materials into proteins. """
    
    ATOMS = [800,500,300]

    ENTROPY = 1
    ENTHALPY = 1000

    def __init__(self, x, y, dna):
        super().__init__(x,y)

        self.rna = bits.functions._convertDNA(dna)
        self.codeType = self.rna[0]
        self.frame = 1

        self.chemicalIdentifier = random.randrange(0,100000)

        self.vector.angle = random.randrange(6)

        self.startEnthalpy(100)

    def tick(self):
        super().tick()
        
        codon = self.rna[self.frame]
        
        if self.codeType == 'A':
            
            if codon == 'g':
                self.frame += 1
                codonArg = self.rna[self.frame]
                self.frame += 1
                codonArg2 = self.rna[self.frame]

                growthAmount = ord(codonArg)
                giveAtoms = [i * growthAmount * 2 for i in bits.ProteinCellMembrane.ATOMS]
                giveEnthalpy = bits.ProteinCellMembrane.ENTHALPY * growthAmount * 2

                extraAmounts = ord(codonArg2) + growthAmount

                giveMoreAtoms = [i*(extraAmounts+growthAmount) for i in bits.ProteinCellMembrane.ATOMS]
                giveMoreEnthalpy = bits.ProteinCellMembrane.ENTHALPY * (growthAmount + extraAmounts)
                
                self.makeBit(bits.ProteinMembraneGrower, self.vector.behind,
                             enthalpy = giveEnthalpy, atoms = giveAtoms,
                             args = {"growingAngle" : self.vector.angle - 3, "outwardLength" : growthAmount})

                self.vector.turnRight()
                
                self.makeBit(bits.ProteinMembraneGrower, self.vector.behind,
                             enthalpy = giveMoreEnthalpy, atoms = giveMoreAtoms,
                             args = {"growingAngle" : self.vector.angle - 3, "outwardLength" : growthAmount})

                self.vector.turnLeft(2)
                
                self.makeBit(bits.ProteinMembraneGrower, self.vector.behind,
                             enthalpy = giveEnthalpy, atoms = giveAtoms,
                             args = {"growingAngle" : self.vector.angle - 3, "outwardLength" : growthAmount})

                self.vector.turnRight()

            elif codon == 'r':
                self.vector.turnRight()
            elif codon == 'l':
                self.vector.turnLeft()

            elif codon == 'm':
                if self.moveForward():
                    if not self.makeBit(bits.OrganelleMatrix, self.vector.behind):
                        self.frame -= 1
                        self.moveto(self.vector.behind)

            elif codon == ' ':
                self.moveto(self.vector.ahead)
                    
            elif codon == 'Q':
                self.becomeBits(bits.Lipid, self.getAdjValids(), {}, True)

            else:
                self.frame += 1
        
        self.frame += 1
