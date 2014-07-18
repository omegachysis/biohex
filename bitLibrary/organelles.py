
import life
import random
import bits
import traceback

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
            if self.lookout("MembraneMatrix", 7):
                self.partner = random.choice(self.lookout("MembraneMatrix", 7))
                
        for bit in self.lookout("FibrousGrowthTissue", 2):
            bit.destroy()
            if random.random() < .05:
                self.destroy()
        for bit in self.lookout("Necrosis", 3):
            bit.destroy()
            if random.random() < .05:
                self.destroy()

# rna
#---------------
# f - place GrowthTissue
# r - turn right
# l - turn left
# q - destroy
# y - follow alongside GrowthTissueline, placing GrowthTissue along the way.
#      If lonely GrowthTissue is found, destroy and attach.
# c - cytoplasm
# d - add them anywhere to signal the ribosome to dope the growth tissue to
#    make it flex further
# g - signal the start of dna genetic code.  make this the last rna letter you use.

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

    def placeNewGrowthTissue(self, GrowthTissuepos):
        newGrowthTissue = bits.GrowthTissue(GrowthTissuepos[0], GrowthTissuepos[1], ribosomeDoping=self.rna.count("d"))
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
                    
                    GrowthTissuepos = self.vector.behind
                    
                    if not life.getBit(*GrowthTissuepos):
                        self.frustration = 0
                        self.nutrition -= 1
                        self.nextCodon()
                        self.placeNewGrowthTissue(GrowthTissuepos)
                        
                else:
                    self.frustration += 1
                    if self.frustration >= 10:
                        self.vector.turnRight()

        elif codon is 'c':
            if self.moveForward():
                if not life.getBit(*self.vector.behind):
                    bits.Cytoplasm(*self.vector.behind)
                    self.nextCodon()
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

                            finalGrowthTissue = bits.GrowthTissue(self.x, self.y, ribosomeDoping=self.rna.count("d"))
                            finalGrowthTissue.attach(abit)

                            self.moveForward()
                            self.destroy()

                            Spindle(self.x, self.y, self.rna)
                            
                            ads = True
                            while self.nutrition > 0 and ads:
                                ads = self.getAdjValids()
                                spot = random.choice(ads + [(self.x, self.y)])
                                bits.Lipid(*spot)
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
                            self.placeNewGrowthTissue(self.vector.behind)
                        else:
                            self.moveBackward()
                            #Test(*self.vector.ahead)
                            self.vector.turnRight()
                                
                    else:
                        self.vector.turnRight()
            
            
        else:
            self.nextCodon()

        for bit in self.lookout("AminoAcid", 20):
            bit.destroy()
            self.nutrition += 10

class Spindle(life.Bit):
    name = "Spindle"
    def __init__(self, x, y, rna=""):
        super().__init__(x,y)

        self.initialDelay = 50

        self.stagnation = 0
        self.frustration = 0

        self.maturing = False
        self.maturingStage = 0

        self.looper = life.Looper(self, self.findCytosol, 10)
        self.looper.pause()

        self.rna = rna
        self.dna = rna[rna.index('g'):]

    def findCytosol(self):
        if self.stagnation >= 20:
            self.randomWalkTowardsType("Cytosol", 10)
        if "Cytosol" in [i.name for i in self.getAdjBits()]:
            self.mature()

    def mature(self):
        if self.maturingStage < 10:
            self.maturingStage += 1
        else:
            self.destroy()
            Nucleocyte(self.x, self.y, self.dna)

    def tick(self):
        super().tick()
        
        self.initialDelay -= 1
        if self.initialDelay <= 0 and not self.maturing:
            if self.moveForward():
                abits = self.getAdjBits()
                GrowthTissuees = 0
                for abit in abits:
                    if abit.name == "GrowthTissue":
                        GrowthTissuees += 1
                        
                if not GrowthTissuees or "FoldingMatrix" in [i.name for i in abits]:
                    self.moveBackward()
                    self.vector.turnRight()
                    self.stagnation += 1

                else:
                    self.stagnation = 0
                    self.frustration = 0
                    FoldingMatrix(*self.vector.behind)
                    for abit in self.getAdjBits(self.vector.behind):
                        if abit.name in ["GrowthTissue"]:
                            abit.spindleActivated = True
                        
            else:
                self.frustration += 1
                if self.frustration >= 3:
                    self.stagnation += 1
                    self.vector.turnRight()
                    
        if self.stagnation == 20:
            self.looper.start()
            self.maturing = True
            
class FoldingMatrix(life.Bit):
    name = "FoldingMatrix"
    def __init__(self, x, y):
        super().__init__(x,y)

        self.life = 13

    def tick(self):
        if self.life > 0:
            self.life -= 1
        else:
            self.destroy()

class MembraneMatrix(life.Bit):
    name = "MembraneMatrix"
    def __init__(self, x, y):
        super().__init__(x,y)

    def tick(self):
        for adjbit in self.getAdjBits():
            if adjbit.name == "MembraneCell":
                adjbit.destroy()

class Nucleocyte(life.Bit):
    name = "Nucleocyte"
    def __init__(self, x, y, dna = ""):
        super().__init__(x,y)

        life.Looper(self, self.spread, 20).timer = 20

        self.energy = 1
        self.nucleoli = []
        self.dna = dna

    def spread(self):
        self.energy -= 1
        if self.energy >= 0:
            for adjtile in self.getAdjValids():
                self.nucleoli.append(Nucleolus(adjtile[0], adjtile[1]))
                
                if not self.destroyed:
                    self.destroy()
                    bits.Nucleus(self.x, self.y, self.nucleoli, self.dna)

    def tick(self):
        super().tick()

class Nucleolus(life.Bit):
    name = "Nucleolus"
    def __init__(self, x, y):
        super().__init__(x,y)

        self.nucleus = None

    def sendHormone(self, name):
        for adjtile in self.getAdjValids():
            eval("bits." + name + "(*adjtile)")

    def detectSignatureBit(self, signatureBit):
        codeName = signatureBit.name.replace("Signature", "")
        if self.nucleus:
            if codeName in self.nucleus.signaturesDetected:
                self.nucleus.signaturesDetected[codeName] += 1
            else:
                self.nucleus.signaturesDetected[codeName] = 1

    def tick(self):
        if self.lookout("SignatureGrowthTissueDecay", 7):
            for sbit in self.lookout("SignatureGrowthTissueDecay", 7):
                sbit.destroy()
                self.detectSignatureBit(sbit)

class Nucleus(life.Bit):
    name = "Nucleus"
    def __init__(self, x, y, nucleoli=[], dna=""):
        super().__init__(x,y)

        self.nucleoli = nucleoli

        for nuc in self.nucleoli:
            nuc.nucleus = self
            print("SHARED NUCLEOLUS MEMORY ENGAGED")

        self.actionConfirmed = 0

        self.signaturesDetected = {}

        self.labels = {}

        self.dna = dna
        self.dnaFrame = 0

        self.waiting = 0
        self.done = False

        dna = dna.replace(" ", "")
        while True:
            labelIndex = dna.find('/l')
            if labelIndex != -1:
                labelName = ""
                i = labelIndex
                while True:
                    i += 1
                    if dna[i] != "/":
                        labelName += dna[i]
                    else:
                        break
                dna = dna[i:]
                self.labels[labelName[1:]] = labelIndex
            else:
                break

    def readNextAction(self):
        action = ""
        reading = False
        for char in self.dna[self.dnaFrame:]:
            if char == "/":
                if not reading:
                    reading = True
                else:
                    break
            elif char == " " or char == "\n":
                pass
            elif char == "_":
                action += " "
            elif char == "@":
                action += "\n"
            else:
                if reading:
                    action += char
            self.dnaFrame += 1
        self.dnaFrame -= 1
        return action

    def goto(self, labelName):
        if labelName in self.labels:
            self.dnaFrame = self.labels[labelName]

    def doNextAction(self):
        action = self.readNextAction()
        print("NEXT ACTION", action)
        lettercode = action[0]
        actioncode = action[1:]
        if lettercode == 'w':
            self.waiting = int(action[1:])
        elif lettercode == 'h':
            hormoneName = "Hormone" + action[1:]
            self.sendHormone(hormoneName)
        elif lettercode == 's':
            try:
                exec(actioncode)
            except:
                print("DNA SCRIPTING ERROR:")
                print(traceback.format_exc())
        elif lettercode == 'l':
            pass
        elif lettercode == 'q':
            self.done = True

    def sendHormone(self, name):
        self.actionConfirmed = 0
        for nuc in self.nucleoli:
            nuc.sendHormone(name)

    def signature(self, name):
        if name not in self.signaturesDetected:
            self.signaturesDetected[name] = 0
        return self.signaturesDetected[name]

    def tick(self):
        if not self.done:
            if not self.waiting:
                self.doNextAction()
            else:
                self.waiting -= 1
