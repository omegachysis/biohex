
import life
import random

class Test(life.Bit):
    name = "Test"
    def __init__(self, x, y):
        super().__init__(x,y)

class NutrientAminoAcid(life.Bit):
    name = "NutrientAminoAcid"
    
    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        self.randomWalk()

class Lipid(life.Bit):
    name = "Lipid"
    
    def __init__(self, x, y):
        super().__init__(x,y)

        life.Looper(self, self.randomWalk, 8)

    def tick(self):
        super().tick()

class HydratedLipid(life.Bit):
    name = "HydratedLipid"
    
    def __init__(self, x, y):
        super().__init__(x,y)

        life.Looper(self, self.randomWalk, 5)
        life.Looper(self, self.dehydrateLipids, 8)

    def dehydrateLipids(self):
        if self.lookout("Membrane", 7):
            membraneBit = random.choice(self.lookout("Membrane", 7))
            if random.random() < .20:
                membraneBit.destroy()
                #membraneBit.completelyUnattach()
            self.destroy()
            if random.random() < .80:
                Lipid(membraneBit.x-1, membraneBit.y)

    def tick(self):
        super().tick()

class Necrosis(life.Bit):
    name = "Necrosis"
    
    def __init__(self, x, y):
        super().__init__(x,y)

        life.Looper(self, self.randomWalk, 10)
        
    def tick(self):
        super().tick()

class StrongAcid(life.Bit):
    name = "StrongAcid"
    
    def __init__(self, x, y):
        super().__init__(x,y)

        life.Looper(self, self.randomWalk, 5)
        
    def tick(self):
        super().tick()
            
        for bit in self.getAdjBits():
            bit.destroy()
            if random.random()<.5:
                self.destroy()
                NeutralSolvent(self.x, self.y)

class NeutralSolvent(life.Bit):
    name = "NeutralSolvent"
    
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
        
        for bit in self.getAdjBits():
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
        for bit in self.lookout("Oxidizer", 15):
            bit.destroy()
            if random.random() < .10:
                self.destroy()
            
    def tick(self):
        super().tick()

class Lysosome(life.Bit):
    name = "Lysosome"

    def __init__(self, x, y):
        super().__init__(x,y)

        self.partner = None

    def tick(self):
        self.randomWalk()
        if self.partner:
            if self.distance(self.partner) >= 7:
                self.randomWalkTowards(self.partner) 
        else:
            if self.lookout("OrganelleMatrix", 7):
                self.partner = random.choice(self.lookout("OrganelleMatrix", 7))
                
        for bit in self.lookout("FibrousGrowthTissue", 2):
            bit.destroy()

class FibrousGrowthTissue(life.Bit):
    name = "FibrousGrowthTissue"

    def __init__(self, x, y, lifetime=100):
        super().__init__(x,y)

        self.lifetime = lifetime

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
                
        elif self.lifetime < 0:
            if self.lookout("MembraneConnective", 2):
                self.destroy()
                if random.random() < .10:
                    Lipid(self.x, self.y)

        for abit in self.getAdjBits():
            if abit.name == "MembraneCell" and abit.lifetime >= 100:
                self.destroy()
                abit.destroy()
                if random.random() < .10:
                    Lysosome(self.x, self.y)

class Cytoplasm(life.Bit):
    name = "Cytoplasm"

    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        pass

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

        self.timer = 50

    def tick(self):
        self.timer -= 1
        if self.timer == 0 or self.timer == -30:
            for adjtile in self.getAdjValids():
                MembraneDipole(*adjtile)

class MembranePermeable(life.Bit):
    name = "MembranePermeable"

    def __init__(self, x, y):
        super().__init__(x,y)

        self.timer =70

    def tick(self):
        self.timer -= 1

        if self.timer == 0:
            if self.lookout("FibrousGrowthTissue", 3):
                self.destroy()
                MembraneCell(self.x, self.y)
                for adjtile in self.getAdjValids():
                    MembraneCell(*adjtile)
            else:
                self.destroy()

class MembraneCell(life.Bit):
    name = "MembraneCell"

    def __init__(self, x, y):
        super().__init__(x,y)

        self.lifetime = 0

    def tick(self):
        self.lifetime += 1
        

class MembraneDipole(life.Bit):
    name = "MembraneDipole"

    def __init__(self, x, y):
        super().__init__(x,y)

        self.glueTimer = 5

    def tick(self):
        self.randomWalk()
        self.glueTimer -= 1
        if self.glueTimer <= 0:
            self.destroy()
            MembranePermeable(self.x, self.y)

class MembraneConnective(life.Bit):
    name = "MembraneConnective"
    
    def __init__(self, x, y):
        super().__init__(x,y)

        life.Looper(self, self.decay, 30)

    def decay(self):
        if not self.lookout("Membrane", 10):
            self.destroy()
            Necrosis(self.x, self.y)

        if self.lookout("Lipid", 8):
            self.destroy()
            convertbit = random.choice(self.lookout("Lipid", 8))
            convertbit.destroy()
            for i in range(3):
                HydratedLipid(convertbit.x + i - 1, convertbit.y)
            MembranePhospholipid(self.x, self.y)

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

    def completelyUnattach(self):
        for attachBit in self.attachments:
            if self in attachBit.attachments:
                attachBit.attachments.remove(self)
        self.attachments = []

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
# f - place GrowthTissue
# r - turn right
# l - turn left
# q - destroy
# y - follow alongside GrowthTissueline, placing GrowthTissue along the way.
#      If lonely GrowthTissue is found, destroy and attach.

class Ribosome(life.Bit):
    name = "Ribosome"

    def __init__(self, x, y, rna, nutrition = 5):
        super().__init__(x,y)

        self.rna = rna
        self.rnaFrame = 0
        self.nutrition = nutrition
        
        self.vector.angle = random.randrange(6)

        self.frustration = 0

        self.previousGrowthTissue = None
    
    def getGrowthTissuePos(self):
        GrowthTissuepos = self.vector.behind
        return GrowthTissuepos

    def placeNewGrowthTissue(self, GrowthTissuepos):
        newGrowthTissue = GrowthTissue(GrowthTissuepos[0], GrowthTissuepos[1], ribosomeDoping=self.rna.count("d."))
        if self.previousGrowthTissue:
            newGrowthTissue.attach(self.previousGrowthTissue)
        self.previousGrowthTissue = newGrowthTissue

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
                    
                    GrowthTissuepos = self.getGrowthTissuePos()
                    
                    if not life.getBit(*GrowthTissuepos):
                        self.frustration = 0
                        self.nutrition -= 1
                        self.nextCodon()
                        self.placeNewGrowthTissue(GrowthTissuepos)
                        
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
                    if abit.name == "GrowthTissue":
                        if abit.lonely and abit != self.previousGrowthTissue:
                            self.frustration = 0
                            self.nutrition -= 1
                            self.destroy()

                            finalGrowthTissue = GrowthTissue(self.x, self.y, ribosomeDoping=self.rna.count("d."))
                            finalGrowthTissue.attach(abit)

                            self.moveForward()
                            self.destroy()

                            Spindle(self.x, self.y)
                            
                            ads = True
                            while self.nutrition > 0 and ads:
                                ads = self.getAdjValids()
                                spot = random.choice(ads + [(self.x, self.y)])
                                Lipid(*spot)
                                self.nutrition -= 5
                            

                if not self.destroyed:
                    
                    if self.moveForward():
                        abits = self.getAdjBits()
                        GrowthTissuees = 0
                        for abit in abits:
                            if abit.name == "GrowthTissue" and abit != self.previousGrowthTissue:
                                GrowthTissuees += 1
                        self.nextCodon()
                                
                        if GrowthTissuees:
                            self.placeNewGrowthTissue(self.getGrowthTissuePos())
                        else:
                            self.moveBackward()
                            #Test(*self.vector.ahead)
                            self.vector.turnRight()
                                
                    else:
                        self.vector.turnRight()
            
            
        else:
            self.nextCodon()

        for bit in self.lookout("NutrientAminoAcid", 20):
            bit.destroy()
            self.nutrition += 10

class Spindle(life.Bit):
    name = "Spindle"
    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        if self.moveForward():
            abits = self.getAdjBits()
            GrowthTissuees = 0
            for abit in abits:
                if abit.name == "GrowthTissue":
                    GrowthTissuees += 1
                    
            if not GrowthTissuees or "FoldingMatrix" in [i.name for i in abits]:
                self.moveBackward()
                self.vector.turnRight()

            else:
                FoldingMatrix(*self.vector.behind)
                for abit in self.getAdjBits(self.vector.behind):
                    if abit.name == "GrowthTissue":
                        abit.triggeredFlexing = True
                    
        else:
            self.vector.turnRight()

class FoldingMatrix(life.Bit):
    name = "FoldingMatrix"
    def __init__(self, x, y):
        super().__init__(x,y)

        self.life = 6

    def tick(self):
        if self.life > 0:
            self.life -= 1
        else:
            self.destroy()

class OrganelleMatrix(life.Bit):
    name = "OrganelleMatrix"
    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        for adjbit in self.getAdjBits():
            if adjbit.name == "MembraneCell":
                adjbit.destroy()

class GrowthTissue(life.Bit):
    name = "GrowthTissue"
    
    def __init__(self, x, y, attachments=[], ribosomeDoping=5):
        super().__init__(x,y)

        self.attachments = list(attachments)

        self.lonely = True
        
        self.flexibility = ribosomeDoping
        self.stagnation = 0

        self.lifetime = 100

        self.triggeredFlexing = None
        self.flexingCountdown = 25

    def tick(self):
        if self.lonely:
            if self.triggeredFlexing:
                self.destroy()
                OrganelleMatrix(self.x, self.y)
        else:
            if self.triggeredFlexing:
                self.flexingCountdown -= 1
                if self.flexingCountdown <= 0:
                    if self.flexibility >= 0:
                        self.pullflex()
                        self.flexibility -= 1
                    else:
                        self.stagnation += 1

            if self.lifetime < self.stagnation:
                self.destroy()
                OrganelleMatrix(self.x, self.y)

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
        
