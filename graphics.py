#!/usr/bin/env python3

import pygame
from pygame.locals import *
import random

import traceback
import hexmech
import life
import bits

pygame.init()

class Engine(object):
    def __init__(self, screen, world, ticksPerSecond=30):
        self.screen = screen
        self.world = world

        self.quitting = False

        self.running = False
        self.stepping = False

        self.ticksPerSecond = ticksPerSecond

    def update(self):
        pass

    def mainloop(self):
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
                    elif event.key == K_1:
                        self.ticksPerSecond = 10
                    elif event.key == K_2:
                        self.ticksPerSecond = 20
                    elif event.key == K_3:
                        self.ticksPerSecond = 30
                    elif event.key == K_4:
                        self.ticksPerSecond = 40
                        
            if self.running or self.stepping:
                
                self.world.tick()         

                self.world.drawEmptyUpdates()
                self.world.drawDirtyBits()
                self.screen.update()

                clock.tick(self.ticksPerSecond)
        
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
