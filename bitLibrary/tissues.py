
import life
import random
import bits

class GrowthTissue(life.Bit):
    name = "GrowthTissue"
    
    def __init__(self, x, y, attachments=[], ribosomeDoping=5):
        super().__init__(x,y)

        if not self.destroyed:
            self.attachments = list(attachments)

            self.lonely = True
            
            self.flexibility = ribosomeDoping
            self.stagnation = 0

            self.lifetime = 100

            self.age = 0

            self.spindleActivated = None
            self.flexingCountdown = 25

    def tick(self):
        self.age += 1
        
        if self.lonely:
            if self.spindleActivated:
                self.destroy()
                bits.MembraneMatrix(self.x, self.y)
        else:
            if self.spindleActivated:
                self.flexingCountdown -= 1
                if self.flexingCountdown <= 0:
                    if self.flexibility >= 0:
                        self.pullflex()
                        self.flexibility -= 1
                    else:
                        self.stagnation += 1

            if self.lifetime < self.stagnation:
                self.destroy()
                bits.MembraneMatrix(self.x, self.y)

        if self.age > 1000:
            self.destroy()
            if random.random() < .80:
                bits.Necrosis(self.x, self.y)
            else:
                bits.SignatureGrowthTissueDecay(self.x, self.y)

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

                membrane0 = bits.Membrane(*adj0)
                membrane1 = bits.Membrane(*adj1)

                self.flexibility -= 1
                if self.flexibility <= 0:
                    self.destroy()
                    membraneCentral = bits.Membrane(self.x, self.y)
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
                    bits.FibrousGrowthTissue(self.x, self.y)
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
                bits.MembraneDouble(self.x, self.y)
                
        elif self.lifetime < 0:
            if self.lookout("MembraneConnective", 2):
                self.destroy()
                if random.random() < .20:
                    if random.random() < .50:
                        bits.Lipid(self.x, self.y)
                    else:
                        bits.LipidSalt(self.x, self.y)

        for abit in self.getAdjBits():
            if abit.name == "MembraneCell" and abit.lifetime >= 100:
                self.destroy()
                abit.destroy()
                if random.random() < .10:
                    bits.Lysosome(self.x, self.y)

        if self.lifetime <= -500:
            self.destroy()
            if random.random() < .40:
                bits.Necrosis(self.x, self.y)
            else:
                bits.Lipid(self.x, self.y)
                
class Cytoplasm(life.Bit):
    name = "Cytoplasm"

    def __init__(self, x, y):
        super().__init__(x,y)

        looper = life.Looper(self, self.walk, 3)
        looper.timer = 20

        self.firstWalk = True

    def release(self):
        self.destroy()
        bits.Cytosol(self.x, self.y)
        for adjtile in self.getAdjValids():
            bits.Cytosol(*adjtile)
            for subadjtile in self.getAdjValids(adjtile):
                bits.Cytosol(*subadjtile)

    def walk(self):
        oldx = self.x
        oldy = self.y
        self.randomWalk()
        if self.firstWalk:
            self.firstWalk = False
            bits.GrowthTissue(oldx, oldy, [], 2)

    def tick(self):
        super().tick()
            
        if self.lookout("Lysosome", 10):
            self.release()
