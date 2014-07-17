
import life
import random

class NutrientAminoAcid(life.Bit):
    name = "NutrientAminoAcid"
    lister = []
    def __init__(self, x, y):
        super().__init__(x,y)
        NutrientAminoAcid.lister.append(self)

    def destroy(self):
        super().destroy()
        try:
            NutrientAminoAcid.lister.remove(self)
        except:
            pass

    def tick(self):
        adjs = life.getAdjacentValids(self)
        if adjs:
            self.moveto(random.choice(adjs))

class Necrosis(life.Bit):
    name = "Necrosis"
    lister = []
    def __init__(self, x, y):
        super().__init__(x,y)
        self.timer = 0
        self.delay = 10
        Necrosis.lister.append(self)
    def destroy(self):
        super().destroy()
        try: Necrosis.lister.remove(self)
        except: pass
    def tick(self):
        self.timer -= 1
        if self.timer <= 0:
            adjs = life.getAdjacentValids(self)
            if adjs:
                self.moveto(random.choice(adjs))
            self.timer = self.delay

class AcidStrong(life.Bit):
    name = "AcidStrong"
    def __init__(self, x, y):
        super().__init__(x,y)
        self.timer = 0
        self.delay = 5
    def tick(self):
        self.timer -= 1
        if self.timer <= 0:
            adjs = life.getAdjacentValids(self)
            if adjs:
                self.moveto(random.choice(adjs))
            self.timer = self.delay
        for bit in life.getAdjacentBits(self):
            bit.destroy()
            if random.random()<.5:
                self.destroy()
                SolventNeutral(self.x, self.y)

class SolventNeutral(life.Bit):
    name = "SolventNeutral"
    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        adjs = life.getAdjacentValids(self)
        if adjs:
            self.moveto(random.choice(adjs))

class Oxidizer(life.Bit):
    name = "Oxidizer"
    lister = []
    def __init__(self, x, y):
        super().__init__(x,y)
        self.timer = 0
        self.delay = 5
        Oxidizer.lister.append(self)
    def destroy(self):
        super().destroy()
        try: Oxidizer.lister.remove(self)
        except: pass
    def tick(self):
        self.timer -= 1
        if self.timer <= 0:
            adjs = life.getAdjacentValids(self)
            if adjs:
                self.moveto(random.choice(adjs))
            self.timer = self.delay
        for bit in life.getAdjacentBits(self):
            if bit.name is "Membrane":
                bit.destroy()
                self.destroy()
                for attachment in bit.attachments:
                    attachment.destroy()

class Antioxidant(life.Bit):
    name = "Antioxidant"
    def __init__(self, x, y):
        super().__init__(x,y)
        self.timer = 0
        self.delay = 2

        self.timer1 = 5
        self.delay1 = 5
    def tick(self):
        self.timer -= 1
        if self.timer <= 0:
            adjs = life.getAdjacentValids(self)
            if adjs:
                self.moveto(random.choice(adjs))
            self.timer = self.delay
        self.timer1 -= 1
        if self.timer1 <= 0:
            once = False
            for oxibit in Oxidizer.lister:
                if life.distance(self, oxibit) <= 15:
                    oxibit.destroy()
                    once = True
            self.timer1 = self.delay1
            if once:
                if random.random() < .3:
                    self.destroy()

class Flesh(life.Bit):
    name = "Flesh"
    
    def __init__(self, x, y, attachments=[], flexWait=5):
        super().__init__(x,y)

        self.attachments = list(attachments)

        self.lonely = True

        self.flexWait = flexWait
        self.flexibility = random.randrange(5,8)
        self.stagnation = 0

        self.lifetime = flexWait * 2

    def tick(self):
        if self.lonely:
            pass
        else:
            if self.flexWait <= 0:
                self.pullflex()
            else:
                self.flexWait -= 1

        if self.lifetime < self.stagnation:
            self.destroy()

    def pullflex(self):
        ads = life.getAdjacentValids(self)
        if ads and len(self.attachments) >= 2:
            oldX = self.x
            oldY = self.y
            
            self.moveto(random.choice(ads))

            adjs = life.getAdjacentValids(self)
            
            attachmentAdjs0 = life.getAdjacentValids(self.attachments[0])
            attachmentAdjs1 = life.getAdjacentValids(self.attachments[1])

            attachmentAdjs0 = [i for i in attachmentAdjs0 if i in adjs and tuple(i) != (self.x, self.y)]
            attachmentAdjs1 = [i for i in attachmentAdjs1 if i in adjs and tuple(i) != (self.x, self.y) and
                               i not in attachmentAdjs0]


            if attachmentAdjs0 and attachmentAdjs1:
                adj0 = random.choice(attachmentAdjs0)
                adj1 = random.choice(attachmentAdjs1)

                membrane0 = Membrane(*adj0)
                membrane1 = Membrane(*adj1)

                self.flexibility -= 1
                if self.flexibility <= 0:
                    self.destroy()
                    membraneCentral = Membrane(self.x, self.y)
                else:
                    membraneCentral = self
                
                membrane0.attach(self.attachments[0])
                membrane1.attach(self.attachments[1])

                self.completelyUnattach()

                membraneCentral.attach(membrane0)
                membraneCentral.attach(membrane1)

            else:
                self.moveto(oldX, oldY)
                self.stagnation += 1

                if self.stagnation >= 10:
                    self.completelyUnattach()
                    self.destroy()
                    FibrousGrowthTissue(self.x, self.y)
        else:
            self.stagnation += 1
                

    def completelyUnattach(self):
        for attachBit in self.attachments:
            self.unattach(attachBit)
        self.attachments = []

    def unattach(self, bit):
        if bit:
            if bit in self.attachments:
                self.attachments.remove(bit)
            if self in bit.attachments:
                bit.attachments.remove(self)
            if len(self.attachments) < 2:
                self.lonely = True
            if len(bit.attachments) < 2:
                bit.lonely = True

    def attach(self, bit):
        if bit:
            if bit not in self.attachments:
                self.attachments.append(bit)
            if self not in bit.attachments:
                bit.attachments.append(self)
            if len(self.attachments) >= 2:
                self.lonely = False
            if len(bit.attachments) >= 2:
                bit.lonely = False

class FibrousGrowthTissue(life.Bit):
    name = "FibrousGrowthTissue"

    def __init__(self, x, y, lifetime=100):
        super().__init__(x,y)

        self.lifetime = lifetime
        self._lifetime = lifetime

    def tick(self):
        self.lifetime -= 1
        
        if self.lifetime == 0:
            count = 0
            abits = life.getAdjacentBits(self)
            for abit in abits:
                if abit.name == "FibrousGrowthTissue":
                    count += 1
            if count <= 3:
                self.destroy()
                MembraneDouble(self.x, self.y)
            
        if self.lifetime == -self._lifetime:
            self.destroy()

class Cytoplasm(life.Bit):
    name = "Cytoplasm"

    def __init__(self, x, y, lifetime=100):
        super().__init__(x,y)

        self.lifetime = lifetime
        self._lifetime = lifetime

    def tick(self):
        self.lifetime -= 1
        
        if self.lifetime == 0:
            count = 0
            abits = life.getAdjacentBits(self)
            for abit in abits:
                if abit.name == "Cytoplasm":
                    count += 1
            if count <= 3:
                self.destroy()
                MembraneDouble(self.x, self.y)
            
        if self.lifetime == -self._lifetime:
            self.destroy()

class MembraneDouble(life.Bit):
    name = "MembraneDouble"

    def __init__(self, x, y, lifetime=200):
        super().__init__(x,y)

        self.lifetime = lifetime

    def tick(self):
        self.lifetime -= 1
        for bit in life.getAdjacentBits(self):
            if bit.name is "Membrane":
                bit.destroy()
                self.destroy()
                MembraneConnective(self.x, self.y)
        if self.lifetime <= 0:
            self.destroy()

class MembranePhospholipid(life.Bit):
    name = "MembranePhospholipid"

    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        pass

class MembraneConnective(life.Bit):
    name = "MembraneConnective"

    def __init__(self, x, y):
        super().__init__(x,y)

        self.timer = 0
        self.delay = 100

    def tick(self):
        self.timer -= 1
        if self.timer <= 0:
            closeMembrane = False
            for membraneBit in Membrane.lister:
                if life.distance(membraneBit, self) <= 10:
                    closeMembrane = True
            if not closeMembrane:
                self.destroy()
                Necrosis(self.x, self.y)

class Membrane(life.Bit):
    name = "Membrane"
    lister = []
    
    def __init__(self, x, y, attachments=[], lifetime=500):
        super().__init__(x,y)

        self.attachments = list(attachments)

        self.lonely = True

        self.lifetime = lifetime

        Membrane.lister.append(self)

    def destroy(self):
        super().destroy()
        if self in Membrane.lister:
            Membrane.lister.remove(self)

    def tick(self):
        self.lifetime -= 1
        
        if len(self.attachments) >= 2 and \
           isinstance(self.attachments[0], Membrane) and \
           isinstance(self.attachments[1], Membrane):
            ads = life.getAdjacentValids(self)
            if ads:
                oldx = self.x
                oldy = self.y

                self.moveto(random.choice(ads))

                moveback = False

                e = 0
                for abit in life.getAdjacentBits(self):
                    if abit.name == "FibrousGrowthTissue":
                        e += 1
                if e >= 2:
                    moveback = True
                    
                for attachment in self.attachments:
                    if life.distance(self, attachment) >= 3:
                        moveback = True

                if moveback:
                    self.moveto(oldx, oldy)
        else:
            self.destroy()
            FibrousGrowthTissue(self.x, self.y)

##        if self.lifetime <= 0:
##            self.destroy()
##            MembraneDouble(self.x, self.y)

    def attach(self, bit):
        if bit:
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
# q - destroy
# y - follow alongside fleshline, placing flesh along the way.
#      If lonely flesh is found, destroy and attach.

class Ribosome(life.Bit):
    name = "Ribosome"

    def __init__(self, x, y, rna, nutrition = 5):
        super().__init__(x,y)

        self.rna = rna
        self.rnaFrame = 0
        self.nutrition = nutrition
        self.heading = random.randrange(6)

        self.rnaShort = ""
        for char in self.rna:
            if char != 'y':
                self.rnaShort += char

        print(self.rnaShort)

        self.frustration = 0

        self.previousFlesh = None

    def turn(self, vec):
        self.heading += vec
        self.heading %= 6

    def moveAhead(self):
        return self.move(life.headingVector(self, self.heading))
    def moveBack(self):
        return self.move(life.headingVector(self, life.headingVectorReverse(self.heading)))
    
    def getFleshPos(self):
        fleshpos = life.headingVector(self, life.headingVectorReverse(self.heading))
        fleshpos = (fleshpos[0]+self.x, fleshpos[1]+self.y)
        return fleshpos

    def placeNewFlesh(self, fleshpos):
        newFlesh = Flesh(fleshpos[0], fleshpos[1], flexWait=len(self.rna)*2)
        if self.previousFlesh:
            newFlesh.attach(self.previousFlesh)
        self.previousFlesh = newFlesh

    def nextCodon(self):
        self.rnaFrame += 1

    def tick(self):
        try:
            codon = self.rna[self.rnaFrame]
        except:
            codon = ''
            
        if codon is 'f':
            if self.nutrition > 0:
                if self.moveAhead():
                    
                    fleshpos = self.getFleshPos()
                    
                    if not life.isBitHere(*fleshpos):
                        self.frustration = 0
                        self.nutrition -= 1
                        self.nextCodon()
                        self.placeNewFlesh(fleshpos)
                        
                else:
                    self.frustration += 1
                    if self.frustration >= 10:
                        self.turn(1)
                        
        elif codon is 'r':
            self.turn(1)
            self.nextCodon()
            
        elif codon is 'l':
            self.turn(-1)
            self.heading %= 6
            self.nextCodon()
            
        elif codon is 'q':
            self.destroy()
            
        elif codon is 'y':
            if self.nutrition > 0:
                abits = life.getAdjacentBits(self)
                for abit in abits:
                    if abit.name == "Flesh":
                        if abit.lonely and abit != self.previousFlesh:
                            self.frustration = 0
                            self.nutrition -= 1
                            self.destroy()
                            
                            finalFlesh = Flesh(self.x, self.y, flexWait=len(self.rnaShort)*1.1)
                            finalFlesh.attach(abit)

                if not self.destroyed:
                    if self.moveAhead():
                        abits = life.getAdjacentBits(self)
                        fleshes = 0
                        for abit in abits:
                            if abit.name == "Flesh" and abit != self.previousFlesh:
                                fleshes += 1
                        self.nextCodon()
                                
                        if fleshes:
                            self.placeNewFlesh(self.getFleshPos())
                        else:
                            self.moveBack()
                            self.turn(1)
                    else:
                        self.turn(1)
            
            
        else:
            self.nextCodon()

        for bit in NutrientAminoAcid.lister:
            if life.distance(bit, self) <= 20:
                bit.destroy()
                self.nutrition += 10

        
