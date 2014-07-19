
import life
import bits
import random

class OrganelleMatrix(life.Bit):
    atoms = [1,1,1]

    ENTROPY = 1
    ENTHALPY = 10
    
    def __init__(self, x, y):
        super().__init__(x,y)

        self.startEnthalpy(100)

    def tick(self):
        super().tick()

class Ribosome(life.Bit):
    """ Turns genetic code and raw materials into proteins. """
    
    atoms = [800,500,300]

    ENTROPY = 1
    ENTHALPY = 1000

    def __init__(self, x, y, dna):
        super().__init__(x,y)

        # keep a storage available of atoms to use
        # to build the organisms parts
        self.atoms = list(Ribosome.atoms)

        self.rna = bits.functions._convertDNA(dna)
        self.codeType = self.rna[0]
        self.frame = 1

        self.vector.heading = random.randrange(6)

        self.startEnthalpy(100)

    def tick(self):
        super().tick()
        
        codon = self.rna[self.frame]
        
        if self.codeType == 'A':
            
            if codon == 'g':
                self.frame += 1
                codonArg = self.rna[self.frame]

                growthAmount = ord(codonArg)
                giveAtoms = [i * growthAmount for i in bits.ProteinCellMembrane.atoms]
                giveEnthalpy = bits.ProteinCellMembrane.ENTHALPY * growthAmount

                print(growthAmount)
                print(giveAtoms)
                
                self.makeBit(bits.ProteinMembraneGrower, self.vector.behind,
                             enthalpy = giveEnthalpy, atoms = giveAtoms,
                             args = {"growingAngle" : self.vector.angle - 3})

                self.vector.turnRight()
                
                self.makeBit(bits.ProteinMembraneGrower, self.vector.behind,
                             enthalpy = giveEnthalpy, atoms = giveAtoms,
                             args = {"growingAngle" : self.vector.angle - 3})

                self.vector.turnLeft(2)
                
                self.makeBit(bits.ProteinMembraneGrower, self.vector.behind,
                             enthalpy = giveEnthalpy, atoms = giveAtoms,
                             args = {"growingAngle" : self.vector.angle - 3})

                self.vector.turnRight()

            elif codon == 'r':
                self.vector.turnRight()
            elif codon == 'l':
                self.vector.turnLeft()

            elif codon == 'm':
                if self.moveto(self.vector.ahead):
                    if not self.makeBit(bits.OrganelleMatrix, self.vector.behind):
                        self.frame -= 1
                        self.moveto(self.vector.behind)
                    
            elif codon == 'Q':
                self.becomeBit(bits.OrganelleMatrix, {}, True)
                               
            else:
                self.frame += 1
        
        self.frame += 1
