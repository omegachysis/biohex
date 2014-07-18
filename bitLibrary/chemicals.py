
import life
import random

class AminoAcid(life.Bit):
    name = "AminoAcid"
    
    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        self.randomWalk()

class Phosphate(life.Bit):
    name = "Phosphate"
    
    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        self.randomWalk()

class Cytosol(life.Bit):
    name = "Cytosol"
    
    def __init__(self, x, y):
        super().__init__(x,y)

        life.Looper(self, self.randomWalk, 7)

    def tick(self):
        super().tick()

class Lipid(life.Bit):
    name = "Lipid"
    
    def __init__(self, x, y):
        super().__init__(x,y)

        life.Looper(self, self.randomWalk, 4)

    def tick(self):
        super().tick()

class LipidSalt(life.Bit):
    name = "LipidSalt"
    
    def __init__(self, x, y):
        super().__init__(x,y)

        life.Looper(self, self.randomWalk, 3)

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
