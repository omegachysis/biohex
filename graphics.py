
import pygame
from pygame.locals import *

import hexagon
import hexmech
import life

pygame.init()

def main():
    hexmech.setMetrics(
        width = 186,
        height = 161,
        t = 46)

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
