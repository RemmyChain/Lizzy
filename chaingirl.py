# This is the main program !

# imports

import pygame
from pygame import *
import sys

# setup stuff

from initialising import *

# loading various images

from images import *

# creating a game level

from levelgen import *

# Lizzy main class and ancilliaries

from lizzy import *

# Special effects

from fx import *

# enemies

from enemies import *

# main game loop

while running:
    screen.blit(background, (0, 0))
    depth.update()
    ref.update()
    for entity in allsprites:
        entity.update()
    liz.update()
    #    cursor.update()

    # this is for rendering some data on the screen for testing and debugging ets.

    flameystate = font.render("flamey behaviour: " + str(testflamey.state), True, ("black"))
    flameyground = font.render("flamey grounded: " + str(testflamey.grounded), True, ("black"))
    flameyobstruct = font.render("flamey obstructed: " + str(testflamey.obstructed), True, ("black"))
    terminal = font.render("angle: " + str(ref.angle), True, ("black"))
    frame = font.render("frame number: " + str(torso.frame), True, ("black"))
    rotangle = font.render("rotation angle: " + str(torso.anglecheck), True, ("black"))
    lizvelocity = font.render("Lizzy velocity: " + str(liz.vel), True, ("black"))
    lizposition = font.render("Lizzy position: " + str(liz.pos), True, ("black"))
    virtualcoords = font.render(
        "level virtual position: " + str(ref.virtualposition), True, ("black")
    )
    spritenumber = font.render(
        "number of sprites: " + str(len(allsprites)), True, ("black")
    )
    screen.blit(virtualcoords, (20, 20))
    # screen.blit(terminal, (20, 40))
    # screen.blit(lizvelocity, (20, 40))
    screen.blit(spritenumber, (20, 40))
    # screen.blit(flameystate, (20, 60))
    # screen.blit(flameyground, (20, 80))
    # screen.blit(flameyobstruct, (20, 100))

    pygame.display.update()

    # quit conditions

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    key = pygame.key.get_pressed()
    if key[K_ESCAPE]:
        running = False

    #    if ref.death == True:
    #        running = False

    pygame.time.Clock().tick(30)


pygame.quit()
sys.exit()
