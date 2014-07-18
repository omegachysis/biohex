#!/usr/bin/env python3

import pygame
import hexmech
import bits
import life
import graphics
import traceback
import random

pygame.init()

def main():
    METRIC_WIDTH = 10
    METRIC_HEIGHT = 10
    METRIC_T = 3
    
    hexmech.setMetrics(
        width = 10, height = 10, t = 3)

    RES_WIDTH = 1920
    RES_HEIGHT = 1080

    WORLD_WIDTH = int(RES_WIDTH / (METRIC_WIDTH / 2))
    WORLD_HEIGHT = RES_HEIGHT // METRIC_HEIGHT

    screen = graphics.Screen(RES_WIDTH, RES_HEIGHT, fullscreen = False)
    world = graphics.World(screen, WORLD_WIDTH, WORLD_HEIGHT)

    engine = graphics.Engine(screen, world, ticksPerSecond = 10)

    life.Bit.world = world

    random.seed(101)

    rna = " " + \
          'f'*15+'r'+'f'*15 + 'r' + 'f'*15 + 'r' + 'f'*15 + 'r' + 'f'*15 + 'r' + 'f'*10 + 'rf' + 'y'*50 + 'c' + \
          'c' + 'c' + 'y'*50 + 'c' + 'y'*50 + 'c' + 'y'*400 + 'q' + \
          'd.'*10

    bits.Ribosome(90, 35, rna, 0)
    
    for i in range(35):
        bits.NutrientAminoAcid(random.randrange(60,110), random.randrange(20, 50))
##    for i in range(5):
##        bits.Oxidizer(random.randrange(world.width), random.randrange(world.height))
##    for i in range(1):
##        bits.StrongAcid(random.randrange(world.width), random.randrange(world.height))

    screen.fill((255,255,255))

    world.drawEmptyGrid()
    world.drawAllBits()
    screen.update()

    engine.start()

if __name__ == "__main__":
    try:
        main()
    except:
        pygame.quit()
        print(traceback.format_exc())
        input()
