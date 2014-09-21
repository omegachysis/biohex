
import biohex

class Test(biohex.life.Bit):
    ATOMS = [0,0,0]
    ENTHALPY = 0
    ENTROPY = 0

    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        pass