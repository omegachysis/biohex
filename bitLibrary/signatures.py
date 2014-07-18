
import life

class SignatureGrowthTissueDecay(life.Bit):
    name = "SignatureGrowthTissueDecay"
    
    def __init__(self, x, y):
        super().__init__(x,y)

        life.Looper(self, self.randomWalk, 5)
        
    def tick(self):
        super().tick()
