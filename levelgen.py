import pygame
from initialising import *
from images import *
from enemies import *
from FX import *
from Lizzy import *


# a simple construction function building square platforms out of 100 x 100 sprite blocks


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

# a constructor for sprite level building blocks used in the above constructor

class basicplatformblock(pygame.sprite.Sprite):
    def __init__(self, imageset, index, position, hardtop):
        super().__init__()
        self.image = (imageset[index])
        self.surf = pygame.surface.Surface ((100,100), pygame.SRCALPHA)
        
        self.rect = self.surf.get_rect()
        self.rect.topleft = position
        self.hardtop = hardtop
        self.hole = pygame.surface.Surface ((20,20))
        self.hole.fill(("black"))
        self.hole.set_alpha(0)
        self.surf.blit(self.image, (0, 0))
    def update(self):
        if self.hardtop:
            self.playercheck()
        self.surf.blit(self.hole, (20,20))
        screen.blit(self.surf, self.rect)

    # check if player is standing on block
    def playercheck(self):

        hits = pygame.sprite.collide_rect(self, liz)

        if hits:
            if liz.pos.y <= (self.rect.top + 50):
                liz.pos.y = (self.rect.top + 1)
                liz.vel.y = 0
                liz.grounded = True
            else:
                liz.grounded = False


# hard block class (blocks player movement and normal attacks, also is a platform)

class hardblock(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.surf = image
        self.rect = self.surf.get_rect()
        self.rect.topleft = position
    def update(self):
        self.playercheck()
        screen.blit(self.surf, self.rect)

    # check if player is standing on block
    def playercheck(self):

        hits = pygame.sprite.collide_rect(self, liz)

        if hits:
            revert = liz.pos.x - liz.vel.x
            reverty = liz.pos.y - liz.vel.y

            if self.rect.center[1] < liz.rect.bottom + 10 and self.rect.center[1] > liz.rect.top - 10:
                liz.pos.x = revert
                liz.rect.midbottom = liz.pos
            elif (liz.pos.y <= (self.rect.top + 50)) and (
                    (liz.vel.x <= 0 and liz.rect.center[0] - self.rect.center[0] < 50) or (
                    liz.vel.x >= 0 and liz.rect.center[0] - self.rect.center[0] > -50)):
                liz.pos.y = (self.rect.top + 1)
                liz.vel.y = 0
                liz.grounded = True
            else:
                liz.grounded = False

            if liz.vel.y < 0:
                if (liz.vel.x <= 0 and liz.rect.center[0] - self.rect.center[0] < 45) or (
                        liz.vel.x >= 0 and liz.rect.center[0] - self.rect.center[0] > -45):
                    liz.vel.y = 0
                    liz.pos.y = reverty

    def gethit(self, impactsite, rotation):
        if liz.ammotype == 1:
            chance = random.randint(0, 3)
        elif liz.ammotype == 2:
            chance = 0
        elif liz.ammotype == 0:
            chance = random.randint(0, 2)
        if chance != 0:
            if liz.ammotype != 2:
                pow = spriticle(impactsite, rotation)
                allsprites.add(pow)
            elif liz.ammotype == 2:
                poef = explosive(impactsite)
                allsprites.add(poef)

class groundblock(pygame.sprite.Sprite):
    def __init__(self, orient, pos):
        super().__init__()
        self.treaded = False
        self.type = orient
        if self.type == "top":
            self.surf = groundblocks[0]
        elif self.type == "mid":
            rando = random.randint(0, 3)
            if rando == 0:
                self.surf = groundblocks[1]
            elif rando == 1:
                self.surf = pygame.transform.flip(groundblocks[1], True, False)
            elif rando == 2:
                self.surf = pygame.transform.flip(groundblocks[1], False, True)
            elif rando == 3:
                self.surf = pygame.transform.flip(groundblocks[1], True, True)
        elif self.type == "startramp":
            self.surf = groundblocks[2]
        elif self.type == "slant":
            self.surf = groundblocks[3]
        elif self.type == "stopramp":
            self.surf = groundblocks[4]
        elif self.type == "startrampreverse":
            self.surf = groundblocks[5]
        elif self.type == "slantreverse":
            self.surf = groundblocks[6]
        elif self.type == "stoprampreverse":
            self.surf = groundblocks[7]
        self.rect = self.surf.get_rect()
        self.rect.midbottom = pos
        self.towerstart = vec(pos)
        while self.towerstart.y < 1200:
            self.towerstart.y += 100
            fillblock = groundblock("mid", self.towerstart)
            hardblocks.add(fillblock)
            allsprites.add(fillblock)

    def gethit(self, impact, rotation):
        pass

    def topcheck(self, type):
        xcor = liz.rect.centerx - self.rect.left
        degree = pi / 400
        degreecor = xcor * degree + pi
        if type == "flattop":
            threshold = self.rect.top
        elif type == "startramp":

            threshold = self.rect.bottom - (cos(degreecor) + 1) * 100

        elif type == "slant":
            threshold = self.rect.bottom - xcor / 2

        elif type == "stopramp":
            threshold = self.rect.bottom - (cos(degreecor + pi / 2)) * 100

        tik = pygame.sprite.collide_rect(self, liz)
        if tik:
            origin = vec(liz.rect.center - liz.vel)
            if liz.rect.bottom > threshold and \
                    (abs(origin.y - self.rect.centery) > abs(origin.x - self.rect.centerx) or self.treaded):

                liz.rect.bottom = threshold + 1
                liz.pos.y = liz.rect.bottom
                if not gatling.firing:
                    liz.vel.y = 10
                liz.grounded = True
                self.treaded = True

    def leftcheck(self):

        tik = pygame.sprite.collide_rect(self, liz)
        if tik and not self.treaded:
            origin = vec(liz.rect.center - liz.vel)
            if liz.rect.right < self.rect.centerx and \
                    abs(origin.y - self.rect.centery) < abs(origin.x - self.rect.centerx) and \
                    liz.rect.bottom > self.rect.top:
                liz.pos -= liz.vel
                liz.vel.x = 0


    def rightcheck(self):
        tik = pygame.sprite.collide_rect(self, liz)
        if tik and not self.treaded:
            origin = vec(liz.rect.center - liz.vel)
            if liz.rect.right < self.rect.centerx and \
                    abs(origin.y - self.rect.centery) < abs(origin.x - self.rect.centerx) and \
                    liz.rect.bottom > self.rect.top:
                liz.pos -= liz.vel
                liz.vel.x = 0

    def update(self):
        tik = pygame.sprite.collide_rect(self, liz)
        if not tik:
            self.treaded = False
        screen.blit(self.surf, self.rect)
        if self.type == "top" or self.type == "mid":
            self.topcheck("flattop")
            self.leftcheck()
            self.rightcheck()
        elif self.type == "startramp":
            self.topcheck("startramp")

        elif self.type == "slant":
            self.topcheck("slant")

        elif self.type == "stopramp":
            self.topcheck("stopramp")

            # self.rightcheck()

def hardblockplacement(hbcoords, image):
    for i in range(len(hbcoords)):
        hblock = hardblock(image, hbcoords[i])
        # platforms.add(hblock)
        hardblocks.add(hblock)
        allsprites.add(hblock)

# generating a level

hardblocklist = [
    (200,600),
    (300,600),
    (0,900),
    (0,800),
    (0,700),
    (0,600),
    (100,600),
    (600,700)
]

basicplatformconstructor((400,800), 5)
basicplatformconstructor((1000,900), 2)
basicplatformconstructor((1700,900), 2)
basicplatformconstructor((2600,200), 2)
basicplatformconstructor((2300,400), 2)
basicplatformconstructor((2400,600), 3)
basicplatformconstructor((2200,800), 5)
basicplatformconstructor((0,1000), 15)
basicplatformconstructor((2000,1000), 10)

ground = groundblock("top", (3300, 1100))
allsprites.add(ground)
hardblocks.add(ground)
ground1 = groundblock("startramp", (3500, 1000))
allsprites.add(ground1)
hardblocks.add(ground1)
ground2 = groundblock("slant", (3700, 900))
allsprites.add(ground2)
hardblocks.add(ground2)
ground3 = groundblock("stopramp", (3900, 800))
allsprites.add(ground3)
hardblocks.add(ground3)
ground4 = groundblock("top", (4100, 800))
allsprites.add(ground4)
hardblocks.add(ground4)


hardblockplacement(hardblocklist, rocktile)

kamaker1 = kamaker((1000, 600))
kamaker2 = kamaker((2200, 600))
enemies.add(kamaker1)
enemies.add(kamaker2)
allsprites.add(kamaker1)
allsprites.add(kamaker2)

depthcenter = vec(screen.get_size()) / 2
depth = depthbg(depthcenter)
