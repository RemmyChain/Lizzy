import pygame
from pygame import *
from initialising import *
from images import *
from enemies import *
import math
from math import atan2, degrees, floor, sin, cos, radians
import random
import FX
from FX import *


# simple placeholder sprite used to gauge level shift to use for saving and reverting during respawn

class yardstick(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.surface.Surface((10, 10))
        self.surf.fill((0, 0, 0))
        self.surf.set_alpha(0)
        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.center = (0, 0)

    def update(self):
        pass


schrevel = yardstick()
allsprites.add(schrevel)


# arbiter class for game logic and storing global variables and stuff

class arbiter():
    def __init__(self):
        self.angle = 0
        self.death = False
        self.virtualposition = vec(0, 0)
        self.scrollmeter = vec(0, 0)
        self.xscrolling = False
        self.yscrolling = False
        self.sbleft = int(screensize[0] * 0.4)
        self.sbright = int(screensize[0] * 0.6)
        self.sbtop = int(screensize[1] * 0.4)
        self.sbbottom = int(screensize[1] * 0.7)
        self.lizpossave = vec(0, 0)
        self.leveloffset = vec(0, 0)
        self.virtpossave = vec(0, 0)
        self.savetimer = 0
        self.ammoselect = 155
        self.peiling = vec(0, 0)

    def update(self):
        self.angleget()
        self.save()
        self.scroll()
        self.virtpos()
        self.hud()

    # a function for saving and reverting position upon death

    def save(self):

        if liz.grounded and not self.death:
            self.savetimer += 1
            if self.savetimer == 5:
                self.lizpossave = vec(liz.pos)

                self.virtpossave = vec(self.scrollmeter)

                self.leveloffset = vec(0, 0)
                self.peiling = vec(schrevel.rect.center)
                self.savetimer = 0

        if self.death:
            liz.pos = vec(self.lizpossave)

            self.scrollmeter = vec(self.virtpossave)

            liz.vel = vec(0, 0)
            leveloffset = vec(schrevel.rect.center - self.peiling)

            for i in allsprites:
                i.rect.center -= leveloffset

            gatling.firing = False
            gatling.spinning = False
            gatling.animtick = 0

            liz.health = 100
            for amount in range(3):
                if liz.ammo[amount] < 100:
                    liz.ammo[amount] = 100
            liz.dead = False
            liz.gothit = False
            liz.dying = False
            liz.hittimer = 0
            liz.deathtimer = 0
            liz.immune = True
            self.death = False

    def hud(self):
        lizhealth = pygame.Rect(20, 120, liz.health * 5, 5)
        pygame.draw.rect(screen, ("red"), lizhealth)
        normalammocount = font.render("regular ammo: " + str(liz.ammo[0]), True, ("black"))
        hvammocount = font.render("hyper velocity ammo: " + str(liz.ammo[1]), True, ("black"))
        explosiveammocount = font.render("explosive ammo: " + str(liz.ammo[2]), True, ("black"))
        screen.blit(normalammocount, (40, 140))
        screen.blit(hvammocount, (40, 160))
        screen.blit(explosiveammocount, (40, 180))
        self.ammoselect = 155 + (liz.ammotype * 20)
        pygame.draw.circle(screen, (255, 255, 255), (20, self.ammoselect), 5)


    def virtpos(self):
        if self.xscrolling:
            self.scrollmeter.x += int(liz.vel.x)
        if self.yscrolling:
            self.scrollmeter.y += int(liz.vel.y)

        self.virtualposition = liz.pos + self.scrollmeter
        self.virtualposition.x = int(self.virtualposition.x)
        # if liz.grounded:
        #   self.virtualposition.y = int(self.virtualposition.y / 100) * 100

        # self.virtualposition.y = int(self.virtualposition.y)
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
        if (liz.pos.x >= self.sbright and liz.vel.x > 0) or (liz.pos.x <= self.sbleft and liz.vel.x < 0):
            self.xscrolling = True
            for entity in allsprites:
                position = list(entity.rect.center)
                position[0] -= int(liz.vel.x)
                #    self.virtualposition.x += int(liz.vel.x)
                entity.rect.center = position
            liz.pos.x -= liz.vel.x

        else:
            self.xscrolling = False
        if (liz.pos.y >= self.sbbottom and liz.vel.y > 0 and self.virtualposition.y <= 800) or (
                liz.pos.y <= self.sbtop and liz.vel.y < 0 and self.virtualposition.y >= -400):
            self.yscrolling = True
            for entity in allsprites:
                position = list(entity.rect.center)
                position[1] -= int(liz.vel.y)
                #    self.virtualposition.y += int(liz.vel.y)
                entity.rect.center = position
            liz.pos.y -= liz.vel.y

        else:
            self.yscrolling = False


class meleehurtbox(pygame.sprite.Sprite):
    def __init__(self, position, orient):
        super().__init__()
        if orient == "left" or orient == "right":
            self.surf = pygame.surface.Surface((80, 40))
        else:
            self.surf = pygame.surface.Surface((40, 80))
        self.surf.fill((0, 0, 0))
        self.surf.set_alpha(100)
        self.rect = self.surf.get_rect()
        self.offset = vec(position)
        self.timer = 0
        self.orient = orient

    def update(self):
        coords = vec(liz.rect.center) + self.offset
        self.rect.center = coords

        whackedbeast = pygame.sprite.spritecollide(self, enemies, False)
        if whackedbeast:

            for i in whackedbeast:
                i.gethit(self.rect.center, 10, "melee")
                if self.orient == "left":
                    i.rect.centerx -= 30
                    liz.vel.x += 10
                    crashcoords = vec((self.rect.centerx - 30), self.rect.centery)
                elif self.orient == "right":
                    i.rect.centerx += 30
                    liz.vel.x -= 10
                    crashcoords = vec((self.rect.centerx + 30), self.rect.centery)
                elif self.orient == "up":
                    i.rect.centery += 30
                    liz.vel.y = 0
                    crashcoords = vec(self.rect.centerx, (self.rect.centery - 30))
                elif self.orient == "down":
                    i.rect.centery += 30
                    liz.vel.y = -20
                    crashcoords = vec(self.rect.centerx, (self.rect.centery + 30))
            paf = FX.crash(crashcoords)
            allsprites.add(paf)
            self.kill()
        if not liz.groundpound:
            self.timer += 1
        if self.timer > 5:
            self.kill()

        # screen.blit(self.surf, self.rect)


class hitdetector(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((1, 1))
        self.surf.set_alpha(0)
        self.rect = self.surf.get_rect()


class Tracereffect(pygame.sprite.Sprite):
    def __init__(self, state, type, cycle):
        super().__init__()
        self.orig = tracer[type]
        self.surf = pygame.transform.rotate(self.orig, ref.angle)
        self.rect = self.surf.get_rect()
        self.pos = vec(liz.rect.center)
        self.error = random.randint(-1, 1) // 2
        self.tick = 0
        self.cycle = cycle

        self.angle = ref.angle + 90 + self.error
        if self.angle > 360:
            self.angle -= 360
        self.pos.x += (sin(radians(self.angle))) * 50
        self.pos.y += (cos(radians(self.angle))) * 50
        self.rect.center = self.pos

        self.rotation = 0
        self.state = state
        self.internal = False

    def update(self):

        ping = hitdetector()
        ping.rect.center = self.pos
        for i in range(5):

            ping.rect.centerx += (sin(radians(self.angle))) * 20
            ping.rect.centery += (cos(radians(self.angle))) * 20
            knal = pygame.sprite.spritecollide(ping, hardblocks, False)
            pats = pygame.sprite.spritecollide(ping, enemies, False)
            if (knal or pats) and not self.internal:
                impact = hitdetector()
                impact.rect.center = ping.rect.center
                impacts.add(impact)
                self.internal = True
                if liz.ammotype != 1:
                    ping.kill()
                elif i == 20:
                    ping.kill()
            if self.internal and not (knal or pats):
                exity = hitdetector()
                exity.rect.center = ping.rect.center
                exits.add(exity)
                self.internal = False

        self.pos.x += (sin(radians(self.angle))) * 100
        self.pos.y += (cos(radians(self.angle))) * 100
        self.tick += 1
        self.rect.center = self.pos
        if self.state == "visible":
            screen.blit(self.surf, self.rect)
        hits = pygame.sprite.spritecollide(self, hardblocks, False)
        splut = pygame.sprite.spritecollide(self, enemies, False)
        impactss = pygame.sprite.spritecollide(self, impacts, True)
        exitss = pygame.sprite.spritecollide(self, exits, True)
        if knal and not pats:
            for i in range(len(hits)):
                if impactss:
                    if abs(impactss[0].rect.centery - hits[i].rect.top) < 15:
                        self.rotation = 0
                    elif abs(impactss[0].rect.centerx - hits[i].rect.left) < 15:
                        self.rotation = 90
                    elif abs(impactss[0].rect.centery - hits[i].rect.bottom) < 15:
                        self.rotation = 180
                    elif abs(impactss[0].rect.centerx - hits[i].rect.right) < 15:
                        self.rotation = 270
                        #    pow = bullitimpact(self.impactsite, self.rotation)
                    if liz.ammotype == 2:
                        boem = FX.explosive(impactss[0].rect.center)

                        allsprites.add(boem)
                    else:
                        hits[i].gethit(impactss[0].rect.center, self.rotation)

                if not impactss and liz.ammotype == 2:
                    if 90 < ref.angle < 270:
                        boem = FX.explosive(hits[0].rect.midright)
                        allsprites.add(boem)
                    else:
                        boem = FX.explosive(hits[0].rect.midleft)
                        allsprites.add(boem)


                if exitss:
                    self.rotation += 180
                    if self.rotation > 360:
                        self.rotation -= 360
                    # pow = spriticle(self.impactsite, self.rotation)
                    # allsprites.add(pow)
                    hits[i].gethit(exitss[0].rect.center, self.rotation)
                if liz.ammotype != 2:

                    screen.blit(hits[i].surf, hits[i].rect, )
                if liz.ammotype != 1:
                    self.kill()

        if pats and not knal:

            for i in splut:
                if impactss:
                    if liz.ammotype != 2:
                        i.gethit(impactss[0].rect.center, 1, "bullet")
                    elif liz.ammotype == 2:
                        boem = FX.explosive(impactss[0].rect.center)

                        allsprites.add(boem)
                screen.blit(i.surf, i.rect)
                if liz.ammotype != 1:
                    self.kill()
                if exitss:

                    i.gethit(exitss[0].rect.center, 0, "bullet")

        if self.tick > 20:
            self.kill()


class Reticle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("reticle.png")
        self.rect = self.surf.get_rect()
        self.pos = vec(0, 0)

    def update(self):
        x, y = pygame.mouse.get_pos()
        self.pos = vec(x, y)
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
        self.flash = False

    def rotate(self):
        self.angle = ref.angle
        if torso.reversed:
            self.preimage = pygame.transform.flip(self.barrelstate, False, True)
        else:
            self.preimage = self.barrelstate
        self.surf = pygame.transform.rotate(self.preimage, self.angle)
        self.rect = self.surf.get_rect()

    def fire(self):
        liz.ammo[liz.ammotype] -= 1
        if not self.flash:
            flash = FX.muzzleflash(liz.ammotype)
            flashy.add(flash)
            self.flash = True

        if self.animtick >= 3:
            self.animtick = 0
        if self.animtick == 0:
            trace = Tracereffect("visible", liz.ammotype, self.animtick)
            allsprites.add(trace)
        else:
            trace = Tracereffect("invisible", liz.ammotype, self.animtick)
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
        self.flash = False
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
        self.orig = pygame.Surface((50, 180))
        self.hitsurf = Lizhit
        self.deathsurf = Lizdeath[0]
        self.meleesurf = Lizmelee[0]
        self.orig.fill("red")
        self.orig.set_alpha(0)
        self.surf = self.orig
        self.rect = self.surf.get_rect()
        self.rect.bottomleft = (100, 1000)
        self.acc = vec(4, 0)
        self.grav = vec(0, 0)
        self.vel = vec(0, 0)
        self.pos = vec(200, 200)
        self.fric = 0.2
        self.grounded = False
        self.recoil = vec(0, 0)
        self.gothit = False
        self.hittimer = 0
        self.deathtimer = 0
        self.health = 100
        self.dying = False
        self.dead = False
        self.yoffset = 0
        self.reverse = False
        self.immune = False
        self.immunetimer = 0
        self.blink = False
        self.melee = False
        self.meleetimer = 0
        self.meleereverse = False
        self.blitoffset = vec(0, 0)
        self.meleetoken = [1, 1, 1]
        self.groundpound = False
        self.meleestate = "null"
        self.ammo = [200, 200, 200]
        self.ammotype = 0
        self.ammoswitchpressed = False


    # dying animation controller

    def swansong(self):

        self.deathtimer += 1
        self.immune = False
        self.immunetimer = 0

        if self.deathtimer < 5:
            self.deathsurf = Lizhit
            self.yoffset = -100

        if 5 <= self.deathtimer < 10:
            self.deathsurf = Lizdeath[0]
            self.yoffset = -100

        if 10 <= self.deathtimer < 15:
            self.deathsurf = Lizdeath[1]
            self.yoffset = -50

        if 15 <= self.deathtimer <= 30:
            self.deathsurf = Lizdeath[2]
            self.yoffset = 50

        if self.deathtimer == 30:
            self.deathtimer = 0
            self.dying = False
            self.dead = True

    # check if dead (due to fall or health depletion)

    def deathcheck(self):
        if self.pos.y > 2000:
            ref.death = True

        if self.health < 0:
            self.health = 0

        if self.health == 0 and not self.dead:
            self.dying = True
            self.swansong()

        if self.dead:
            ref.death = True

        # invulnerability timer blink thing for hit and respawn

        if self.immune:
            self.immunetimer += 1
            if self.immunetimer % 3 == 0 and not self.melee:
                self.blink = True
            else:
                self.blink = False
            if self.immunetimer >= 31:
                self.immunetimer = 0
                self.immune = False

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
            reverty = self.pos.y - self.vel.y
            for i in range(len(hits)):
                if hits[i].rect.center[1] < self.rect.bottom + 10 and hits[i].rect.center[1] > self.rect.top - 10:
                    self.pos.x = revert
                    self.rect.midbottom = self.pos
                elif (self.pos.y <= (hits[i].rect.top + 50)) and (
                        (self.vel.x <= 0 and self.rect.center[0] - hits[i].rect.center[0] < 50) or (
                        self.vel.x >= 0 and self.rect.center[0] - hits[i].rect.center[0] > -50)):
                    self.pos.y = (hits[i].rect.top + 1)
                    self.vel.y = 0
                    self.grounded = True
                else:
                    self.grounded = False

                if self.vel.y < 0:
                    if (self.vel.x <= 0 and self.rect.center[0] - hits[i].rect.center[0] < 45) or (
                            self.vel.x >= 0 and self.rect.center[0] - hits[i].rect.center[0] > -45):
                        self.vel.y = 0
                        self.pos.y = reverty

    # main update routine

    def update(self):
        if not self.dying and not self.dead:
            self.gethit()
        self.move()
        self.groundcheck()
        self.hardblockcheck()
        self.integrate()
        if not self.blink:
            self.render()
        self.deathcheck()
        torso.update()
        gatling.rotate()

    def gethit(self):
        ouch = pygame.sprite.spritecollide(self, enemies, False)
        yikes = pygame.sprite.spritecollide(self, hazards, False)
        if ouch or yikes:
            self.pos -= self.vel

        if ouch and not self.gothit and self.hittimer == 0 and not self.immune:

            self.health -= ouch[0].attack
            xcor = ((self.rect.centerx * 2) + ouch[0].rect.centerx) // 3
            ycor = ((self.rect.centery * 2) + ouch[0].rect.centery) // 3
            crashcoords = (xcor, ycor)
            paf = FX.crash(crashcoords)
            allsprites.add(paf)
            self.gothit = True
            self.immune = True
            if abs(self.vel.x) > 15:
                self.vel.x *= -1
            elif abs(self.vel.x) < 15:
                if ouch[0].rect.centerx < self.rect.centerx:
                    self.vel.x = 15
                if ouch[0].rect.centerx > self.rect.centerx:
                    self.vel.x = -15
            if self.vel.y > 20:
                self.vel.y = 20
            self.vel.y *= -1.1
        if self.gothit or self.hittimer > 1:
            self.hittimer += 2
        if self.hittimer >= 10:
            self.gothit = False
        if self.hittimer >= 24:
            self.hittimer = 0

        elif yikes and not self.gothit and self.hittimer == 0 and not self.immune:

            self.health -= 20

            self.gothit = True
            self.immune = True
            if abs(self.vel.x) > 15:
                self.vel.x *= -1
            elif abs(self.vel.x) < 15:
                if yikes[0].rect.centerx < self.rect.centerx:
                    self.vel.x = 15
                if yikes[0].rect.centerx > self.rect.centerx:
                    self.vel.x = -15
            if self.vel.y > 20:
                self.vel.y = 20
            self.vel.y *= -1.1
        if self.gothit or self.hittimer > 1:
            self.hittimer += 2
        if self.hittimer >= 10:
            self.gothit = False
        if self.hittimer >= 24:
            self.hittimer = 0

        if not ouch and not yikes:
            self.gothit = False
            self.hittimer = 0

    # function for integrating all Lizzy's various sprites

    def integrate(self):
        legs.rect.midtop = self.rect.center
        torsooffset = vec(5, 0)
        if torso.reversed == True:
            torso.rect.center = self.rect.center - torsooffset
        else:
            torso.rect.center = self.rect.center + torsooffset
        gatling.rect.center = torso.rect.center

    # render all component sprite to the screen in correct order

    def render(self):
        if self.gothit and not self.dying:
            if self.reverse:
                screen.blit(self.hitsurf, self.rect)
            if not self.reverse:
                screen.blit(pygame.transform.flip(self.hitsurf, True, False), self.rect)

        elif self.dying:
            if self.reverse:
                screen.blit(self.deathsurf, (self.rect.centerx, (self.rect.centery + self.yoffset)))
            if not self.reverse:
                screen.blit(pygame.transform.flip(self.deathsurf, True, False),
                            (self.rect.centerx, (self.rect.centery + self.yoffset)))

        elif self.melee:

            if not self.meleereverse:

                blitplace = self.rect.center + vec(-140, -90)
                blitplace += self.blitoffset
                screen.blit(self.meleesurf, (blitplace))

            elif self.meleereverse:

                blitplace = self.rect.center + vec(-140, -90)
                blitplace += self.blitoffset
                screen.blit(pygame.transform.flip(self.meleesurf, True, False), blitplace)


        else:
            screen.blit(legs.surf, legs.rect)
            screen.blit(torso.surf, torso.rect)
            screen.blit(gatling.surf, gatling.rect)
            screen.blit(self.surf, self.rect)
        for entity in flashy:
            entity.update()

    # melee strike function:

    def whack(self, direction):

        lizpos = vec(liz.rect.center)
        mousepos = vec(pygame.mouse.get_pos())
        if mousepos.x >= lizpos.x:
            self.meleereverse = False
            self.meleestate = "right"

        if mousepos.x < lizpos.x:
            self.meleereverse = True
            self.meleestate = "left"

        if direction == "up":
            self.meleestate = "up"
        if direction == "down":
            self.meleestate = "down"

        if self.meleetimer < 3:

            if not self.grounded:
                if direction == "up":
                    liz.vel.y -= 10
                elif direction == "down":
                    liz.vel.y -= 10

                elif self.meleereverse:
                    liz.vel.x -= 15
                elif not self.meleereverse:
                    liz.vel.x += 15
        if 8 > self.meleetimer < 12:
            if not self.grounded:
                if direction == "down":

                    liz.vel.x = 0
                    liz.vel.y += 5
                    if liz.vel.y > 45:
                        liz.vel.y = 45

        if self.blink:
            self.blink = False

        if gatling.firing:
            gatling.firing = False
            gatling.spinning = False
            gatling.winddown()
        if self.meleetimer < 13:
            picindex = self.meleetimer // 2
            if direction == "side":
                self.meleesurf = Lizmelee[picindex]
            elif direction == "up":
                increment = 90 / 7
                self.meleesurf = pygame.transform.rotate(Lizmelee[picindex], (picindex * increment))
                self.blitoffset.y = (picindex * -15)
                if not self.meleereverse:
                    self.blitoffset.x = (picindex * 10)
            elif direction == "down":
                increment = (90 / 7) * -1
                self.meleesurf = pygame.transform.rotate(Lizmelee[picindex], (picindex * increment))
                self.blitoffset.y = (picindex * -15)
                if self.meleereverse:
                    self.blitoffset.x = (picindex * 10)
        else:
            if direction == "side":
                self.meleesurf = Lizmelee[6]
            elif direction == "up":
                self.meleesurf = pygame.transform.rotate(Lizmelee[6], 90)
                self.blitoffset.y = -105
                if not self.meleereverse:
                    self.blitoffset.x = 70
            elif direction == "down":
                self.meleesurf = pygame.transform.rotate(Lizmelee[6], -90)
                self.blitoffset.y = -105
                if self.meleereverse:
                    self.blitoffset.x = 70

        self.meleetimer += 1

        if self.meleetimer == 10:
            self.immune = True
            if direction == "side":
                if self.meleereverse:
                    boxpos = (-80, 0)
                    orient = "left"
                else:
                    boxpos = (140, 0)
                    orient = "right"
            elif direction == "up":
                orient = "up"
                boxpos = (0, -120)
            elif direction == "down":
                orient = "down"
                boxpos = (0, 120)
                self.groundpound = True

            hurtbox = meleehurtbox(boxpos, orient)
            allsprites.add(hurtbox)

        if self.meleetimer > 16:

            if direction == "down" and not self.grounded:
                self.meleetimer = 16

        if self.meleetimer > 16:
            self.groundpound = False
            self.melee = False
            self.meleestate = "null"
            self.meleetimer = 0
            self.immune = False
            self.blitoffset = vec(0, 0)
            if direction == "side":
                self.meleetoken[0] -= 1
            elif direction == "up":
                self.meleetoken[1] -= 1

            elif direction == "down":
                self.meleetoken[2] -= 1

    # controlling movement and actions based on keyboard and mouse input

    def move(self):
        # setting gravity if not on solid ground
        if self.grounded or self.vel.y > 45:
            self.grav.y = 0
        else:
            self.grav.y = 2

        # key input:

        key = pygame.key.get_pressed()
        self.mousekey = pygame.mouse.get_pressed()

        # select ammo type:

        if not self.ammoswitchpressed:
            for event in pygame.event.get():
                if event.type == MOUSEWHEEL:
                    ammoselect = self.ammotype
                    if event.y < 0:
                        ammoselect -= 1
                    if event.y > 0:
                        ammoselect += 1
                    if ammoselect > 2:
                        ammoselect = 0
                    if ammoselect < 0:
                        ammoselect = 2
                    if ammoselect != self.ammotype:
                        self.ammotype = ammoselect
                        self.ammoswitchpressed = True

        if self.ammoswitchpressed:
            for event in pygame.event.get():
                wheely = False
                if event.type == MOUSEWHEEL:
                    wheely = True
                if not wheely:
                    self.ammoswitchpressed = False


# firing the gatling:

        if self.mousekey[0] and not self.gothit and not self.dying and not self.melee:
            if not gatling.spinning and not self.dying:
                gatling.spinup()
            if gatling.spinning and not self.dying and self.ammo[self.ammotype] > 0:
                gatling.fire()
        if not self.mousekey[0] and gatling.spinning:
            gatling.winddown()
        if self.dying or self.gothit or self.ammo[self.ammotype] == 0 and gatling.spinning:
            gatling.winddown()
        # move left and right:
        if key[K_d] and not self.gothit and not self.dying:
            self.vel.x += self.acc.x

        if key[K_a] and not self.gothit and not self.dying:
            self.vel.x -= self.acc.x



        # setting melee token if grounded and not pressing melee button:

        if self.grounded and not self.mousekey[2]:
            self.meleetoken = [1, 1, 1]

        # melee attack:

        if self.meleestate == "left" or self.meleestate == "right":
            self.whack("side")
        elif self.meleestate == "up":
            self.whack("up")
        elif self.meleestate == "down":
            self.whack("down")

        if self.mousekey[2] and not self.gothit and not self.dying and not self.melee:
            self.melee = True

        if self.melee and self.meleestate == "null":

            lizpos = vec(liz.rect.center)
            mousepos = vec(pygame.mouse.get_pos())
            ydif = lizpos.y - mousepos.y
            xdif = lizpos.x - mousepos.x
            virtbut = "x"
            if ydif <= 0:
                if abs(ydif) > abs(xdif):
                    virtbut = "s"
            elif ydif > 0:
                if abs(ydif) > abs(xdif):
                    virtbut = "w"

            if virtbut != "w" and virtbut != "s" and self.meleetoken[0] > 0:
                self.whack("side")
            elif virtbut == "w" and self.meleetoken[1] > 0:
                self.whack("up")
            elif virtbut == "s" and self.meleetoken[2] > 0:
                self.whack("down")
            else:
                self.melee = False

        # jump:
        if self.grounded and key[K_SPACE] and not self.gothit and not self.dying:
            self.vel.y = -25

        self.surf = self.orig
        if not key[K_a] and not key[K_d]:
            key = 0
        if self.grounded:

            legs.run(int(self.vel.x), key)
        else:
            legs.airborne(int(self.vel.x))
        torso.reverse(int(self.vel.x), key)
        # adding velocity based on gravity and friction forces
        self.vel.x -= self.vel.x * self.fric
        self.vel += self.grav
        # gatling recoil force:
        if gatling.firing:
            recoil = 0
            if self.ammotype == 0:
                recoil = 1
            else:
                recoil = 2.5
            self.recoil.x = cos(radians(ref.angle)) * 0.75 * recoil

            self.recoil.y = sin(radians(ref.angle)) * -1 * recoil
            if self.grounded:
                if self.recoil.y < 2:
                    self.recoil.y = 0
                else:
                    self.pos.y -= 5
            if self.vel.y > 40 or self.vel.y < -40:
                self.recoil.y = 0
            self.vel -= self.recoil
        else:
            self.recoil = vec(0, 0)

        if self.pos.y <= 0:
            self.vel.y = 1
        # position change based on velocity
        self.pos += self.vel
        self.rect.midbottom = self.pos
        if self.vel.x < 0.1 and self.vel.x > -0.1:
            self.vel.x = 0

        if self.vel.x > 0:
            self.reverse = False
        if self.vel.x < 0:
            self.reverse = True


# creating instances of all the stuff

ref = arbiter()
liz = LizMain()
legs = Lizlegs()
torso = Liztorso()
gatling = barrels()
# cursor = Reticle()
