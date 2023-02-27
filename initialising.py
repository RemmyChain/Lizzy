import pygame
from pygame import *
import os

pygame.init()

flags = FULLSCREEN | DOUBLEBUF
screen = pygame.display.set_mode((0, 0), flags, 16)
# screen = pygame.display.set_mode((600, 600))
backgroundimage = pygame.image.load(os.path.join('images', 'bg01.jpg')).convert()
screensize = screen.get_size()
background = pygame.transform.scale(backgroundimage, screensize)
running = True
vec = pygame.math.Vector2
# pygame.mouse.set_visible(False)
mousesurf = pygame.image.load(os.path.join('images', 'reticle.png'))
reticursor = pygame.cursors.Cursor((15,15), mousesurf)
pygame.mouse.set_cursor(reticursor)
font = pygame.font.SysFont("comicsansms", 20)
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

# sprite groups

allsprites = pygame.sprite.Group()
impacts = pygame.sprite.Group()
exits = pygame.sprite.Group()
flashy = pygame.sprite.Group()
platforms = pygame.sprite.Group()
hardblocks = pygame.sprite.Group()
enemies = pygame.sprite.Group()
hazards = pygame.sprite.Group()

depthlayer = pygame.image.load(os.path.join('images', 'depthlayer.png')).convert_alpha()

class depthbg(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__()
        self.pos = vec(coords)
        self.image = depthlayer
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
    def update(self):
        self.rect.center = self.pos
        screen.blit(self.image, self.rect)


depthcenter = vec(1300, 700)
depth = depthbg(depthcenter)
