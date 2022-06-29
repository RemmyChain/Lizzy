import pygame
from pygame import *
from initialising import *
from images import *
import math
from math import atan2, degrees, floor

# arbiter class for game logic and storing global variables and stuff

class arbiter():
    def __init__(self):
        self.angle = 0
        self.death = False
        self.virtualposition = vec(0,0)
    def update(self):
        self.angleget()
        self.scroll()

# computing angle between Lizzy and the reticle for determining where she points her gatling at.

    def angleget(self):
        lizpos = vec(liz.rect.center)
        difference = vec(lizpos - cursor.pos)
        self.angle = round((degrees(atan2(difference.x, difference.y)) + 90), 2)
        if self.angle < 0:
            self.angle += 360

# scrolling the level.

    def scroll(self):
        if (liz.pos.x >= 800 and liz.vel.x > 0) or (liz.pos.x <= 700 and liz.vel.x < 0):
            self.scrolling = True
            for entity in allsprites:
                position = list(entity.rect.center)
                position[0] -= int(liz.vel.x)
                self.virtualposition.x += int(liz.vel.x)
                entity.rect.center = position
            liz.pos.x -= liz.vel.x
        if (liz.pos.y >= 800 and liz.vel.y > 0 and self.virtualposition.y <= 0) or (liz.pos.y <= 400 and liz.vel.y < 0):
            for entity in allsprites:
                position = list(entity.rect.center)
                position[1] -= int(liz.vel.y)
                self.virtualposition.y += int(liz.vel.y)
                entity.rect.center = position
            liz.pos.y -= liz.vel.y

# This is the mouse controlled reticle used for aiming and shooting

class Reticle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("reticle.png")
        self.rect = self.surf.get_rect()
        self.pos = vec(0,0)
    def update(self):
        x,y = pygame.mouse.get_pos()
        self.pos = vec(x,y)
        self.rect.center = self.pos
        screen.blit(self.surf, self.rect)

# The animated spinning barrels for Lizzy's gatling.

class barrels(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.orig = barrelpix
        self.surf = self.orig[0]
        self.rect = self.surf.get_rect()
        self.angle = 0
        self.preimage = self.orig[0]
        self.spinning = False
        self.animtick = 0
        self.barrelstate = self.orig[0]
        self.spinspeed = 0
        self.iteration = 0
        self.firing = False
    def rotate(self):
        self.angle = ref.angle
        if torso.reversed:
            self.preimage = pygame.transform.flip(self.barrelstate, False, True)
        else:
            self.preimage = self.barrelstate
        self.surf = pygame.transform.rotate(self.preimage, self.angle)
        self.rect = self.surf.get_rect()
    def fire(self):
        if self.animtick >= 3:
            self.animtick = 0
        self.firing = True
        self.barrelstate = self.orig[(self.animtick) + 2]
        self.animtick += 1
        if self.animtick == 3:
            self.animtick = 0
    def spinup(self):
        self.animtick += 1
        if self.animtick == 1:
            self.barrelstate = self.orig[1]
        elif self.animtick == 3:
            self.barrelstate = self.orig[2]
        elif self.animtick == 5:
            self.barrelstate = self.orig[0]
        elif self.animtick == 6:
            self.barrelstate = self.orig[1]
        elif self.animtick == 7:
            self.barrelstate = self.orig[2]
        elif self.animtick == 8:
            self.barrelstate = self.orig[0]
            self.animtick = 0
            self.spinning = True
    def winddown(self):
        self.firing = False
        self.animtick += 1
        if self.animtick == 1:
            self.barrelstate = self.orig[1]
        elif self.animtick == 2:
            self.barrelstate = self.orig[2]
        elif self.animtick == 3:
            self.barrelstate = self.orig[0]
        elif self.animtick == 5:
            self.barrelstate = self.orig[1]
        elif self.animtick == 8:
            self.barrelstate = self.orig[2]
        elif self.animtick == 11:
            self.barrelstate = self.orig[0]
            self.animtick = 0
            self.spinning = False

# Lizzy's legs, with walking and jumping animation

class Lizlegs(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = Lizlegstill
        self.rect = self.surf.get_rect()
        self.runtimer = 0
        self.runanim = []
        self.reverse = False
    def airborne(self, speed):
        if speed > 0:
            self.reverse = False
        if speed < 0:
            self.reverse = True
        if not self.reverse:
            if liz.vel.y < 0:
                self.surf = Lizlegsair[0]
            else:
                self.surf = Lizlegsair[1]
        if self.reverse:
            if liz.vel.y < 0:
                self.surf = Lizlegsaireverse[0]
            else:
                self.surf = Lizlegsaireverse[1]
    def run(self, speed):
        if speed > 0:
            self.reverse = False
            self.runanim = Lizlegsrun
        if speed < 0:
            self.reverse = True
            self.runanim = Lizlegsreverse
            speed = speed * -1
        self.frame = (self.runtimer // 10) + 3
        self.runtimer += speed // 3
        if self.runtimer >= 60:
            self.runtimer = -30
        if speed != 0:
            self.surf = self.runanim[self.frame]
        if speed == 0 and liz.grounded:
            if self.reverse:
                self.surf = pygame.transform.flip(Lizlegstill, True, False)
            else:
                self.surf = Lizlegstill

# Lizzy's torso with gatling, which rotates based on angle between Lizzy and reticle

class Liztorso(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = Liztorsostill
        self.rect = self.surf.get_rect()
        self.aim = []
        self.frame = 0
        self.reversed = False
        self.anglecheck = 0
    def update(self):
        theangle = ref.angle
        if self.reversed == False:
            self.aim = Liztorsopix
        if self.reversed == True:
            self.aim = Liztorsoreverse
            theangle = 360 - (theangle + 180)
            if theangle >= 360:
                theangle -= 180
        self.frame = floor((theangle + 11) / 22.5)
        if self.frame >= 16:
            self.frame = 0
        rotateangle = round((theangle - (22.5 * self.frame)), 2)
        self.anglecheck = rotateangle
        if not self.reversed:
            self.surf = pygame.transform.rotate((self.aim[self.frame]), rotateangle)
        if self.reversed:
            self.surf = pygame.transform.rotate((self.aim[self.frame]), (rotateangle * -1))
        self.rect = self.surf.get_rect()
    def reverse(self, speed):
        if speed < 0:
            self.reversed = True
        if speed > 0:
            self.reversed = False

# Lizzy's main control sprite with transparant surface and the rect hitbox.

class LizMain(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.orig = pygame.Surface((50,180))
        self.orig.fill("red")
        self.orig.set_alpha(0)
        self.surf = self.orig
        self.rect = self.surf.get_rect()
        self.rect.bottomleft = (100, 1000)
        self.acc = vec(4, 0)
        self.grav = vec(0, 0)
        self.vel = vec(0, 0)
        self.pos = vec(200, 1000)
        self.fric = 0.2
        self.grounded = False
    def deathcheck(self):
        if self.pos.y > 2000:
            ref.death = True
            torso.kill()
            legs.kill()
            self.kill()

# this checks if Lizzy is on solid ground or in the air

    def groundcheck(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            for i in range(len(hits)):
                if self.pos.y <= (hits[i].rect.top + 50):
                    self.pos.y = (hits[i].rect.top + 1)
                    self.vel.y = 0
                    self.grounded = True
                else:
                    self.grounded = False
        else:
            self.grounded = False

# check if Lizzy hits a hard block and define what happens if she does

    def hardblockcheck(self):

        hits = pygame.sprite.spritecollide(self, hardblocks, False)

        if hits:
            revert = self.pos.x - self.vel.x
            for i in range(len(hits)):
                if hits[i].rect.center[1] < self.rect.bottom + 10 and hits[i].rect.center[1] > self.rect.top - 10:
                    self.pos.x = revert
                    self.rect.midbottom = self.pos
                elif (self.pos.y <= (hits[i].rect.top + 50)) and ((self.vel.x <= 0 and self.rect.center[0] - hits[i].rect.center[0] < 50) or (self.vel.x >= 0 and self.rect.center[0] - hits[i].rect.center[0] > -50)):
                    self.pos.y = (hits[i].rect.top + 1)
                    self.vel.y = 0
                    self.grounded = True
                else:
                    self.grounded = False


                if self.vel.y < 0:
                    if (self.vel.x <= 0 and self.rect.center[0] - hits[i].rect.center[0] < 45) or (self.vel.x >= 0 and self.rect.center[0] - hits[i].rect.center[0] > -45):
                        self.vel.y = 0


# main update routine

    def update(self):
        self.move()
        self.groundcheck()
        self.hardblockcheck()
        self.integrate()
        self.render()
        self.deathcheck()
        torso.update()
        gatling.rotate()

# function for integrating all Lizzy's various sprites

    def integrate(self):
        legs.rect.midtop = self.rect.center
        torsooffset = vec(5,0)
        if torso.reversed == True:
            torso.rect.center = self.rect.center - torsooffset
        else:
            torso.rect.center = self.rect.center + torsooffset
        gatling.rect.center = torso.rect.center

# render all component sprite to the screen in correct order

    def render(self):
        screen.blit(legs.surf, legs.rect)
        screen.blit(torso.surf, torso.rect)
        screen.blit(gatling.surf, gatling.rect)
        screen.blit(self.surf, self.rect)

# controlling movement and actions based on keyboard and mouse input

    def move(self):
        if self.grounded or self.vel.y > 40:
            self.grav.y = 0
        else:
            self.grav.y = 2
        key = pygame.key.get_pressed()
        self.mousekey = pygame.mouse.get_pressed()
        if self.mousekey[0]:
            if not gatling.spinning:
                gatling.spinup()
            if gatling.spinning:
                gatling.fire()
        if not self.mousekey[0] and gatling.spinning:
            gatling.winddown()
        if key[K_d]:
            self.vel.x += self.acc.x
        if key[K_a]:
            self.vel.x -= self.acc.x
        if self.grounded and key[K_SPACE]:
            self.vel.y = -25
        if not key[K_SPACE] and self.vel.y < -5:
            self.vel.y += 5
        self.surf = self.orig
        if self.grounded:
            legs.run(int(self.vel.x))
        else:
            legs.airborne(int(self.vel.x))
        torso.reverse(int(self.vel.x))
        self.vel.x -= self.vel.x * self.fric
        self.vel += self.grav
        self.pos += self.vel
        self.rect.midbottom = self.pos
        if self.vel.x < 0.1 and self.vel.x > -0.1:
            self.vel.x = 0

# creating instances of all the stuff

ref = arbiter()
liz = LizMain()
legs = Lizlegs()
torso = Liztorso()
gatling = barrels()
cursor = Reticle()

