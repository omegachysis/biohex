
import life
import random

class NutrientAminoAcid(life.Bit):
    name = "NutrientAminoAcid"
    
    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        self.randomWalk()

class NutrientLipid(life.Bit):
    name = "NutrientLipid"
    
    def __init__(self, x, y):
        super().__init__(x,y)

        life.Looper(self, self.randomWalk, 8)

    def tick(self):
        super().tick()

class Necrosis(life.Bit):
    name = "Necrosis"
    
    def __init__(self, x, y):
        super().__init__(x,y)

        life.Looper(self, self.randomWalk, 10)
        
    def tick(self):
        super().tick()

class AcidStrong(life.Bit):
    name = "AcidStrong"
    
    def __init__(self, x, y):
        super().__init__(x,y)

        life.Looper(self, self.randomWalk, 5)
        
    def tick(self):
        super().tick()
            
        for bit in self.getAdjBits():
            bit.destroy()
            if random.random()<.5:
                self.destroy()
                SolventNeutral(self.x, self.y)

class SolventNeutral(life.Bit):
    name = "SolventNeutral"
    
    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        self.randomWalk()

class Oxidizer(life.Bit):
    name = "Oxidizer"
    
    def __init__(self, x, y):
        super().__init__(x,y)

        life.Looper(self, self.randomWalk, 5)
        
    def tick(self):
        super().tick()
        
        for bit in life.getAdjBits(self):
            if bit.name is "Membrane":
                bit.destroy()
                self.destroy()
                for attachment in bit.attachments:
                    attachment.destroy()

class Antioxidant(life.Bit):
    name = "Antioxidant"
    
    def __init__(self, x, y):
        super().__init__(x,y)

        life.Looper(self, self.randomWalk, 3)

        life.Looper(self, self.antioxidize, 5)

    def antioxidize(self):
        once = False
        for oxibit in self.getlist("Oxidizer"):
            if life.distance(self, oxibit) <= 15:
                oxibit.destroy()
                once = True
        self.timer = self.delay
        if once:
            if random.random() < .3:
                self.destroy()
            
    def tick(self):
        super().tick()

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
        ads = self.getAdjValids()
        if ads and len(self.attachments) >= 2:
            oldX = self.x
            oldY = self.y
            
            self.moveto(random.choice(ads))

            adjs = self.getAdjValids()
            
            attachmentAdjs0 = self.attachments[0].getAdjValids()
            attachmentAdjs1 = self.attachments[1].getAdjValids()

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
            abits = self.getAdjBits()
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
            abits = self.getAdjBits()
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
    
    def __init__(self, x, y, lifetime=100):
        super().__init__(x,y)

        self.lifetime = lifetime

    def tick(self):
        self.lifetime -= 1
        for bit in self.getAdjBits():
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

        life.Looper(self, self.decay, 30)

    def decay(self):
        closeMembrane = False
        for membraneBit in self.getlist("Membrane"):
            if self.distance(membraneBit) <= 10:
                closeMembrane = True
        if not closeMembrane:
            self.destroy()
            Necrosis(self.x, self.y)

    def tick(self):
        super().tick()

class Membrane(life.Bit):
    name = "Membrane"
    
    def __init__(self, x, y, attachments=[], lifetime=500):
        super().__init__(x,y)

        self.attachments = list(attachments)
        self.lonely = True
        self.lifetime = lifetime

    def tick(self):
        self.lifetime -= 1
        
        if len(self.attachments) >= 2 and \
           isinstance(self.attachments[0], Membrane) and \
           isinstance(self.attachments[1], Membrane):
            ads = self.getAdjValids()
            if ads:
                oldx = self.x
                oldy = self.y

                self.moveto(random.choice(ads))

                moveback = False

                e = 0
                for abit in self.getAdjBits():
                    if abit.name == "FibrousGrowthTissue":
                        e += 1
                if e >= 2:
                    moveback = True
                    
                for attachment in self.attachments:
                    if self.distance(attachment) >= 3:
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
        
        self.vector.angle = random.randrange(6)

        self.rnaShort = ""
        for char in self.rna:
            if char != 'y':
                self.rnaShort += char

        self.frustration = 0

        self.previousFlesh = None
    
    def getFleshPos(self):
        fleshpos = self.vector.behind
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
                
                if self.moveForward():
                    
                    fleshpos = self.getFleshPos()
                    
                    if not life.getBit(*fleshpos):
                        self.frustration = 0
                        self.nutrition -= 1
                        self.nextCodon()
                        self.placeNewFlesh(fleshpos)
                        
                else:
                    self.frustration += 1
                    if self.frustration >= 10:
                        self.vector.turnRight()
                        
        elif codon is 'r':
            self.vector.turnRight()
            self.nextCodon()
            
        elif codon is 'l':
            self.vector.turnLeft()
            self.nextCodon()
            
        elif codon is 'q':
            self.destroy()
            
        elif codon is 'y':
            if self.nutrition > 0:
                abits = self.getAdjBits()
                for abit in abits:
                    if abit.name == "Flesh":
                        if abit.lonely and abit != self.previousFlesh:
                            self.frustration = 0
                            self.nutrition -= 1
                            self.destroy()

                            finalFlesh = Flesh(self.x, self.y, flexWait=len(self.rnaShort)*1.1)
                            finalFlesh.attach(abit)

                            self.moveForward()
                            self.destroy()

                            ads = True
                            while self.nutrition > 0 and ads:
                                ads = self.getAdjValids()
                                spot = random.choice(ads + [(self.x, self.y)])
                                NutrientLipid(*spot)
                                self.nutrition -= 5
                            

                if not self.destroyed:
                    
                    if self.moveForward():
                        abits = self.getAdjBits()
                        fleshes = 0
                        for abit in abits:
                            if abit.name == "Flesh" and abit != self.previousFlesh:
                                fleshes += 1
                        self.nextCodon()
                                
                        if fleshes:
                            self.placeNewFlesh(self.getFleshPos())
                        else:
                            self.moveBackward()
                            self.vector.turnRight()
                    else:
                        self.vector.turnRight()
            
            
        else:
            self.nextCodon()

        for bit in self.getlist("NutrientAminoAcid"):
            if self.distance(bit) <= 20:
                bit.destroy()
                self.nutrition += 10

        
