import pygame
from pygame import *

pygame.init()

flags = FULLSCREEN | DOUBLEBUF
screen = pygame.display.set_mode((0, 0), flags, 16)
background = pygame.image.load("bg01.jpg").convert()
running = True
vec = pygame.math.Vector2
pygame.mouse.set_visible(False)
font = pygame.font.SysFont("comicsansms", 20)
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

# sprite groups

allsprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
hardblocks = pygame.sprite.Group()
