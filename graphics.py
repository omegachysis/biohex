
import pygame
from pygame.locals import *

import hexagon
import hexmech

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

class World(object):
    def __init__(self, width, height):
        self.hexes = []
