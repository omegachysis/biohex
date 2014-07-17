#!/usr/bin/env python3

import pygame
from pygame.locals import *
import random

import traceback
import hexmech
import life
import bits

pygame.init()

def main():
    hexmech.setMetrics(
        width = 10, height = 10, t = 3)

    screen = Screen(1280, 720, fullscreen = False)
    world = World(screen, 180, 70)

    engine = Engine(screen, world)

    life.Bit.world = world

    rna = """
 """ + "f"*15 +'r'+'f'*25+'r'+'f'*5 + 'rfrf' + 'y'*50 + """q
"""

    bits.Ribosome(90, 35, rna, 0)
    
    for i in range(30):
        bits.NutrientAminoAcid(random.randrange(world.width), random.randrange(world.height))
    
    for i in range(5):
        bits.Oxidizer(random.randrange(world.width), random.randrange(world.height))
    for i in range(3):
        bits.Antioxidant(random.randrange(world.width), random.randrange(world.height))
    for i in range(3):
        bits.AcidStrong(random.randrange(world.width), random.randrange(world.height))

##    bits.MembranePhospholipid(90, 35)
##    bits.MembranePhospholipid(90, 37)

    screen.fill((0,0,0))

    world.drawEmptyGrid()
    world.drawAllBits()
    screen.update()

    engine.start()

class Engine(object):
    def __init__(self, screen, world):
        self.screen = screen
        self.world = world

        self.quitting = False

        self.running = False
        self.stepping = False

    def update(self):
        pass

    def mainloop(self):
        f = 1

        clock = pygame.time.Clock()
        
        while not self.quitting:
            self.stepping = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quitting = True
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.quitting = True
                    elif event.key == K_RETURN:
                        self.running = not self.running
                    elif event.key == K_SPACE:
                        self.stepping = True
                        f = 1
                        
            if self.running or self.stepping:
                f -= 1
                
                self.world.tick()         

                if f == 0:
                    self.world.drawEmptyUpdates()
                    self.world.drawDirtyBits()
                    self.screen.update()

                    f = 1

                clock.tick(20)
        
    def start(self):
        self.mainloop()

class Screen(object):
    def __init__(self, width, height, fullscreen=False, cursorLock=False):
        self.canvas = None
        if fullscreen:
            self.canvas = pygame.display.set_mode((width, height), FULLSCREEN)
        else:
            self.canvas = pygame.display.set_mode((width, height))

        pygame.event.set_grab(cursorLock)

    def fill(self, color):
        self.canvas.fill(color)

    def blit(self, surface, position):
        self.canvas.blit(surface, position)

    def update(self):
        pygame.display.flip()

class World(life.World):
    def __init__(self, screen, width, height):
        super().__init__(width, height)

        self._bitSurfaces = {}
        self._loadBitSurfaces()

        self.screen = screen

        self._emptyBit = pygame.image.load("bits/_empty.png").convert()
        self._emptyBit.set_colorkey((255,255,255))

    def _loadBitSurfaces(self):
        for bitName in life.bitList:
            surface = pygame.image.load("bits/" + bitName + ".png").convert()
            surface.set_colorkey((255,255,255))
            self._bitSurfaces[bitName] = surface

    def drawBit(self, bit):
        self.screen.blit(self._bitSurfaces[bit.name], hexmech.coordsToPixels(bit.x, bit.y))

    def drawAllBits(self):
        for bit in self.bits:
            self.drawBit(bit)

    def drawDirtyBits(self):
        for bit in self.dirtyBits:
            self.drawBit(bit)
        self.dirtyBits = []

    def drawEmpty(self, pos):
        self.screen.blit(self._emptyBit, hexmech.coordsToPixels(pos[0], pos[1]))

    def drawEmptyGrid(self):
        for y in range(self.height):
            for x in range(self.width):
                self.drawEmpty((x,y))
        self.updatePositions = []

    def drawEmptyUpdates(self):
        for updatePos in self.updatePositions:
            self.drawEmpty(updatePos)
        self.updatePositions = []

    def markDirty(self, bit):
        self.dirtyBits.append(bit)
    def unmarkDirty(self, bit):
        if bit in self.dirtyBits:
            self.dirtyBits.remove(bit)

    def markUpdate(self, x, y):
        self.updatePositions.append((x,y))

if __name__ == "__main__":
    try:
        main()
    except:
        pygame.quit()
        print(traceback.format_exc())
        input()
