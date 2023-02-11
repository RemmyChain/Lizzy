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
        self.surf = pygame.surface.Surface((10,10))
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
        self.virtualposition = vec(0,0)
        self.scrollmeter = vec(0,0)
        self.xscrolling = False
        self.yscrolling = False
        self.sbleft = int(screensize[0] * 0.4)
        self.sbright = int(screensize[0] * 0.6)
        self.sbtop = int(screensize[1] * 0.4)
        self.sbbottom = int(screensize[1] * 0.7)
        self.lizpossave = vec(0,0)
        self.leveloffset = vec(0,0)
        self.virtpossave = vec(0,0)
        self.savetimer = 0

        self.peiling = vec(0,0)

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

                self.leveloffset = vec(0,0)
                self.peiling = vec(schrevel.rect.center)
                self.savetimer = 0

        if self.death:
            liz.pos = vec(self.lizpossave)

            self.scrollmeter = vec(self.virtpossave)

            liz.vel = vec(0,0)
            leveloffset = vec(schrevel.rect.center - self.peiling)

            for i in allsprites:
                i.rect.center -= leveloffset

            gatling.firing = False
            gatling.spinning = False
            gatling.animtick = 0

            liz.health = 100
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

    def virtpos(self):
        if self.xscrolling:
            self.scrollmeter.x += int(liz.vel.x)
        if self.yscrolling:
            self.scrollmeter.y += int(liz.vel.y)

        self.virtualposition = liz.pos  + self.scrollmeter
        self.virtualposition.x = int(self.virtualposition.x)
        #if liz.grounded:
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
        if (liz.pos.y >= self.sbbottom and liz.vel.y > 0 and self.virtualposition.y <= 800) or (liz.pos.y <= self.sbtop and liz.vel.y < 0 and self.virtualposition.y >= -400):
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
    def __init__(self, position):
        super().__init__()
        self.surf = pygame.surface.Surface((80, 40))
        self.surf.set_alpha(0)
        self.rect = self.surf.get_rect()
        self.offset = position
        self.timer = 0
    def update(self):
        coords = vec((liz.rect.centerx + self.offset), liz.rect.centery)
        self.rect.center = coords

        whackedbeast = pygame.sprite.spritecollide(self, enemies, False)
        if whackedbeast:
            for i in whackedbeast:
                i.gethit(self.rect.center, 5)

        self.timer += 1
        if self.timer > 5:
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
        self.error = random.randint(-1, 1) // 2
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
            pats = pygame.sprite.spritecollide(ping, enemies, False)
            if not knal and not pats:
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
        splut = pygame.sprite.spritecollide(self, enemies, False)
        if hits and not splut:
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
                hits[0].gethit(self.impactsite, self.rotation)
                # pow = spriticle(self.impactsite, self.rotation)
                # allsprites.add(pow)
            for i in range(len(hits)):
                screen.blit(hits[i].surf, hits[i].rect,)
                self.kill()

        if splut and not hits:

            for i in splut:
                i.gethit(self.impactsite, 1)
                screen.blit(i.surf, i.rect)
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
        if not self.flash:
            flash = FX.muzzleflash()
            flashy.add(flash)
            self.flash = True

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
        self.orig = pygame.Surface((50,180))
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
        self.recoil = vec(0,0)
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
            if self.immunetimer % 3 == 0:
                self.blink = True
            else:
                self.blink = False
            if self.immunetimer == 31:

                self.immunetimer = 0
                self.immune = False

  #          torso.kill()
  #          legs.kill()
  #          self.kill()

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
                elif (self.pos.y <= (hits[i].rect.top + 50)) and ((self.vel.x <= 0 and self.rect.center[0] - hits[i].rect.center[0] < 50) or (self.vel.x >= 0 and self.rect.center[0] - hits[i].rect.center[0] > -50)):
                    self.pos.y = (hits[i].rect.top + 1)
                    self.vel.y = 0
                    self.grounded = True
                else:
                    self.grounded = False


                if self.vel.y < 0:
                    if (self.vel.x <= 0 and self.rect.center[0] - hits[i].rect.center[0] < 45) or (self.vel.x >= 0 and self.rect.center[0] - hits[i].rect.center[0] > -45):
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
        if ouch:

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

        if not ouch:
            self.gothit = False
            self.hittimer = 0





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
        if self.gothit and not self.dying:
            if self.reverse:
                screen.blit(self.hitsurf, self.rect)
            if not self.reverse:
                screen.blit(pygame.transform.flip(self.hitsurf, True, False), self.rect)

        elif self.dying:
            if self.reverse:
                screen.blit(self.deathsurf, (self.rect.centerx, (self.rect.centery + self.yoffset)))
            if not self.reverse:
                screen.blit(pygame.transform.flip(self.deathsurf, True, False), (self.rect.centerx, (self.rect.centery + self.yoffset)))

        elif self.melee:
            lizpos = vec(liz.rect.center)
            mousepos = vec(pygame.mouse.get_pos())
            if mousepos.x >= lizpos.x:
                self.meleereverse = False
                blitplace = self.rect.center + vec(-140,-90)
                screen.blit(self.meleesurf, (blitplace))
            if mousepos.x < lizpos.x:
                self.meleereverse = True
                blitplace = self.rect.center + vec(-140, -90)
                screen.blit(pygame.transform.flip(self.meleesurf, True, False), blitplace)


        else:
            screen.blit(legs.surf, legs.rect)
            screen.blit(torso.surf, torso.rect)
            screen.blit(gatling.surf, gatling.rect)
            screen.blit(self.surf, self.rect)
        for entity in flashy:
            entity.update()

    def whack(self):
        if self.meleetimer < 13:
            picindex = self.meleetimer // 2
            self.meleesurf = Lizmelee[picindex]
        else:
            self.meleesurf = Lizmelee[6]
        self.meleetimer += 1

        if self.meleetimer == 10:
            if self.meleereverse:
                boxpos = -50
            else:
                boxpos = 50
            hurtbox = meleehurtbox(boxpos)
            allsprites.add(hurtbox)

        if self.meleetimer > 16:

            self.melee = False
            self.meleetimer = 0
            self.immune = False

# controlling movement and actions based on keyboard and mouse input

    def move(self):
        # setting gravity if not on solid ground
        if self.grounded or self.vel.y > 40:
            self.grav.y = 0
        else:
            self.grav.y = 2

        key = pygame.key.get_pressed()


        self.mousekey = pygame.mouse.get_pressed()
        if self.mousekey[0] and not self.gothit and not self.dying and not self.melee:
            if not gatling.spinning and not self.dying:
                gatling.spinup()
            if gatling.spinning and not self.dying:
                gatling.fire()
        if not self.mousekey[0] and gatling.spinning:
            gatling.winddown()
        if self.dying or self.gothit and gatling.spinning:
            gatling.winddown()
# move left and right:
        if key[K_d] and not self.gothit and not self.dying:
            self.vel.x += self.acc.x

        if key[K_a] and not self.gothit and not self.dying:
            self.vel.x -= self.acc.x

# melee attack:
        if self.mousekey[2] and not self.gothit and not self.dying and not self.melee:
            self.melee = True
            # self.immune = True
        if self.melee:
            self.whack()

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
            self.recoil.x = cos(radians(ref.angle)) * 1.5

            self.recoil.y = sin(radians(ref.angle)) * -2.5
            if self.grounded:
                if self.recoil.y < 2:
                    self.recoil.y = 0
                else:
                    self.pos.y -= 5
            if self.vel.y > 40 or self.vel.y < -40:
                self.recoil.y = 0
            self.vel -= self.recoil
        else:
            self.recoil = vec(0,0)

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

