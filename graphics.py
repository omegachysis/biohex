#!/usr/bin/env python3

import pygame
from pygame.locals import *
import pygame.freetype

import random
import math

import traceback
import hexmech
import life
import bits

import experiment

pygame.init()
pygame.freetype.init()

class Engine(object):
    SCROLL_SPEED = 15
    
    def __init__(self, screen, world, ticksPerSecond=30):
        self.screen = screen
        self.world = world

        self.quitting = False

        self.running = False
        self.stepping = False
        self.rendering = True

        self.performanceModeIcon = pygame.image.load("assets/PerformanceModeIcon.png").convert_alpha()
        self.performanceModeIcon.fill((255,255,255,100), special_flags=BLEND_RGBA_MULT)
        self.performanceModeIconWidth, self.performanceModeIconHeight = self.performanceModeIcon.get_size()
        self.performanceModeIconPos = (screen.width//2-self.performanceModeIconWidth//2,
                                       screen.height//2-self.performanceModeIconHeight//2)

        self.ticksPerSecond = ticksPerSecond

    def update(self):
        pass

    def mainloop(self):
        clock = pygame.time.Clock()

        self.screen.update()

        keys = []
        
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
                        self.ticksPerSecond = 0
                    elif event.key == K_p:
                        self.rendering = not self.rendering
                        if self.rendering:
                            self.world.flush()
                        else:
                            self.screen.surface.fill((20,20,20), special_flags=BLEND_RGB_ADD)
                            self.screen.surface.blit(self.performanceModeIcon, self.performanceModeIconPos)
                            self.screen.renderText("Performance Mode Enabled", (128,0,0))
                            self.screen.update()
                            while not self.rendering:
                                self.world.tick()
                                for event in pygame.event.get():
                                    if event.type == QUIT:
                                        self.quitting = True
                                    elif event.type == KEYDOWN:
                                        if event.key == K_ESCAPE or event.key == K_p:
                                            self.rendering = True
                                            
                            self.world.flush()
                            self.rendering = True
                                        
                    elif event.key == K_a:
                        print("ATOMS IN EXPERIMENT: ", experiment.probeAtoms(self.world))
                    elif event.key == K_e:
                        print("ENTHALPY IN EXPERIMENT: ", experiment.probeEnthalpy(self.world))
                    elif event.key == K_r:
                        print("ENTROPY IN EXPERIMENT: ", experiment.probeEntropy(self.world))
          
            if self.running or self.stepping:
                self.world.tick()         

                if self.rendering:
                    self.world.drawEmptyUpdates()
                    self.world.drawDirtyBits()

                    self.screen.writeCanvas()
                    self.screen.update()

                    clock.tick(self.ticksPerSecond)

            else:
                keys = pygame.key.get_pressed()
                if keys[K_LEFT]:
                    self.screen.cameraX += Engine.SCROLL_SPEED
                if keys[K_RIGHT]:
                    self.screen.cameraX -= Engine.SCROLL_SPEED
                if keys[K_UP]:
                    self.screen.cameraY += Engine.SCROLL_SPEED
                if keys[K_DOWN]:
                    self.screen.cameraY -= Engine.SCROLL_SPEED

                self.screen.surface.fill((255,255,255))
                self.screen.writeCanvas()
                self.screen.update()

                clock.tick(60)
        
    def start(self):
        self.world.flush()
        self.mainloop()

class RenderLoadingScreen(object):
    def __init__(self, screen, numLoadingDots=40):
        self.mainIcon = pygame.image.load("assets/RenderIcon.png").convert_alpha()
        self.loadingDotIcon = pygame.image.load("assets/RenderLoadingDot.png").convert_alpha()
        self.screen = screen

        self.width, self.height = self.mainIcon.get_size()

        self.value = 0
        self.numLoadingDots = numLoadingDots
        self.percentageIncrements = 100 / numLoadingDots

        self.x = self.screen.width // 2
        self.y = self.screen.height // 2

        self.left = self.x - self.width // 2
        self.top = self.y - self.height // 2

        self.screen.surface.fill((80,80,80), special_flags=BLEND_RGB_ADD)
        self.drawMainIcon()

        self.screen.update()
        
    def update(self, loadingPercentage=0.00):
        value = loadingPercentage // self.percentageIncrements
        if value != self.value:
            self.value = value
            self.drawNewDot(self.value - 1)
            
    def drawMainIcon(self):
        self.screen.surface.blit(self.mainIcon, (self.left, self.top))
        self.screen.renderText(" "*50 + "Rendering Experiment" + " "*50, (0,0,128))
        self.screen.update()
        
    def drawNewDot(self, number):
        degrees = 360 / self.numLoadingDots * number
        radians = math.radians(degrees)
        buffer = 150
        
        dotX = math.sin(radians) * buffer + self.x
        dotY = -math.cos(radians) * buffer + self.y
        dotWidth, dotHeight = self.loadingDotIcon.get_size()

        dotLeft = dotX - dotWidth // 2
        dotTop = dotY - dotHeight // 2

        self.screen.surface.blit(self.loadingDotIcon, (dotLeft, dotTop))
        self.screen.update()

class Screen(object):
    def __init__(self, width, height, canvasSize, fullscreen=False, cursorLock=False):
        self.canvas = Canvas(canvasSize[0], canvasSize[1])
        self.surface = None
        if fullscreen:
            self.surface = pygame.display.set_mode((width, height), FULLSCREEN)
        else:
            self.surface = pygame.display.set_mode((width, height))

        self.surface.fill((255,255,255))

        pygame.event.set_grab(cursorLock)

        self.cameraX = 0
        self.cameraY = 0
        self.cameraScale = 0

        self.width = width
        self.height = height

        self.font = pygame.freetype.Font("assets/georgia.ttf", 30)

    def renderText(self, text, color = (0,0,0), x=0.50, y=0.75):
        surf, rect = self.font.render(text, color, (255,255,255))
        rect.centerx = self.width * x
        rect.centery = self.height * y
        self.surface.blit(surf, rect)

    def writeCanvas(self):
        self.surface.blit(self.canvas.surface, (self.cameraX, self.cameraY))

    def fill(self, color):
        self.canvas.fill(color)

    def blit(self, surface, position):
        self.canvas.blit(surface, position)

    def update(self):
        pygame.display.flip()

class Canvas(object):
    def __init__(self, width, height):
        self.surface = pygame.Surface((width, height))
    def blit(self, surface, position):
        self.surface.blit(surface, position)
    def fill(self, color):
        self.surface.fill(color)

class World(life.World):
    def __init__(self, screen, width, height, passErrors=False):
        super().__init__(width, height, passErrors)

        self._bitSurfaces = {}
        self._loadBitSurfaces()

        self.screen = screen
        self.loadingScreen = None

        self._emptyBit = pygame.image.load("bitGraphics/_empty.png").convert()
        self._emptyBit.set_colorkey((255,255,255))

    def _loadBitSurfaces(self):
        for bitName in life.bitList:
            surface = pygame.image.load("bitGraphics/" + bitName + ".png").convert()
            surface.set_colorkey((255,255,255))
            self._bitSurfaces[bitName] = surface

    def flush(self):
        self.loadingScreen = RenderLoadingScreen(self.screen)
        
        self.drawEmptyGrid()
        
        for bit in self.bits:
            self.drawBit(bit)

        self.updatePositions = []
        self.dirtyBits = []

        self.loadingScreen = None

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
        amount = self.height
        for y in range(self.height):
            self.loadingScreen.update(y/amount*100)
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
