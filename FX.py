import pygame
from pygame import *
from initialising import *
from images import *
from Lizzy import *
from enemies import *
import math
from math import atan2, degrees, floor, sin, cos, radians, pi, sqrt
import random

class crash(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__()
        self.pos = vec(coords)
        self.surf = pygame.surface.Surface((300, 300))
        self.rect = self.surf.get_rect()
        self.rect.center = self.pos
        self.surf.fill((0, 0, 0))
        self.surf.set_alpha(255)
        self.surf.set_colorkey((0, 0, 0))
        self.innersurf = pygame.surface.Surface((100, 100))
        self.innersurf.fill((255, 255, 255))
        self.timer = 0
        self.scale = 0
        self.fade = 0
        for i in range(0, 8):
            spacing = (pi / 4)
            angle = (spacing * i) + (random.randint(-5, 5) / 50)
            radius = random.randint(20, 25)
            x = cos(angle) * 50 + 50
            y = sin(angle) * 50 + 50
            pygame.draw.circle(self.innersurf, (0, 0, 0), (x, y), radius, 0)

    def update(self):
        self.surf.fill((0, 0, 0))
        self.innersurfx = pygame.transform.smoothscale(self.innersurf, ((100 + self.scale), (100 + self.scale)))
        self.surf.set_alpha(255 - self.fade)

        self.surf.blit(self.innersurfx, ((100 - (self.scale / 2)), (100 - (self.scale / 2))))
        screen.blit(self.surf, self.rect)
        self.timer += 2
        self.scale += 20 - self.timer
        self.fade += 10 + self.timer * 5
        if self.timer > 10:
            self.kill()

class blasticle():
    def __init__(self, pos, vel, acc, size, dsize, ddsize, color, surface, colorchange, dcolorchange):
        self.pos = vec(pos)
        self.vel = vec(vel)
        self.acc = vec(acc)
        self.size = size
        self.dsize = dsize
        self.ddsize = ddsize
        self.color = color
        self.surface = surface
        self.colorchange = colorchange
        self.dcolorchange = dcolorchange
        self.red = self.color[0]
        self.blue = self.color[2]
        self.green = self.color[1]

    def draw(self):
        pygame.draw.circle(self.surface, self.color, self.pos, self.size, 0)

        self.red += (self.colorchange[0] * self.dcolorchange)
        if self.red < 10:
            self.red = 10
        self.green += (self.colorchange[1] * self.dcolorchange)
        if self.green < 10:
            self.green = 10
        self.blue += (self.colorchange[2] * self.dcolorchange)
        if self.blue < 10:
            self.blue = 10
        self.color = (self.red, self.green, self.blue)

        self.pos += self.vel
        self.vel += self.acc

        self.size += self.dsize
        self.dsize += self.ddsize



class particle():
    def __init__(self, xpos, ypos, xvel, yvel, xacc, yacc, size, dsize, color, surface, colorchange):
        self.xpos = xpos
        self.ypos = ypos
        self.xvel = xvel
        self.yvel = yvel
        self.xacc = xacc
        self.yacc = yacc
        self.size = size
        self.dsize = dsize
        self.color = color
        self.colorchange = colorchange
        self.surface = surface
        self.center = vec(self.xpos, self.ypos)
        self.red = self.color[0]
        self.blue = self.color[2]
        self.green = self.color[1]
    def draw(self):
        pygame.draw.circle(self.surface, self.color, self.center, self.size, 0)

        self.red += self.colorchange[0]
        self.green += self.colorchange[1]
        self.blue += self.colorchange[2]
        self.color = (self.red, self.green, self.blue)
        self.xvel += self.xacc
        self.yvel += self.yacc
        if self.yvel > 0:
            self.yvel = random.randrange(-1,1)
        # self.xpos += self.xvel
        # self.ypos += self.ypos
        self.size += self.dsize
        self.center.x += self.xvel
        self.center.y += self.yvel

class explosive(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__()
        self.circleseedzise = 20
        self.circle2size = 5
        self.surf = pygame.surface.Surface((200, 200))
        self.blastsurf = pygame.surface.Surface((200, 200))

        self.blastsurf.set_colorkey((0, 0, 0))

        self.blastsurf.set_alpha(50)

        self.rect = self.surf.get_rect()
        self.rect.center = vec(coords)
        self.timer = 0
        self.list = []
        self.surf.set_alpha(255)
        self.surf.set_colorkey((0, 0, 0))
        self.alpha = 255
        self.fade = 10
        self.faderate = 1.5

    def circly(self, size, expand, color,):
        # self.blastsurf.fill((0, 0, 0))
        pygame.draw.circle(self.blastsurf, color, (100, 100), size)
        self.circleseedzise += expand
        self.circle2size += expand

        for i in range(25):
            x = random.random()
            y = sqrt(1 - (x * x))
            rando1 = random.randint(0, 1)
            if rando1 == 0:
                rando1 = -1
            rando2 = random.randint(0, 1)
            if rando2 == 0:
                rando2 = -1
            x += random.random() / 2
            y += random.random() / 2
            x *= rando1
            y *= rando2
            size = random.random() * 2
            vel = vec(x, y)
            vel *= 10
            acc = vel * -0.1
            part = blasticle((100, 100), vel, acc, size, 2.2, -0.8, (255, 255, 255), self.surf, (-5, -20, -30), 1.5)
            self.list.append(part)

    def update(self):
        self.surf.fill((0, 0, 0))
        for thing in self.list:
            thing.draw()
        self.surf.set_alpha(self.alpha)
        self.alpha -= self.fade
        self.fade *= self.faderate
        self.timer += 1
        if self.timer < 8:
            self.circly(self.circleseedzise, 4, (10, 10, 10))
        if self.timer > 4:
            self.circly(self.circle2size, 8, (0, 0, 0))
        screen.blit(self.surf, self.rect)
        screen.blit(self.blastsurf, self.rect, special_flags=BLEND_RGB_ADD)

        if self.timer == 10:
            self.kill()


class muzzleflash(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.orig = pygame.surface.Surface((100,50))
        self.orig.set_colorkey((0,0,0))
        self.orig.set_alpha(200)
        self.rect = self.orig.get_rect()
        self.list = []
        self.timer = 0
        self.angle = ref.angle
        self.offangle = ref.angle
        self.pos = vec(liz.rect.center)
        self.color = color

    def update(self):

        self.timer += 1
        self.orig.fill((0,0,0))
        if self.color == 0:
            colorchange = (-15, -25, -60)
            color = (255, 255, 240)
        elif self.color == 1:
            colorchange = (-45, -45, -10)
            color = (240, 240, 255)
        else:
            colorchange = (-10, -45, -45)
            color = (255, 240, 240)
        if self.timer > 2:
            for i in range(12):
                random1 = random.randrange(23, 27)
                random2 = random.randrange(0, 50)
                random3 = random.randrange(-5, 5)
                random4 = random.randrange(5, 15)
                part = particle(random2, random1, random4, random3 ,0 ,(random3 * -0.2) , 5, -1, color, self.orig, colorchange)
                self.list.append(part)
        for i in self.list:
            i.draw()
            if i.size < 1:
                self.list.remove(i)
        self.glow = pygame.transform.scale(self.orig, (130, 65))
        self.glow.set_alpha(100)
        self.glowy = pygame.transform.rotate(self.glow, self.angle)
        self.glowrect = self.glowy.get_rect()
        self.surf = pygame.transform.rotate(self.orig, self.angle)
        self.rect = self.surf.get_rect()

        self.angle = gatling.angle
        if self.angle > 360:
            self.angle -= 360
        self.offangle = gatling.angle

        if self.offangle > 360:
            self.offangle -= 360
        xoffset = 160 * cos(radians(self.offangle))
        yoffset = 160 * sin(radians(self.offangle))
        self.pos = vec(liz.rect.center)
        self.pos.x += xoffset
        self.pos.y -= yoffset
        self.rect.center = self.pos
        self.glowrect.center = self.pos

        screen.blit(self.glowy, self.glowrect)
        screen.blit(self.surf, self.rect)
        if self.timer > 2:
            self.timer = 0
        if gatling.firing == False:
            self.kill()

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
            splinter = particle(xpos, ypos, randomdir , (-10 + randomdir), 0, 0, 5, -1, (255,220,150), self.splintscreen, (0,0,0))
            self.splinterlist.append(splinter)

        for i in range(6):
            randomized1 = random.randrange(-10,10) / 10
            randomized2 = random.randrange(-10, 10) / 10
            randomized3 = random.randrange(-10, 10) / 10
            randomized4 = random.randrange(-10, 10) / 10
            randomized5 = random.randrange(-10, 10) / 10

            xpos = 50
            ypos = 100
            part = particle(xpos,ypos, randomized1, (randomized2 * 2 - 22), (randomized3 / 20), (5 + (randomized4 / 20)), 1, (1 + (randomized5 / 2)), (50,40,10), self.orig, (0,0,0))
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

class organichit(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__()
        self.pos = vec(coords)
        self.timer = 0
        self.surf = pygame.surface.Surface((100, 100))
        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.center = self.pos
        self.list = []
        for i in range(7):
            xvel = random.randrange(-100, 100) / 10
            yvel = 10 - abs(xvel)
            yvel *= random.randint(-1, 1)
            part = particle(50, 50, xvel, yvel, -1, -1, 3, -0.2, (240, 0, 0), self.surf, (0, 0, 0))
            self.list.append(part)
    def update(self):
        self.surf.fill((0, 0, 0))
        for i in self.list:
            i.draw()
        self.timer += 1
        screen.blit(self.surf, self.rect)
        if self.timer > 20:
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
