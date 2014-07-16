
import life
import random

class NutrientAminoAcid(life.Bit):
    name = "NutrientAminoAcid"
    
    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        adjs = life.getAdjacentValids(self)
        if adjs:
            self.moveto(random.choice(adjs))

class Flesh(life.Bit):
    name = "Flesh"
    
    def __init__(self, x, y, attachments=[]):
        super().__init__(x,y)

        self.attachments = attachments

        self.lonely = True

    def tick(self):
        if self.lonely:
            pass

    def attach(self, bit):
        if bit not in self.attachments:
            self.attachments.append(bit)
        if self not in bit.attachments:
            bit.attachments.append(self)
        if len(self.attachments) >= 2:
            self.lonely = False
        if len(bit.attachments) >= 2:
            bit.lonely = False
    

# dna
#---------------
# f - place flesh
# r - turn right
# l - turn left


class Ribosome(life.Bit):
    name = "Ribosome"

    def __init__(self, x, y, dna, nutrition = 5):
        super().__init__(x,y)

        self.dna = dna
        self.dnaFrame = 0
        self.nutrition = nutrition
        self.heading = random.randrange(6)

        self.frustration = 0

        self.previousFlesh = None

    def turn(self, vec):
        self.heading += vec
        self.heading %= 6

    def tick(self):
        try:
            codon = self.dna[self.dnaFrame]
        except:
            codon = ''
            
        if codon is 'f':
            if self.nutrition > 0:
                if self.move(life.headingVector(self, self.heading)):
                    fleshpos = life.headingVector(self, life.headingVectorReverse(self.heading))
                    fleshpos = (fleshpos[0]+self.x, fleshpos[1]+self.y)

                    if not life.isBitHere(*fleshpos):
                        self.frustration = 0
                        self.nutrition -= 1
                        self.dnaFrame += 1
                        newFlesh = Flesh(fleshpos[0], fleshpos[1])
                        if self.previousFlesh:
                            newFlesh.attach(self.previousFlesh)
                        self.previousFlesh = newFlesh
                        
                else:
                    self.frustration += 1
                    if self.frustration >= 10:
                        self.turn(1)
                        
        elif codon is 'r':
            self.turn(1)
            self.dnaFrame += 1
        elif codon is 'l':
            self.turn(-1)
            self.heading %= 6
            self.dnaFrame += 1
        elif codon is 'q':
            self.destroy()
        else:
            self.dnaFrame += 1

        for bit in life.getAdjacentBits(self):
            if bit.name is "NutrientAminoAcid":
                self.nutrition += 10
                bit.destroy()

        
