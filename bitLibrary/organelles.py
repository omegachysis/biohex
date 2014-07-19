
import life
import bits

class Ribosome(life.Bit):
    """ Turns genetic code and raw materials into proteins. """
    
    atoms = [800,500,300]

    ENTROPY = 1
    ENTHALPY = 100

    def __init__(self, x, y, dna):
        super().__init__(x,y)

        # keep a storage available of atoms to use
        # to build the organisms parts
        self.ATOMS = list(Ribosome.atoms)

        self.codeType = rna[0]
        self.frame = 1

        self.rna = convertDNA(dna)

        self.vector.heading = random.randrange(6)

        self.enthalpyLooper(100)

    def enthalpyZero(self):
        bits.Necrosis(self.x, self.y, self.atoms)

    def makeBit(self, bitclass, pos, args={}):
        if len([i for i in self.atoms if \
                self.atoms[i] >= bitclass.atoms[i]]) == len(self.atoms):
            for i in range(len(self.atoms)):
                self.atoms[i] -= bitclass.atoms[I]

            return bitclass(pos[0], pos[1], **args)

        else:
            return None

    def _nucleotidesToNumerals(self, nucleotides):
        nums = []
        for nuc in nucleotides:
            nums.append(('a','t','c','g').index(nuc.lower()))
        return nums
    
    def _baseFourToChar(self, nums):
        val = 0
        nums.reverse()
        for i in range(4):
            val += int(nums[i]) * ( 4 ** i)
        return chr(val)
    
    def _charToBaseFour(self, char):
        val = ord(char)
        nums = []
        for i in list(range(4)).__reversed__():
            divides = val // (4 ** i)
            val -= divides * (4 ** i)
            nums.append(divides)
        return nums

    def convertDNA(self, dna):
        nums = self._nucleotidesToNumerals(dna)
        rna = ""
        frame = []
        FRAME_WIDTH = 4
        for num in nums:
            frame.append(num)
            if len(frame) == FRAME_WIDTH:
                rna += self._baseFourToChar(frame)
                frame = []
        return rna

    def convertRNA(self, rna):
        dna = ""
        for char in rna:
            for num in self._charToBaseFour(char):
                dna += "ATCG"[num]
        return dna

    def tick(self):
        codon = self.rna[self.frame]
        
        if self.codeType == "A":
            if codon == 'm':
                if self.moveto(self.vector.ahead):
                    self.makeBit(bits.ProteinCellMembrane, self.vector.behind)
        
        self.frame += 1
