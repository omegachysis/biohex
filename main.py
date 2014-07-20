#!/usr/bin/env python3

import pygame
import hexmech
import bits
import life
import graphics
import traceback
import random

import bitLibrary

pygame.init()

def runGraphics():
    METRIC_WIDTH = 10
    METRIC_HEIGHT = 10
    METRIC_T = 3
    
    hexmech.setMetrics(
        width = 10, height = 10, t = 3)

    RES_WIDTH = 1280
    RES_HEIGHT = 720

    WORLD_WIDTH = 400
    WORLD_HEIGHT = 200
    
    FULLSCREEN = False

    CANVAS_WIDTH = WORLD_WIDTH * (METRIC_WIDTH+METRIC_T*2) / 2
    CANVAS_HEIGHT = WORLD_HEIGHT * METRIC_HEIGHT

    screen = graphics.Screen(RES_WIDTH, RES_HEIGHT,
                             canvasSize = (CANVAS_WIDTH, CANVAS_HEIGHT), fullscreen = FULLSCREEN)
    world = graphics.World(screen, WORLD_WIDTH, WORLD_HEIGHT, passErrors = True)

    engine = graphics.Engine(screen, world, ticksPerSecond = 10)

    life.Bit.world = world

    random.seed(0)

    RNA = "Ag" + chr(10) + "mmmmmmmmmmmmmmmmmmmmmrrrg" + chr(10) + "Q"

    DNA = bitLibrary.functions._convertRNA(RNA)
    print("DNA: ", DNA)

    bits.Ribosome(WORLD_WIDTH//2, WORLD_HEIGHT//2, DNA)

    for i in range(150):
        bits.Lipid(random.randrange(WORLD_WIDTH),
                   random.randrange(WORLD_HEIGHT))
    for i in range(150):
        bits.AminoAcid(random.randrange(WORLD_WIDTH),
                       random.randrange(WORLD_HEIGHT))
    for i in range(150):
        bits.Water(random.randrange(WORLD_WIDTH),
                       random.randrange(WORLD_HEIGHT))

##    dna = """
##/w 100 /s if(self.signature('GrowthTissueDecay')>=10):self.goto('A'); /hCytoDissolve /q
##"""
##
##    rna = " " + \
##          'f'*15+'r'+'f'*15 + 'r' + 'f'*15 + 'r' + 'f'*15 + 'r' + 'f'*15 + 'r' + 'f'*10 + 'rf' + 'y'*50 + 'c' + \
##          'c' + 'c' + 'y'*50 + 'c' + 'y'*50 + 'c' + 'y'*400 + 'q' + \
##          'd'*10 + dna

    screen.fill((255,255,255))

    engine.start()

def runConsole():
    METRIC_WIDTH = 10
    METRIC_HEIGHT = 10
    METRIC_T = 3
    
    hexmech.setMetrics(
        width = 10, height = 10, t = 3)

    WORLD_WIDTH = 200
    WORLD_HEIGHT = 100

    world = life.World(WORLD_WIDTH, WORLD_HEIGHT)

    life.Bit.world = world

    random.seed(0)

    rna = " " + \
          'f'*15+'r'+'f'*15 + 'r' + 'f'*15 + 'r' + 'f'*15 + 'r' + 'f'*15 + 'r' + 'f'*10 + 'rf' + 'y'*50 + 'c' + \
          'c' + 'c' + 'y'*50 + 'c' + 'y'*50 + 'c' + 'y'*400 + 'q' + \
          'd'*10 + 'g/w100 /hCytoDissolve /w100 /q'

    bits.Ribosome(WORLD_WIDTH//2, WORLD_HEIGHT//2, rna, 0)
    
    for i in range(50):
        bits.AminoAcid(random.randrange(60,110), random.randrange(20, 50))
    for i in range(5):
        bits.Oxidizer(random.randrange(world.width), random.randrange(world.height))
    for i in range(1):
        bits.StrongAcid(random.randrange(world.width), random.randrange(world.height))

    printCounter = 0
    for i in range(1):
        if printCounter == 0:
            printCounter = 50
            print("ITERATION %-5d   BIT COUNT = %-5d" % (i, len(world.bits)))
        world.tick()
        printCounter -= 1

    input()

def main(profile = False):

    statement = "runGraphics()"

    if profile:
        import cProfile
        cProfile.run(statement)
        input()
    else:
        exec(statement)

if __name__ == "__main__":
    try:
        main()
    except:
        print(traceback.format_exc())
        input()
