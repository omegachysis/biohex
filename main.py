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
    hexmech.setMetrics(
        width = 10, height = 10, t = 3)

    screen = graphics.Screen(1280, 720, fullscreen = False)
    world = graphics.World(screen, 180, 70)

    engine = graphics.Engine(screen, world, ticksPerSecond = 30)

    life.Bit.world = world

    random.seed(6)

    rna = " " + \
          'f'*8 +'r'+'f'*25+'r'+'f'*20 + 'r' + 'f'*20 + 'rf' + 'y'*500 + 'q' + \
          'd.'*15

    bits.Ribosome(90, 35, rna, 0)
    
    for i in range(35):
        bits.NutrientAminoAcid(random.randrange(60,110), random.randrange(20, 50))
    for i in range(5):
        bits.Oxidizer(random.randrange(world.width), random.randrange(world.height))
    for i in range(1):
        bits.StrongAcid(random.randrange(world.width), random.randrange(world.height))

    screen.fill((0,0,0))

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
