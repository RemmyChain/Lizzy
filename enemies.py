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
        self.xpos1 = 40
        self.xpos2 = 85
        self.xpos3 = 100
        self.xpos4 = 145
        self.ypos1 = 70
        self.ypos2 = 70
        self.ypos3 = 70
        self.ypos4 = 70



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
        if hits:
            self.pos = self.oldpos
            if not self.reversed:
                self.reversed = True
            elif self.reversed:
                self.reversed = False
    def render(self):

        if not self.reversed:
            screen.blit(self.surf, self.rect)
        else:
            flipped = pygame.transform.flip(self.surf, True, False)
            screen.blit(flipped, self.rect)
        self.surf.fill((0, 0, 0))
    def update(self):
        if self.timer > 19:
            self.timer = 0
        self.edgedetect()
        self.move()
        self.platformcheck()
        self.hardblockscheck()
        self.animate()
        self.render()
        self.timer += 1

    def animate(self):
        self.frontpawfront()
        self.frontpawback()
        self.backpawfront()
        self.backpawback()
        self.surf.blit(kamakerpaw, (self.xpos1, self.ypos1))
        self.surf.blit(kamakerpaw, (self.xpos3, self.ypos3))
        self.surf.blit(kamakerbody, (50,15))
        self.surf.blit(kamakertail, (160,50))
        self.surf.blit(kamakerpaw, (self.xpos2, self.ypos2))
        self.surf.blit(kamakerpaw, (self.xpos4, self.ypos4))
        self.surf.blit(kamakerhead, (0,0))

    def frontpawfront(self):
        if self.timer < 10:
            self.xpos1 += 5
        elif self.timer >= 10 and self.timer < 15:
            self.xpos1 -= 5
            self.ypos1 -= 5
        elif self.timer >= 15:
            self.xpos1 -= 5
            self.ypos1 += 5

    def frontpawback(self):
        if self.timer < 5:
            self.xpos2 -= 5
            self.ypos2 -=5
        elif self.timer >= 5 and self.timer < 10:
            self.xpos2 -= 5
            self.ypos2 += 5
        elif self.timer >= 10:
            self.xpos2 += 5

    def backpawfront(self):
        if self.timer < 10:
            self.xpos3 += 5
        elif self.timer >= 10 and self.timer < 15:
            self.xpos3 -= 5
            self.ypos3 -= 5
        elif self.timer >= 15:
            self.xpos3 -= 5
            self.ypos3 += 5

    def backpawback(self):
        if self.timer < 5:
            self.xpos4 -= 5
            self.ypos4 -=5
        elif self.timer >= 5 and self.timer < 10:
            self.xpos4 -= 5
            self.ypos4 += 5
        elif self.timer >= 10:
            self.xpos4 += 5



