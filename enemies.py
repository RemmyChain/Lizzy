import pygame
from pygame import *
from initialising import *
from images import *
import math
from math import atan2, degrees, floor, sin, cos, radians
import random
import FX
from FX import *


class kamaker(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__()
        self.surf = pygame.Surface((200,100))
        self.surf.fill((0,0,0))
        self.surf.set_alpha(255)
        self.surf.set_colorkey((0,0,0))
        self.rect = self.surf.get_rect()

        self.pos = vec(coords)
        self.rect.midbottom = self.pos
        self.speed = -5
        self.fallspeed = 0
        self.health = 100
        self.grounded = False
        self.gravity = 2
        self.reversed = False
        self.timer = 0
        self.oldpos = self.pos

    def gethit(self):
        self.health -= 1
        if self.helth <= 0:
            self.kill()

    def move(self):
        self.oldpos = self.pos
        self.pos = vec(self.rect.midbottom)
        if not self.grounded:
            self.fallspeed += self.gravity
            if self.fallspeed > 20:
                self.fallspeed = 20
            self.pos.y += self.fallspeed

        if self.grounded and not self.reversed:
            self.pos.x += self.speed
        elif self.grounded and self.reversed:
            self.pos.x -= self.speed
        self.rect.midbottom = self.pos


    def edgedetect(self):

        if self.grounded:

            if not self.reversed:
                self.rect.centerx -= 200
            elif self.reversed:
                self.rect.centerx += 200
            hits = pygame.sprite.spritecollide(self, platforms, False)
            if not self.reversed:
                self.rect.centerx += 200
            elif self.reversed:
                self.rect.centerx -= 200
            if not hits:
                if self.reversed:
                    self.reversed = False
                    self.pos.x -= self.speed
                elif not self.reversed:
                    self.reversed = True
                    self.pos.x += self.speed



            # self.rect.midbottom = self.pos
    def platformcheck(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            for i in hits:
                if self.pos.y < i.rect.centery:
                    self.grounded = True
                    self.pos.y = i.rect.top + 1
                    self.rect.bottom = i.rect.top + 1
                else:
                    self.grounded = False
        else:
            self.grounded = False

    def hardblockscheck(self):
        hits = pygame.sprite.spritecollide(self, hardblocks, False)
    def render(self):
        if not self.reversed:
            screen.blit(self.surf, self.rect)
        else:
            flipped = pygame.transform.flip(self.surf, True, False)
            screen.blit(flipped, self.rect)
    def update(self):
        self.edgedetect()
        self.move()
        self.platformcheck()
        self.hardblockscheck()
        self.animate()
        self.render()
    def animate(self):
        self.surf.blit(kamakerpaw, (70, 70))
        self.surf.blit(kamakerpaw, (140, 70))
        self.surf.blit(kamakerbody, (50,15))
        self.surf.blit(kamakertail, (160,50))
        self.surf.blit(kamakerpaw, (50,70))
        self.surf.blit(kamakerpaw, (120, 70))
        self.surf.blit(kamakerhead, (0,0))
