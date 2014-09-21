
from pygame import locals
import pygame

class UI(object):
    HEIGHT = 20
    STATUS_BACKGROUND_COLOR = (30,30,30)
    STATUS_TEXT_COLOR = (210,210,210)

    def __init__(self, engine):
        self.engine = engine
        self.pygameDisplay = engine.pygameDisplay

        self.font = pygame.freetype.Font("biohex/assets/consola.ttf", 13)
        self.fontIcon = pygame.freetype.Font("biohex/assets/fontawesome.ttf", 13)

        self.STATUS_BAR_TEXT_Y = self.engine.screen.height - UI.HEIGHT // 2

        self.statusHelperText = ""

    def _renderStatusValue(self, value, posPercent, rightAligned=False):
        valueSurface, valueRect = self.font.render(
            value, UI.STATUS_TEXT_COLOR, UI.STATUS_BACKGROUND_COLOR)

        valueRect.centery = self.STATUS_BAR_TEXT_Y
        if not rightAligned:
            valueRect.left = self.engine.screen.width * posPercent
        else:
            valueRect.right = self.engine.screen.width * posPercent

        self.engine.screen.surface.blit(valueSurface, valueRect)

    def render(self):
        # render a partially transparent black bar for the status bar
        self.engine.screen.surface.fill(UI.STATUS_BACKGROUND_COLOR,
                                        (0, self.engine.screen.height-UI.HEIGHT,
                                         self.engine.screen.width, UI.HEIGHT))

        wrenchSurface, wrenchRect = self.fontIcon.render(
            "\uF0AD", UI.STATUS_TEXT_COLOR, UI.STATUS_BACKGROUND_COLOR)
        wrenchRect.centery = self.STATUS_BAR_TEXT_Y
        wrenchRect.right = self.engine.screen.width - 5
        self.engine.screen.surface.blit(wrenchSurface, wrenchRect)

        self._renderStatusValue("TIME = " + str(self.engine.world.tickNumber),
                                0.01)
        self._renderStatusValue("\u03A3 ENTHALPY = " + str(self.engine.world.experiment.probeEnthalpy()),
                                0.10)
        self._renderStatusValue("\u03A3 ENTROPY = " + str(self.engine.world.experiment.probeEntropy()),
                                0.22)
        self._renderStatusValue("\u0394 THERMAL = " + str(self.engine.world.experiment.probeThermalEnergy()),
                                0.34)
        self._renderStatusValue("\u03BC TEMP = " + str(self.engine.world.experiment.probeTemperature()),
                                0.46)
        self._renderStatusValue("\u03A3 ATOMS = " + str(self.engine.world.experiment.probeAtoms()),
                                0.58)

        mousex, mousey = pygame.mouse.get_pos()
        if mousex > wrenchRect.left and mousex < wrenchRect.right and \
            mousey > self.engine.screen.height-UI.HEIGHT and \
            mousey < self.engine.screen.height:
            self.statusHelperText = "Toggle Toolbox (t)"
        else:
            self.statusHelperText = ""

        self._renderStatusValue(self.statusHelperText, 0.98, rightAligned = True)

