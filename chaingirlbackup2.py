import pygame
from pygame import *
import sys
import math
from math import atan2, degrees

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
background = pygame.image.load("bg01.jpg")
running = True
vec = pygame.math.Vector2
pygame.mouse.set_visible(False)
font = pygame.font.SysFont("comicsansms", 20)

Lizlegstill = pygame.image.load("walkstilla.png")
Liztorsostill = pygame.image.load("torso01a.png")
Lizlegsrun = [
    pygame.image.load("walk01a.png"),
    pygame.image.load("walk02a.png"),
    pygame.image.load("walk03a.png"),
    pygame.image.load("walk04a.png"),
    pygame.image.load("walk05a.png"),
    pygame.image.load("walk06a.png"),
    pygame.image.load("walk07a.png"),
    pygame.image.load("walk08a.png"),
    pygame.image.load("walk09a.png"),
    pygame.image.load("walk10a.png"),
]
Lizlegsreverse = []
for i in range(len(Lizlegsrun)):
    Lizlegsreverse.append(pygame.transform.flip((Lizlegsrun[i]), True, False))

Liztorsopix = [
    pygame.image.load("torsosmall00.png"),
    pygame.image.load("torsosmall01.png"),
    pygame.image.load("torsosmall02.png"),
    pygame.image.load("torsosmall03.png"),
    pygame.image.load("torsosmall04.png"),
    pygame.image.load("torsosmall05.png"),
    pygame.image.load("torsosmall06.png"),
    pygame.image.load("torsosmall07.png"),
    pygame.image.load("torsosmall08.png"),
    pygame.image.load("torsosmall09.png"),
    pygame.image.load("torsosmall10.png"),
    pygame.image.load("torsosmall11.png"),
    pygame.image.load("torsosmall12.png"),
    pygame.image.load("torsosmall13.png"),
    pygame.image.load("torsosmall14.png"),
]
Liztorsoreverse = []
for i in range(len(Liztorsopix)):
    Liztorsoreverse.append(pygame.transform.flip((Liztorsopix[i]), True, False))

class arbiter():
    def __init__(self):
        self.angle = 0
    def update(self):
        self.angleget()
    def angleget(self):
        lizpos = vec(liz.rect.center)
        difference = vec(lizpos - cursor.pos)
        self.angle = round((degrees(atan2(difference.x, difference.y)) + 90), 2)
        if self.angle < 0:
            self.angle += 360



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

class Lizlegs(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = Lizlegstill
        self.rect = self.surf.get_rect()
        self.runtimer = 0
        self.runanim = []
        self.reverse = False

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

        self.surf = self.runanim[self.frame]
        if speed == 0:
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

    def update(self):

        theangle = ref.angle

        if self.reversed == False:
            self.aim = Liztorsopix

        if self.reversed == True:
            self.aim = Liztorsoreverse
            theangle = 360 - (ref.angle + 180)
            if theangle >= 360:
                theangle -= 360

        self.frame = int((theangle + 15) / 24)
        if self.frame == 15:
            self.frame = 14
        self.surf = self.aim[self.frame]


    def reverse(self, speed):
        if speed < 0:
            self.reversed = True
        if speed > 0:
            self.reversed = False



class LizMain(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.orig = pygame.Surface((100,180))
        self.orig.fill("red")
        self.orig.set_alpha(0)
        self.surf = self.orig
        self.rect = self.surf.get_rect()
        self.rect.bottomleft = (100, 1000)
        self.acc = vec(3, 0)
        self.vel = vec(0, 0)
        self.pos = vec(100, 1000)
        self.fric = 0.2
        self.resist = vec(0, 0)

    def update(self):
        self.move()
        self.integrate()
        self.render()
        torso.update()

    def integrate(self):
        legs.rect.midtop = self.rect.center

        torsooffset = vec(5,0)
        if torso.reversed == True:
            torso.rect.center = self.rect.center - torsooffset
        else:
            torso.rect.center = self.rect.center + torsooffset

    def render(self):
        screen.blit(legs.surf, legs.rect)
        screen.blit(torso.surf, torso.rect)
        screen.blit(self.surf, self.rect)

    def move(self):
        key = pygame.key.get_pressed()
        if key[K_d]:

            self.vel += self.acc

        if key[K_a]:

            self.vel -= self.acc


        if self.vel.x != 0:
            self.surf = self.orig
            legs.run(int(self.vel.x))
            torso.reverse(int(self.vel.x))
            if self.vel.x < 0.01 and self.vel.x > -0.01:
                self.vel.x = 0


        self.resist = self.fric * self.vel
        self.vel -= self.resist
        self.pos += self.vel
        self.rect.bottomleft = self.pos


liz = LizMain()
legs = Lizlegs()
torso = Liztorso()
cursor = Reticle()
ref = arbiter()


allsprites = pygame.sprite.Group()
allsprites.add(liz)
allsprites.add(cursor)

while running:

    screen.blit(background, (0, 0))
    for entity in allsprites:
        entity.update()
    ref.update()


    terminal = font.render(str(ref.angle), True, ("black"))
    screen.blit(terminal, (20, 20))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    key = pygame.key.get_pressed()
    if key[K_ESCAPE]:
        running = False

    pygame.time.Clock().tick(30)


pygame.quit()
sys.exit()




