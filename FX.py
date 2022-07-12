import pygame
from pygame import *
from initialising import *
from images import *
import math
from math import atan2, degrees, floor, sin, cos, radians
import random

class particle():
    def __init__(self, xpos, ypos, xvel, yvel, xacc, yacc, size, dsize, color, surface):
        self.xpos = xpos
        self.ypos = ypos
        self.xvel = xvel
        self.yvel = yvel
        self.xacc = xacc
        self.yacc = yacc
        self.size = size
        self.dsize = dsize
        self.color = color
        self.surface = surface
        self.center = vec(self.xpos, self.ypos)
    def draw(self):
        pygame.draw.circle(self.surface, self.color, self.center, self.size, 0)
        self.xvel += self.xacc
        self.yvel += self.yacc
        if self.yvel > 0:
            self.yvel = random.randrange(-1,1)
        # self.xpos += self.xvel
        # self.ypos += self.ypos
        self.size += self.dsize
        self.center.x += self.xvel
        self.center.y += self.yvel



class spriticle(pygame.sprite.Sprite):
    def __init__(self, coords, rotation):
        super().__init__()
        self.orig = pygame.surface.Surface((100,100))
        self.orig.set_colorkey((0,0,0))
        self.splintscreen = pygame.surface.Surface((100,100))
        self.splintscreen.set_colorkey((0,0,0))
        self.orig.set_alpha(255)
        self.alpha = 255
        self.fade = 0.85
        self.rect = self.orig.get_rect()
        self.rect.center = coords
        self.coords = vec(coords)
        self.timer = 0
        if rotation == 0:
            self.rect.midbottom = coords
        elif rotation == 90:
            self.rect.midright = coords
        elif rotation == 180:
            self.rect.midtop = coords
        elif rotation == 270:
            self.rect.midleft = coords
        self.rotation = rotation
        self.particlelist = []
        self.splinterlist = []

        for i in range(random.randint(1,3)):
            randomdir = random.randrange(-10,10)
            xpos = 50
            ypos = 100
            splinter = particle(xpos, ypos, randomdir , (-10 + randomdir), 0, 0, 5, -1, (255,220,150), self.splintscreen)
            self.splinterlist.append(splinter)

        for i in range(6):
            randomized1 = random.randrange(-10,10) / 10
            randomized2 = random.randrange(-10, 10) / 10
            randomized3 = random.randrange(-10, 10) / 10
            randomized4 = random.randrange(-10, 10) / 10
            randomized5 = random.randrange(-10, 10) / 10

            xpos = 50
            ypos = 100
            part = particle(xpos,ypos, randomized1, (randomized2 * 2 - 22), (randomized3 / 20), (5 + (randomized4 / 20)), 1, (1 + (randomized5 / 2)), (50,40,10), self.orig)
            self.particlelist.append(part)

    def update(self):
        # self.orig.fill((0,0,0))
        self.splintscreen.fill((0,0,0))
        for i in range(len(self.particlelist)):
            self.particlelist[i].draw()
        for i in range(len(self.splinterlist)):
            self.splinterlist[i].draw()
        self.timer += 1
        self.alpha = self.alpha * self.fade

        self.surf = pygame.transform.rotate(self.orig, self.rotation)
        self.splinters = pygame.transform.rotate(self.splintscreen, self.rotation)
        self.surf.set_alpha(self.alpha)
        screen.blit(self.surf, self.rect)
        screen.blit(self.splinters, self.rect)
        if self.timer > 15:
            self.kill()




class bullitimpact(pygame.sprite.Sprite):
    def __init__(self, coords, rotation):
        super().__init__()
        self.orig = hitpix[0]
        self.surf = pygame.transform.rotate(self.orig, rotation)
        self.rect = self.surf.get_rect()
        self.rect.center = coords
        if rotation == 0:
            self.rect.midbottom = coords
        elif rotation == 90:
            self.rect.midright = coords
        elif rotation == 180:
            self.rect.midtop = coords
        elif rotation == 270:
            self.rect.midleft = coords


        self.timer = 0
        self.rotation = rotation
    def update(self):
        self.timer += 1
        picnum = self.timer // 2
        self.surf = pygame.transform.rotate(hitpix[picnum], self.rotation)
        screen.blit(self.surf, self.rect)
        if self.timer > 8:
            self.kill()
