import pygame
from pygame import *
import sys
import math
from math import atan2, degrees, floor

pygame.init()

flags = FULLSCREEN | DOUBLEBUF
screen = pygame.display.set_mode((0, 0), flags, 16)
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
background = pygame.image.load("bg01.jpg").convert()
running = True
vec = pygame.math.Vector2
pygame.mouse.set_visible(False)
font = pygame.font.SysFont("comicsansms", 20)
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

barrelpix = [
    pygame.image.load("barrels01.png").convert_alpha(),
    pygame.image.load("barrels02.png").convert_alpha(),
    pygame.image.load("barrels03.png").convert_alpha(),
    pygame.image.load("barrels04.png").convert_alpha(),
    pygame.image.load("barrels05.png").convert_alpha(),
    pygame.image.load("barrels06.png").convert_alpha(),
]

groundtiles = [
    pygame.image.load("groundlefttop.png").convert_alpha(),
    pygame.image.load("groundmidtop.png").convert(),
    pygame.image.load("groundbotleft.png").convert(),
    pygame.image.load("groundbotmid.png").convert(),
    pygame.transform.flip((pygame.image.load("groundlefttop.png").convert_alpha()), True, False),
    pygame.transform.flip((pygame.image.load("groundbotleft.png").convert()), True, False)
]


Lizlegstill = pygame.image.load("walkstilla.png").convert_alpha()
Liztorsostill = pygame.image.load("torso01a.png").convert_alpha()
Lizlegsair = [
    pygame.image.load("jump1.png").convert_alpha(),
    pygame.image.load("jump2.png").convert_alpha()
]
Lizlegsaireverse = [
    pygame.transform.flip((pygame.image.load("jump1.png").convert_alpha()), True, False),
    pygame.transform.flip((pygame.image.load("jump2.png").convert_alpha()), True, False)
]
Lizlegsrun = [
    pygame.image.load("walk01a.png").convert_alpha(),
    pygame.image.load("walk02a.png").convert_alpha(),
    pygame.image.load("walk03a.png").convert_alpha(),
    pygame.image.load("walk04a.png").convert_alpha(),
    pygame.image.load("walk05a.png").convert_alpha(),
    pygame.image.load("walk06a.png").convert_alpha(),
    pygame.image.load("walk07a.png").convert_alpha(),
    pygame.image.load("walk08a.png").convert_alpha(),
    pygame.image.load("walk09a.png").convert_alpha(),
    pygame.image.load("walk10a.png").convert_alpha(),
]
Lizlegsreverse = []
for i in range(len(Lizlegsrun)):
    Lizlegsreverse.append(pygame.transform.flip((Lizlegsrun[i]), True, False))

Liztorsopix = [
    pygame.image.load("torsosmall00.png").convert_alpha(),
    pygame.image.load("torsosmall01.png").convert_alpha(),
    pygame.image.load("torsosmall02.png").convert_alpha(),
    pygame.image.load("torsosmall03.png").convert_alpha(),
    pygame.image.load("torsosmall04.png").convert_alpha(),
    pygame.image.load("torsosmall05.png").convert_alpha(),
    pygame.image.load("torsosmall06.png").convert_alpha(),
    pygame.image.load("torsosmall07.png").convert_alpha(),
    pygame.image.load("torsosmall08.png").convert_alpha(),
    pygame.image.load("torsosmall09.png").convert_alpha(),
    pygame.image.load("torsosmall10.png").convert_alpha(),
    pygame.image.load("torsosmall11.png").convert_alpha(),
    pygame.image.load("torsosmall12.png").convert_alpha(),
    pygame.image.load("torsosmall13.png").convert_alpha(),
    pygame.image.load("torsosmall14.png").convert_alpha(),
    pygame.image.load("torsosmall15.png").convert_alpha(),
]
Liztorsoreverse = []
for i in range(len(Liztorsopix)):
    Liztorsoreverse.append(pygame.transform.flip((Liztorsopix[i]), True, False))

def basicplatformconstructor(position, size):
    size -= 2
    if size < 0:
        size = 0
    blockpos = vec(position)
    leftcorner = basicplatformblock(groundtiles, 0, blockpos, True)
    allsprites.add(leftcorner)
    platforms.add(leftcorner)

    for i in range(size):
        blockpos.x += 100
        midblock = basicplatformblock(groundtiles, 1, blockpos , True)
        allsprites.add(midblock)
        platforms.add(midblock)

    blockpos.x += 100
    rightcorner = basicplatformblock(groundtiles, 4, blockpos , True)
    allsprites.add(rightcorner)
    platforms.add(rightcorner)

    while blockpos.y < 1024:
        blockpos.x -= ((size + 1) * 100)
        blockpos.y += 100

        leftwall = basicplatformblock(groundtiles, 2, blockpos, False)
        allsprites.add(leftwall)

        for i in range(size):
            blockpos.x += 100
            midfill = basicplatformblock(groundtiles, 3, blockpos, False)
            allsprites.add(midfill)

        blockpos.x += 100
        rightwall = basicplatformblock(groundtiles, 5, blockpos, False)
        allsprites.add(rightwall)





class basicplatformblock(pygame.sprite.Sprite):
    def __init__(self, imageset, index, position, hardtop):
        super().__init__()
        self.surf = imageset[index]
        self.rect = self.surf.get_rect()
        self.rect.topleft = position
        self.hardtop = hardtop
    def update(self):
        screen.blit(self.surf, self.rect)


class arbiter():
    def __init__(self):
        self.angle = 0
        self.death = False
    def update(self):
        self.angleget()
        self.scroll()
    def angleget(self):
        lizpos = vec(liz.rect.center)
        difference = vec(lizpos - cursor.pos)
        self.angle = round((degrees(atan2(difference.x, difference.y)) + 90), 2)
        if self.angle < 0:
            self.angle += 360
    def scroll(self):
        if (liz.pos.x >= 800 and liz.vel.x > 0) or (liz.pos.x <= 700 and liz.vel.x < 0):
            for entity in allsprites:
                position = list(entity.rect.center)
                position[0] -= int(liz.vel.x)
                entity.rect.center = position
            liz.pos.x -= liz.vel.x




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
        # if self.frame < 0:
        #   self.frame == 0


        rotateangle = round((theangle - (22.5 * self.frame)), 2)
        # rotateangle = 0
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
        self.pos = vec(100, 1000)
        self.fric = 0.2
        self.grounded = False

    def deathcheck(self):
        if self.pos.y > 2000:
            ref.death = True
            torso.kill()
            legs.kill()
            self.kill()

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


    def update(self):
        self.groundcheck()
        self.move()
        self.integrate()
        self.render()
        self.deathcheck()
        torso.update()
        gatling.rotate()

    def integrate(self):
        legs.rect.midtop = self.rect.center

        torsooffset = vec(5,0)
        if torso.reversed == True:
            torso.rect.center = self.rect.center - torsooffset

        else:
            torso.rect.center = self.rect.center + torsooffset
        gatling.rect.center = torso.rect.center



    def render(self):
        screen.blit(legs.surf, legs.rect)
        screen.blit(torso.surf, torso.rect)
        screen.blit(gatling.surf, gatling.rect)
        screen.blit(self.surf, self.rect)

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


liz = LizMain()
legs = Lizlegs()
torso = Liztorso()
gatling = barrels()
cursor = Reticle()
ref = arbiter()


allsprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

basicplatformconstructor((400,800), 5)
basicplatformconstructor((1000,900), 2)
basicplatformconstructor((1700,900), 2)
basicplatformconstructor((2600,200), 2)
basicplatformconstructor((2300,400), 2)
basicplatformconstructor((2400,600), 3)
basicplatformconstructor((2200,800), 5)
basicplatformconstructor((0,1000), 15)
basicplatformconstructor((2000,1000), 10)

while running:

    screen.blit(background, (0, 0))

    ref.update()
    for entity in allsprites:
        entity.update()
    liz.update()
    cursor.update()


    terminal = font.render("angle: " + str(ref.angle), True, ("black"))
    frame = font.render("frame number: " + str(torso.frame), True, ("black"))
    rotangle = font.render("rotation angle: " + str(torso.anglecheck), True, ("black"))
    lizvelocity = font.render("Lizzy velocity: " + str(liz.vel), True, ("black"))
    lizposition = font.render("Lizzy position: " + str(liz.pos), True, ("black"))
    screen.blit(terminal, (20, 20))
    screen.blit(lizposition, (20,40))
    screen.blit(lizvelocity, (20, 60))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    key = pygame.key.get_pressed()
    if key[K_ESCAPE]:
        running = False

    if ref.death == True:
        running = False

    pygame.time.Clock().tick(30)


pygame.quit()
sys.exit()




