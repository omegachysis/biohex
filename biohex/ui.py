
import graphics
from pygame import locals
import pygame

class UI(object):
    HEIGHT = 30

    def __init__(self, engine):
        self.engine = engine
        self.pygameDisplay = engine.pygameDisplay

        self.font = pygame.freetype.Font("assets/consola.ttf", 15)

        self.statusBarTextY = self.engine.screen.height - UI.HEIGHT // 2

    def _renderStatusValue(self, value, posPercent):
        valueSurface, valueRect = self.font.render(
            value, (255,255,255), (0,0,0))

        valueRect.centery = self.statusBarTextY
        valueRect.centerx = self.engine.screen.height * posPercent

        self.engine.screen.surface.blit(valueSurface, valueRect)

    def render(self):
        # render a partially transparent black bar for the status bar
        self.engine.screen.surface.fill((0,0,0),
                                            (0, self.engine.screen.height-UI.HEIGHT,
                                             self.engine.screen.width, UI.HEIGHT))

        self._renderStatusValue("\u03A3 ENTHALPY = " + str(self.engine.world.experiment.probeEnthalpy()),
                                0.20)





