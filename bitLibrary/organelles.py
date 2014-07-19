
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

        self.startEnthalpy(100)

    def tick(self):
        super().tick()
        
        codon = self.rna[self.frame]
        
        if self.codeType == 'A':    # TAAT
            if codon == 'm':        # TCGT
                if self.moveto(self.vector.ahead):
                    self.makeBit(bits.ProteinCellMembrane, self.vector.behind)
                    
            elif codon == 'Q':      # TTAT
                self.die()
            else:
                self.frame += 1
        
        self.frame += 1
