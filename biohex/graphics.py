import pygame
from pygame.locals import *
import pygame.freetype

import random
import math

import traceback
import hexmech
import life
import bits
import ui

import experiment

pygame.init()
pygame.freetype.init()

class Engine(object):
    """Highest level pygame class to handle all program events."""

    SCROLL_SPEED = 15 # how fast the virtual screen camera moves on arrow presses
    
    def __init__(self, screen, world, ticksPerSecond=30):
        """
        Initialize a new world engine.  Start with a screen 
        and world already created.  'ticksPerSecond' defines
        how many ticks occur on autorun per second.
        """

        self.pygameDisplay = pygame.display

        self.screen = screen
        self.world = world
        self.ui = ui.UI(self)

        self.quitting = False

        self.running = False        # auto-run enabled
        self.stepping = False       # in a mode where only one tick is to occur and then a pause
        self.rendering = True       # whether or not every tick is to be rendered

        # load the icon that shows on the screen when entering performance mode ('p')
        self.performanceModeIcon = pygame.image.load("assets/PerformanceModeIcon.png").convert_alpha()
        self.performanceModeIcon.fill((255,255,255,100), special_flags=BLEND_RGBA_MULT)
        self.performanceModeIconWidth, self.performanceModeIconHeight = self.performanceModeIcon.get_size()
        self.performanceModeIconPos = (screen.width//2-self.performanceModeIconWidth//2,
                                       screen.height//2-self.performanceModeIconHeight//2)

        self.ticksPerSecond = ticksPerSecond

    def update(self):
        pass

    def quit(self):
        self.quitting = True

    def mainloop(self):
        # create master time-keeper
        clock = pygame.time.Clock()

        # refresh the SDL screen surface
        self.screen.update()

        # will store keyboard keys later in mainloop
        keys = []
        
        while not self.quitting:
            self.stepping = False

            for event in pygame.event.get():

                if event.type == QUIT:
                    self.quit()

                # a key has been pressed down on this frame
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.quit()
                    elif event.key == K_RETURN:
                        # RETURN key toggles autorun
                        self.running = not self.running
                    elif event.key == K_SPACE:
                        # SPACEBAR steps through individual ticks
                        self.stepping = True
                    elif event.key == K_1:
                        # 1 key sets to 10 ticks per second
                        self.ticksPerSecond = 10
                    elif event.key == K_2:
                        # 2 key sets to 20 ticks per second
                        self.ticksPerSecond = 20
                    elif event.key == K_3:
                        # 3 key sets to 30 ticks per second
                        self.ticksPerSecond = 30
                    elif event.key == K_4:
                        # 4 key removes the tick limit, rendering and ticking as fast as possible
                        self.ticksPerSecond = 0

                    elif event.key == K_p:
                        # pressing the 'P' key goes into performance mode,
                        # where only world calculations are made and no
                        # rendering is done

                        self.rendering = not self.rendering

                        if self.rendering:
                            # coming out of performance mode,
                            # re-render the entire world
                            self.world.flush()
                        else:
                            # going into performance mode
                            # render graphics for that, now

                            # brighten the whole screen by 20 pixels in each color
                            self.screen.surface.fill((20,20,20), special_flags=BLEND_RGB_ADD)
                            # render mode image icon with text label
                            self.screen.surface.blit(self.performanceModeIcon, self.performanceModeIconPos)
                            self.screen.renderText("Performance Mode Enabled", (128,0,0))
                            self.screen.update()
                            while not self.rendering:
                                self.world.tick()
                                for event in pygame.event.get():
                                    if event.type == QUIT:
                                        self.quit()
                                    elif event.type == KEYDOWN:
                                        if event.key == K_ESCAPE or event.key == K_p:
                                            self.rendering = True
                            # render the whole world, this can take a while   
                            self.world.flush()
                            self.ui.render()
                            self.rendering = True
                                        
                    elif event.key == K_a: # display all counts of atoms in console window
                        print("ATOMS IN EXPERIMENT: ", self.world.experiment.probeAtoms())
                    elif event.key == K_e: # display total enthalpy in console window
                        print("ENTHALPY IN EXPERIMENT: ", self.world.experiment.probeEnthalpy())
                    elif event.key == K_r: # display total entropy in console window
                        print("ENTROPY IN EXPERIMENT: ", self.world.experiment.probeEntropy())
          
            if self.running or self.stepping:
                # run a simulation tick
                self.world.tick()         

                if self.rendering:
                    # redraw tiles that have been made empty
                    self.world.drawEmptyUpdates()
                    # draw bits that have changed or moved
                    self.world.drawDirtyBits()

                    # draw the final screen canvas to the pygame display
                    self.screen.writeCanvas()

                    # draw the ui over all that
                    self.ui.render()

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

                self.ui.render()

                self.screen.update()

                clock.tick(60)

        pygame.quit()
        
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
