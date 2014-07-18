
import life
import bits
import random

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
                bits.MembraneConnective(self.x, self.y)
        if self.lifetime <= 0:
            self.destroy()

class MembranePhospholipid(life.Bit):
    name = "MembranePhospholipid"

    # made when MembraneConnective has access
    # to a Lipid
    
    def __init__(self, x, y):
        super().__init__(x,y)

        self.timer = 50

    def tick(self):
        self.timer -= 1
        if self.timer == 0 or self.timer == -30:
            for adjtile in self.getAdjValids():
                bits.MembraneDipole(*adjtile)

class MembranePermeable(life.Bit):
    name = "MembranePermeable"

    # made by a MembraneDipole

    def __init__(self, x, y):
        super().__init__(x,y)

        self.timer =70

    def tick(self):
        self.timer -= 1

        if self.timer == 0:
            if self.lookout("FibrousGrowthTissue", 3):
                self.destroy()
                bits.MembraneCell(self.x, self.y)
                for adjtile in self.getAdjValids():
                    bits.MembraneCell(*adjtile)
            else:
                self.destroy()
        

class MembraneDipole(life.Bit):
    name = "MembraneDipole"

    # made by a MembranePhospholipid

    def __init__(self, x, y):
        super().__init__(x,y)

        self.glueTimer = 5

    def tick(self):
        self.randomWalk()
        self.glueTimer -= 1
        if self.glueTimer <= 0:
            self.destroy()
            bits.MembranePermeable(self.x, self.y)

class MembraneConnective(life.Bit):
    name = "MembraneConnective"
    
    def __init__(self, x, y):
        super().__init__(x,y)

        life.Looper(self, self.decay, 30)

    def decay(self):
        if not self.lookout("Membrane", 10):
            self.destroy()
            bits.Necrosis(self.x, self.y)

        if self.lookout("Lipid", 8):
            self.destroy()
            convertbit = random.choice(self.lookout("Lipid", 8))
            convertbit.destroy()
            for i in range(3):
                bits.HydratedLipid(convertbit.x + i - 1, convertbit.y)
            bits.MembranePhospholipid(self.x, self.y)

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
            bits.FibrousGrowthTissue(self.x, self.y)

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

class MembraneCell(life.Bit):
    name = "MembraneCell"

    def __init__(self, x, y):
        super().__init__(x,y)

        self.lifetime = 0
        self.solidification = 0
        self.passthruWait = 0

    def passthru(self, bit):
        self.vector.ahead = (bit.x, bit.y)
        if self.vector.angle != None:
            self.vector.reverse()
            self.vector.angle += random.randrange(3) - 1

            aheadBit = life.getBit(self.vector.ahead)
            if aheadBit:
                if aheadBit.name == "MembraneCell":
                    bit.passthru(aheadBit)
                    return True
            else:
                bit.moveto(self.vector.ahead)
                return True
       
        adjValids = self.getAdjValids()
        adjAlikes = [i for i in self.getAdjBits() if i.name == "MembraneCell"]

        if adjValids:
            bit.moveto(random.choice(adjValids))
            adjToBitButNotMe = [i for i in bit.getAdjValids() if i not in adjValids]
            if adjToBitButNotMe:
                bit.moveto(random.choice(adjToBitButNotMe))
        else:
            if adjAlikes:
                alike = random.choice(adjAlikes)
                alike.passthru(bit)

    def tick(self):
        self.lifetime += 1

        if self.passthruWait:
            self.passthruWait -= 1

        for abit in self.getAdjBits():
            if abit.name in ["Spindle", "Lipid"]:
                if not self.passthruWait:
                    self.passthru(abit)
