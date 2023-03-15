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
        self.killed = False
        self.surf.fill((0,0,0))
        self.surf.set_alpha(255)
        self.surf.set_colorkey((0,0,0))
        self.rect = self.surf.get_rect()
        self.hardblocked = False
        self.gothit = False
        self.pos = vec(coords)
        self.rect.midbottom = self.pos
        self.speed = -5
        self.fallspeed = 0
        self.health = 25
        self.grounded = False
        self.gravity = 2
        self.reversed = False
        self.timer = 0
        self.deathtimer = 0
        self.oldpos = self.pos
        self.xpos1 = 40
        self.xpos2 = 85
        self.xpos3 = 100
        self.xpos4 = 145
        self.ypos1 = 70
        self.ypos2 = 70
        self.ypos3 = 70
        self.ypos4 = 70
        self.partlist1 = []
        self.partlist2 = []
        self.attack = 20

    def gethit(self, hitcoords, damage, type):

        self.gothit = True
        self.health -= damage
        chance = random.randint(0, 2)
        if type == "bullet" or type == "melee":
            if chance == 0:
                hitfx = organichit(hitcoords)
                allsprites.add(hitfx)
        elif type == "explosive":
            blast = explosive(hitcoords)
            allsprites.add(blast)
        copysurf = self.surf
        if not self.killed:
            self.surf.blit(copysurf, (100, 50), special_flags=BLEND_RGB_ADD)
        if type != "explosive":
            if hitcoords[0] < self.rect.centerx:
                if not self.hardblocked:
                    self.rect.centerx += 10
                else:
                    self.rect.centerx -= 10
            if hitcoords[0] > self.rect.centerx:
                if not self.hardblocked:
                    self.rect.centerx -= 10
                else:
                    self.rect.centerx += 5

        if self.health <= 0:
            self.killed = True

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
                self.rect.centerx -= 150
            elif self.reversed:
                self.rect.centerx += 150
            hits = pygame.sprite.spritecollide(self, platforms, False)
            if not self.reversed:
                self.rect.centerx += 150
            elif self.reversed:
                self.rect.centerx -= 150
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
            self.hardblocked = True
        else:
            self.hardblocked = False

    def render(self):

        if not self.reversed:
            screen.blit(self.surf, self.rect)
            if self.gothit:
                screen.blit(self.surf, self.rect, special_flags=BLEND_RGB_ADD)
        else:
            flipped = pygame.transform.flip(self.surf, True, False)
            screen.blit(flipped, self.rect)
            if self.gothit:
                screen.blit(flipped, self.rect, special_flags=BLEND_RGB_ADD)

        if self.health < 25:
            healthrect = pygame.Rect(self.rect.left, self.rect.bottom, self.health * 5, 5)
            pygame.draw.rect(screen, ("red"), healthrect)
        self.surf.fill((0, 0, 0))

    def update(self):
        if self.timer > 19:
            self.timer = 0
        self.edgedetect()
        if not self.killed:
            self.move()
        self.platformcheck()
        self.hardblockscheck()


        if self.deathtimer < 5:
            self.animate()
            self.render()
        if self.killed:
            self.deathani()
        self.timer += 1
        self.gothit = False

    def deathani(self):
        if self.deathtimer == 0:
            for i in range(30):
                x = self.rect.centerx + (random.randint( -30, 30))
                y = self.rect.centery + (random.randint(-10, 10))
                randomcol = random.randint( 170, 230)
                part1 = particle(x, y, 0, 0, 0, 0, 1, 4, (50, randomcol, 20), screen, (0 ,0 ,0), True)
                self.partlist1.append(part1)
        if self.deathtimer < 8:

            for i in self.partlist1:
                i.draw()

        if self.deathtimer == 6:
            for i in range(50):
                x = self.rect.centerx + (random.randint(-40, 40))
                y = self.rect.centery + (random.randint(-20, 20))
                randomcol2 = random.randint( 170, 230)
                part2 = particle(x, y, random.randint(-15, 15), random.randint(-30, 0), 0, 1, 8, -0.4, (50, randomcol2, 20), screen, (0 ,0 ,0), True)
                self.partlist2.append(part2)
        if self.deathtimer > 6 and self.deathtimer < 20:
            for i in self.partlist2:
                i.draw()

        if self.deathtimer > 30:
            self.kill()
        self.deathtimer += 1


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



