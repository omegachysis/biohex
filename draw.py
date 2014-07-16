
import pygame
from pygame.locals import *

pygame.init()

class Screen(object):
    def __init__(self, width, height, fullscreen=False):

        self.canvas = None
        if fullscreen:
            self.canvas = pygame.display.set_mode((width, height), FULLSCREEN)
        else:
            self.canvas = pygame.display.set_mode((width, height))

    def draw(self, surface, position):
        self.canvas.blit(surface, position)

    def update(self):
        pygame.display.flip()

