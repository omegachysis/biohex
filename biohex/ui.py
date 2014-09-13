
import graphics
from pygame import locals

class UI(object):
    def __init__(self, engine):
        self.engine = engine
        self.pygameDisplay = engine.pygameDisplay

    def render(self):
        # render a partially transparent black bar for the status bar
        self.engine.screen.surface.fill((0,0,0),
                                            (0, self.engine.screen.height-20,
                                             self.engine.screen.width, 20))


