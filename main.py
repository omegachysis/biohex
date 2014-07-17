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

    engine = graphics.Engine(screen, world)

    life.Bit.world = world

    rna = """
 """ + "f"*15 +'r'+'f'*25+'r'+'f'*5 + 'rfrf' + 'y'*50 + """q
"""

    bits.Ribosome(90, 35, rna, 0)
    
    for i in range(15):
        bits.NutrientAminoAcid(random.randrange(world.width), random.randrange(world.height))

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
