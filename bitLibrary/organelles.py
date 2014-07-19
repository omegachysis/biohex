
import life
import bits
import random

class Ribosome(life.Bit):
    """ Turns genetic code and raw materials into proteins. """
    
    atoms = [800,500,300]

    ENTROPY = 1
    ENTHALPY = 100

    def __init__(self, x, y, dna):
        super().__init__(x,y)

        # keep a storage available of atoms to use
        # to build the organisms parts
        self.atoms = list(Ribosome.atoms)

        self.rna = bits.functions._convertDNA(dna)
        self.codeType = self.rna[0]
        self.frame = 1

        self.vector.heading = random.randrange(6)

        self.enthalpyLooper(100)

    def enthalpyZero(self):
        self.die()

    def makeBit(self, bitclass, pos, args={}):
        print(bitclass.atoms)
        print(self.atoms)
        if len([i for i in range(len(self.atoms)) if \
                self.atoms[i] >= bitclass.atoms[i]]) == len(self.atoms):
            for i in range(len(self.atoms)):
                self.atoms[i] -= bitclass.atoms[i]

            return bitclass(pos[0], pos[1], **args)

        else:
            return None

    def tick(self):
        codon = self.rna[self.frame]
        
        if self.codeType == "A":
            if codon == 'm':
                if self.moveto(self.vector.ahead):
                    self.makeBit(bits.ProteinCellMembrane, self.vector.behind)
        
        self.frame += 1
