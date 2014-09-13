
import graphics
from pygame import locals
import pygame

class UI(object):
    HEIGHT = 20
    STATUS_BACKGROUND_COLOR = (30,30,30)
    STATUS_TEXT_COLOR = (210,210,210)

    def __init__(self, engine):
        self.engine = engine
        self.pygameDisplay = engine.pygameDisplay

        self.font = pygame.freetype.Font("assets/consola.ttf", 15)

        self.statusBarTextY = self.engine.screen.height - UI.HEIGHT // 2

    def _renderStatusValue(self, value, posPercent):
        valueSurface, valueRect = self.font.render(
            value, UI.STATUS_TEXT_COLOR, UI.STATUS_BACKGROUND_COLOR)

        valueRect.centery = self.statusBarTextY
        valueRect.centerx = self.engine.screen.width * posPercent

        self.engine.screen.surface.blit(valueSurface, valueRect)

    def render(self):
        # render a partially transparent black bar for the status bar
        self.engine.screen.surface.fill(UI.STATUS_BACKGROUND_COLOR,
                                        (0, self.engine.screen.height-UI.HEIGHT,
                                         self.engine.screen.width, UI.HEIGHT))

        self._renderStatusValue("\u03A3 ENTHALPY = " + str(self.engine.world.experiment.probeEnthalpy()),
                                0.30)
        self._renderStatusValue("\u03A3 ENTROPY = " + str(self.engine.world.experiment.probeEntropy()),
                                0.70)




