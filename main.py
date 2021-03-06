#!/usr/bin/env python3

import pygame
import traceback
import random

import sys

from biohex import hexmech
from biohex import bits
from biohex import life
from biohex import graphics
from biohex import bitLibrary

pygame.init()

# command to run on initialization
INIT_STATEMENT = "runGraphics()"

# use python profiler
USE_PROFILER = False

def runGraphics():
    METRIC_WIDTH = 10       # width from very left to very right of hexagon
    METRIC_HEIGHT = 10      # height from very top to very bottom of hexagon
    METRIC_T = 3            # distance from upper left boundary 
                            #   corner to upper left corner of hexagon
    
    hexmech.setMetrics(
        width = 10, height = 10, t = 3)

    # search ring cache for all hexagon rings and load them into hexmech.rings
    hexmech.loadRings()

    # screen resolution.
    RES_WIDTH = 1280
    RES_HEIGHT = 720

    # world width and height in hexagons
    WORLD_WIDTH = 200
    WORLD_HEIGHT = 100
    
    FULLSCREEN = False

    # calculate size of on-screen canvas
    CANVAS_WIDTH = WORLD_WIDTH * (METRIC_WIDTH+METRIC_T*2) / 2
    CANVAS_HEIGHT = WORLD_HEIGHT * METRIC_HEIGHT

    screen = graphics.Screen(RES_WIDTH, RES_HEIGHT,
                             canvasSize = (CANVAS_WIDTH, CANVAS_HEIGHT), fullscreen = FULLSCREEN)
    world = graphics.World(screen, WORLD_WIDTH, WORLD_HEIGHT, passErrors = True)

    engine = graphics.Engine(screen, world, ticksPerSecond = 10)

    # important to do this after initialization
    life.Bit.world = world
    
    # random seed to start the world
    SEED = 1

    random.seed(SEED)

    # RNA for ribosome.  details in bitLibrary.organelles.Ribosome

    RNA = "Ag"     + chr(8)    + chr(15)    + "m" * 15  + "rrrg"    + chr(8)   + chr(15)   + "Q"

    DNA = bitLibrary.functions._convertRNA(RNA)
    print("DNA: ", DNA)

    bits.Ribosome(50, 40, DNA)

    world.setAmbientTemperature(25)

    for i in range(200):
        bits.Lipid(random.randrange(WORLD_WIDTH),
                   random.randrange(WORLD_HEIGHT))
    for i in range(150):
        bits.AminoAcid(random.randrange(WORLD_WIDTH),
                       random.randrange(WORLD_HEIGHT))
    for i in range(150):
        bits.Water(random.randrange(WORLD_WIDTH),
                       random.randrange(WORLD_HEIGHT))

    screen.fill((255,255,255))
    engine.start()

def main(profile = False):

    if profile:
        import cProfile
        cProfile.run(INIT_STATEMENT)
        input()
    else:
        exec(INIT_STATEMENT)

if __name__ == "__main__":
    try:
        main( USE_PROFILER )
    except:
        print(traceback.format_exc())
