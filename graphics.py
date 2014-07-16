#!/usr/bin/env python3

import pygame
from pygame.locals import *

import traceback
import hexmech
import life

pygame.init()

def main():
    hexmech.setMetrics(
        width = 37, height = 32, t = 9)

    screen = Screen(1280, 720, fullscreen = False)
    world = World(screen, 30, 20)

    engine = Engine(screen, world)

    life.Bit.world = world
    
    for i in range(15):
        life.Walker(0, i)

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

    def update(self):
        pass

    def mainloop(self):
        while not self.quitting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quitting = True
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.quitting = True
                        
                    elif event.key == K_SPACE:
                        self.world.tick()
                        self.world.drawEmptyGrid()
                        self.world.drawAllBits()
                        self.screen.update()

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

    def _drawEmpty(self, x, y):
        self.screen.blit(self._emptyBit, hexmech.coordsToPixels(x, y))

    def drawEmptyGrid(self):
        for y in range(self.height):
            for x in range(self.width):
                self._drawEmpty(x, y)

if __name__ == "__main__":
    try:
        main()
    except:
        pygame.quit()
        print(traceback.format_exc())
        input()
