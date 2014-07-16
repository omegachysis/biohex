
class Hexagon(object):

    # width and height of the entire hexagon bounds
    METRIC_WIDTH = 186
    METRIC_HEIGHT = 161
    # horizontal distance from upper left corner to high left point
    #  of the hexagon
    METRIC_T = 46

    MS = int(METRIC_WIDTH - 2 * METRIC_T)
    MR = int(METRIC_HEIGHT / 2)
    MH = int(METRIC_HEIGHT)
    MT = int(METRIC_T)
    
    def __init__(self, xgrid, ygrid):
        self.x = xgrid
        self.y = ygrid
