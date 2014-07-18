
import life
import random
import bits

class HormoneCytoDissolve(life.Bit):
    name = "HormoneCytoDissolve"
    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        self.randomWalk()

        for membrane in self.lookout("MembraneCell", 10):
            if membrane.lookout("Cytosol", 3):
                membrane.destroy()
                if random.random() < .05:
                    self.destroy()
        for membrane in self.lookout("MembranePhospholipid", 10):
            if membrane.lookout("Cytosol", 3):
                membrane.destroy()
                bits.Phosphate(membrane.x, membrane.y)
                if random.random() < .05:
                    self.destroy()
