#!/usr/bin/env python3

import pygame
from pygame.locals import *

import traceback
import hexmech
import life

pygame.init()

def main():
    hexmech.setMetrics(
        width = 186,
        height = 161,
        t = 46)

    screen = Screen(1280, 720, False)
    world = World(screen, 10, 10)

    engine = Engine(screen, world)

    world.drawEmptyGrid()

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

    def start(self):
        self.mainloop()

class Screen(object):
    def __init__(self, width, height, fullscreen=False):

        self.canvas = None
        if fullscreen:
            self.canvas = pygame.display.set_mode((width, height), FULLSCREEN)
        else:
            self.canvas = pygame.display.set_mode((width, height))

    def blit(self, surface, position):
        self.canvas.blit(surface, position)

    def update(self):
        pygame.display.flip()

class World(life.World):
    def __init__(self, screen, width, height):
        super().__init__(width, height)
        
        self.bits = []

        self.screen = screen

        self._emptyBit = pygame.image.load("hexagon.png").convert()
        self._emptyBit.set_colorkey((255,255,255))

    def _drawEmpty(self, x, y):
        self.screen.blit(self._emptyBit, hexmech.coordsToPixels(x, y))

    def drawEmptyGrid(self):
        for y in range(self.height):
            for x in range(self.width):
                self._drawEmpty(x, y)

        self.screen.update()

if __name__ == "__main__":
    try:
        main()
    except:
        print(traceback.format_exc())
        input()
