import pygame
from pygame import *
from initialising import *
from images import *
import math
from math import atan2, degrees, floor, sin, cos, radians
import random

# arbiter class for game logic and storing global variables and stuff

class arbiter():
    def __init__(self):
        self.angle = 0
        self.death = False
        self.virtualposition = vec(0,0)
        self.scrollmeter = vec(0,0)
        self.xscrolling = False
        self.yscrolling = False
    def update(self):
        self.angleget()

        self.scroll()
        self.virtpos()
    def virtpos(self):
        if self.xscrolling:
            self.scrollmeter.x += int(liz.vel.x)
        if self.yscrolling:
            self.scrollmeter.y += int(liz.vel.y)

        self.virtualposition = liz.pos  + self.scrollmeter
        self.virtualposition.x = int(self.virtualposition.x)
        # self.virtualposition.x = int(self.virtualposition.x)
        # self.virtualposition.y = int(self.virtualposition.y)

# computing angle between Lizzy and the reticle for determining where she points her gatling at.

    def angleget(self):
        lizpos = vec(liz.rect.center)
        mousepos = vec(pygame.mouse.get_pos())
        difference = vec(lizpos - mousepos)
        self.angle = round((degrees(atan2(difference.x, difference.y)) + 90), 2)
        if self.angle < 0:
            self.angle += 360

# scrolling the level.

    def scroll(self):
        if (liz.pos.x >= 800 and liz.vel.x > 0) or (liz.pos.x <= 700 and liz.vel.x < 0):
            self.xscrolling = True
            for entity in allsprites:
                position = list(entity.rect.center)
                position[0] -= int(liz.vel.x)
            #    self.virtualposition.x += int(liz.vel.x)
                entity.rect.center = position
            liz.pos.x -= liz.vel.x
        else:
            self.xscrolling = False
        if (liz.pos.y >= 800 and liz.vel.y > 0 and self.virtualposition.y <= 800) or (liz.pos.y <= 400 and liz.vel.y < 0 and self.virtualposition.y >= -400):
            self.yscrolling = True
            for entity in allsprites:
                position = list(entity.rect.center)
                position[1] -= int(liz.vel.y)
            #    self.virtualposition.y += int(liz.vel.y)
                entity.rect.center = position
            liz.pos.y -= liz.vel.y
        else:
            self.yscrolling = False


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

        for i in range(7):
            randomized1 = random.randrange(-10,10) / 10
            randomized2 = random.randrange(-10, 10) / 10
            randomized3 = random.randrange(-10, 10) / 10
            randomized4 = random.randrange(-10, 10) / 10
            randomized5 = random.randrange(-10, 10) / 10

            xpos = 50
            ypos = 100
            part = particle(xpos,ypos, randomized1, (randomized2 * 2 - 22), (randomized3 / 20), (5 + (randomized4 / 20)), 1, (1 + (randomized5 / 2)), (10,10,10), self.orig)
            self.particlelist.append(part)

    def update(self):
        # self.orig.fill((0,0,0))
        for i in range(len(self.particlelist)):
            self.particlelist[i].draw()
        self.timer += 1
        self.alpha = self.alpha * self.fade

        self.surf = pygame.transform.rotate(self.orig, self.rotation)
        self.surf.set_alpha(self.alpha)
        screen.blit(self.surf, self.rect)
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

class hitdetector(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((3,3))
        self.surf.set_alpha(0)
        self.rect = self.surf.get_rect()

class Tracereffect(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.orig = tracer
        self.surf = pygame.transform.rotate(self.orig, ref.angle)
        self.rect = self.surf.get_rect()
        self.pos = vec(liz.rect.center)
        self.error = random.randint(-1,1) // 2
        self.tick = 0
        self.scantick = 0
        self.angle = ref.angle + 90 + self.error
        if self.angle > 360:
            self.angle -= 360
        self.pos.x += (sin(radians(self.angle))) * 50
        self.pos.y += (cos(radians(self.angle))) * 50
        self.rect.center = self.pos
        self.impactsite = (0,0)
        self.rotation = 0


    def update(self):

        ping = hitdetector()
        ping.rect.center = self.pos
        for i in range(100):
            knal = pygame.sprite.spritecollide(ping, hardblocks, False)
            if not knal:
                ping.rect.centerx += (sin(radians(self.angle))) * 10
                ping.rect.centery += (cos(radians(self.angle))) * 10
                self.impactsite = vec(ping.rect.center)
            else:
                ping.kill()

        self.pos.x += (sin(radians(self.angle))) * 100
        self.pos.y += (cos(radians(self.angle))) * 100
        self.tick += 1
        self.rect.center = self.pos
        screen.blit(self.surf, self.rect)
        hits = pygame.sprite.spritecollide(self, hardblocks, False)
        if hits:
            if (abs(self.rect.center[0] - self.impactsite[0]) < 50):
                if abs(self.impactsite[1] - hits[0].rect.top) < 15:
                    self.rotation = 0
                elif abs(self.impactsite[0] - hits[0].rect.left) < 15:
                    self.rotation = 90
                elif abs(self.impactsite[1] - hits[0].rect.bottom) < 15:
                    self.rotation = 180
                elif abs(self.impactsite[0] - hits[0].rect.right) < 15:
                    self.rotation = 270
            #    pow = bullitimpact(self.impactsite, self.rotation)
                pow = spriticle(self.impactsite, self.rotation)
                allsprites.add(pow)
            for i in range(len(hits)):
                screen.blit(hits[i].surf, hits[i].rect)
                self.kill()
        if self.tick > 20:
            self.kill()

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
        if self.animtick == 0:
            trace = Tracereffect()
            allsprites.add(trace)
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
    def run(self, speed, key):
        if speed > 0 and key != 0:
            self.reverse = False
            self.runanim = Lizlegsrun
        if speed < 0 and key != 0:
            self.reverse = True
            self.runanim = Lizlegsreverse
            speed = speed * -1
        if self.runtimer > 60:
            self.runtimer = -30
        if self.runtimer < -30:
            self.runtimer = 60
        self.frame = (self.runtimer // 10) + 3

        self.runtimer += speed // 3

        if speed != 0 and key != 0:
            self.surf = self.runanim[self.frame]
        if speed == 0 and liz.grounded and key == 0:
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
    def reverse(self, speed, key):
        if speed < 0 and key != 0:
            self.reversed = True
        if speed > 0 and key != 0:
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
        self.recoil = vec(0,0)
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
    #    if not key[K_SPACE] and self.vel.y < -5:
    #        self.vel.y += 5
        self.surf = self.orig
        if not key[K_a] and not key[K_d]:
            key = 0
        if self.grounded:

            legs.run(int(self.vel.x), key)
        else:
            legs.airborne(int(self.vel.x))
        torso.reverse(int(self.vel.x), key)

        self.vel.x -= self.vel.x * self.fric
        self.vel += self.grav

        if gatling.firing:
            self.recoil.x = cos(radians(ref.angle)) * 1.5
            if not self.grounded:
                self.recoil.y = sin(radians(ref.angle)) * -2.5
                if self.vel.y > 40 or self.vel.y < -40:
                    self.recoil.y = 0
            self.vel -= self.recoil
        else:
            self.recoil = vec(0,0)

        if self.pos.y <= 0:
            self.vel.y = 1
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
# cursor = Reticle()

