import pygame
from pygame import *
import sys

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
background = pygame.image.load("bg01.jpg")
running = True
vec = pygame.math.Vector2

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
    def reverse(self, speed):
        if speed < 0:
            self.surf = pygame.transform.flip(Liztorsostill, True, False)
        if speed > 0:
            self.surf = Liztorsostill



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

    def integrate(self):
        legs.rect.midtop = self.rect.center

        torso.rect.center = self.rect.center

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

        if self.vel.x == 0:
            legs.surf = Lizlegstill


        self.resist = self.fric * self.vel
        self.vel -= self.resist
        self.pos += self.vel
        self.rect.bottomleft = self.pos


liz = LizMain()
legs = Lizlegs()
torso = Liztorso()


allsprites = pygame.sprite.Group()
allsprites.add(liz)


while running:

    screen.blit(background, (0, 0))
    for entity in allsprites:
        entity.update()


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




