# a simple construction function building square platforms out of 100 x 100 sprite blocks
from math import sin, radians, cos, pi
from random import randint

from enemies import kamaker
from fx import groundimpact, spriticle
from images import groundtiles, rocktile, decals, groundblocks
from initialising import (
    vec,
    allsprites,
    platforms,
    screen,
    hardblocks,
    enemies,
    depthbg, mobs,
)
import pygame as pg

from lizzy import liz, gatling


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
        midblock = basicplatformblock(groundtiles, 1, blockpos, True)
        allsprites.add(midblock)
        platforms.add(midblock)

    blockpos.x += 100
    rightcorner = basicplatformblock(groundtiles, 4, blockpos, True)
    allsprites.add(rightcorner)
    platforms.add(rightcorner)

    while blockpos.y < 1024:
        blockpos.x -= (size + 1) * 100
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


class decal(pg.sprite.Sprite):
    def __init__(self, placement):
        super().__init__()
        randomimg = randint(0, 5)
        self.surf = decals[randomimg]
        self.rect = self.surf.get_rect()
        self.rect.midbottom = placement

    def update(self):
        screen.blit(self.surf, self.rect)


# a constructor for sprite level building blocks used in the above constructor


class basicplatformblock(pg.sprite.Sprite):
    def __init__(self, imageset, index, position, hardtop):
        super().__init__()
        self.image = imageset[index]
        self.surf = pg.surface.Surface((100, 100), pg.SRCALPHA)

        self.rect = self.surf.get_rect()
        self.rect.topleft = position
        self.hardtop = hardtop
        self.hole = pg.surface.Surface((20, 20))
        self.hole.fill(("black"))
        self.hole.set_alpha(0)
        self.surf.blit(self.image, (0, 0))

        # adding some decoration

        if hardtop:
            chance = randint(0, 5)
            if chance == 0:
                planty = decal(self.rect.midtop)
                allsprites.add(planty)

    def update(self):
        self.surf.blit(self.hole, (20, 20))
        screen.blit(self.surf, self.rect)

    # check if player is standing on block
    def playercheck(self):
        if self.hardtop:
            hits = pg.sprite.spritecollide(self, mobs, False)

            if hits:
                for i in hits:
                    if i.pos.y <= (self.rect.top + 50):
                        i.pos.y = self.rect.top + 1
                        i.vel.y = 0
                        i.grounded = True


# hard block class (blocks player movement and normal attacks, also is a platform)


class hardblock(pg.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.surf = image
        self.rect = self.surf.get_rect()
        self.rect.topleft = position

    def update(self):
        screen.blit(self.surf, self.rect)

    # check if player is standing on block
    def playercheck(self):
        hits = pg.sprite.spritecollide(self, mobs, False)

        if hits:
            for i in hits:
                revert = i.pos.x - i.vel.x
                reverty = i.pos.y - i.vel.y
                if i.vel.y > 25:
                    i.rect.bottom = self.rect.top

                if (
                        i.rect.bottom + 10 > self.rect.center[1] > i.rect.top - 10
                ):
                    i.pos.x = revert
                    i.rect.midbottom = i.pos
                elif (i.pos.y <= (self.rect.top + 50)) and (
                    (i.vel.x <= 0 and i.rect.center[0] - self.rect.center[0] < 50)
                    or (i.vel.x >= 0 and i.rect.center[0] - self.rect.center[0] > -50)
                ):
                    i.pos.y = self.rect.top + 1
                    i.vel.y = 0
                    i.grounded = True
                else:
                    i.grounded = False

                if i.vel.y < 0:
                    if (
                        i.vel.x <= 0 and i.rect.center[0] - self.rect.center[0] < 45
                    ) or (
                        i.vel.x >= 0 and i.rect.center[0] - self.rect.center[0] > -45
                    ):
                        i.vel.y = 0
                        i.pos.y = reverty

    def gethit(self, impactsite, rotation, angle):
        chance = 0
        if liz.ammotype == 1:
            chance = randint(0, 2)
        elif liz.ammotype == 2:
            chance = 0
        elif liz.ammotype == 0:
            chance = randint(0, 1)
        if chance != 0:
            if liz.ammotype != 2:
                pow = spriticle(impactsite, rotation)
                allsprites.add(pow)


class groundblock(pg.sprite.Sprite):
    def __init__(self, orient, pos):
        super().__init__()
        self.treaded = False
        self.type = orient

        if self.type == "top":
            self.surf = groundblocks[0]
        elif self.type == "mid":
            rando = randint(0, 3)
            if rando == 0:
                self.surf = groundblocks[1]
            elif rando == 1:
                self.surf = pg.transform.flip(groundblocks[1], True, False)
            elif rando == 2:
                self.surf = pg.transform.flip(groundblocks[1], False, True)
            elif rando == 3:
                self.surf = pg.transform.flip(groundblocks[1], True, True)
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
        elif self.type == "corner":
            self.surf = groundblocks[8]
        elif self.type == "edge":
            randy = randint(0, 1)
            if randy == 0:
                self.surf = groundblocks[9]
            else:
                self.surf = pg.transform.flip(groundblocks[9], False, True)
        elif self.type == "tallslant":
            self.surf = groundblocks[10]
        elif self.type == "cornerreverse":
            self.surf = groundblocks[11]
        elif self.type == "edgereverse":
            randa = randint(0, 1)
            if randa == 0:
                self.surf = groundblocks[12]
            else:
                self.surf = pg.transform.flip(groundblocks[12], False, True)
        elif self.type == "tallslantreverse":
            self.surf = groundblocks[13]
        self.rect = self.surf.get_rect()
        self.rect.midbottom = pos
        self.towerstart = vec(pos)
        while self.towerstart.y < 1200:
            self.towerstart.y += 100
            if (
                self.type != "corner"
                and self.type != "cornerreverse"
                and self.type != "edge"
                and self.type != "edgereverse"
            ):
                fillblock = groundblock("mid", self.towerstart)
                hardblocks.add(fillblock)
                allsprites.add(fillblock)
            elif self.type == "corner":
                fillblock = groundblock("edge", self.towerstart)
                hardblocks.add(fillblock)
                allsprites.add(fillblock)
            elif self.type == "cornerreverse":
                fillblock = groundblock("edgereverse", self.towerstart)
                hardblocks.add(fillblock)
                allsprites.add(fillblock)

        plantchance = randint(0, 5)
        if plantchance == 0:
            if (
                self.type == "top"
                or self.type == "corner"
                or self.type == "cornerreverse"
            ):
                plantje = decal(self.rect.midtop)
                allsprites.add(plantje)
            elif (
                self.type != "mid"
                and self.type != "edge"
                and self.type != "edgereverse"
            ):
                plantje = decal(self.rect.center)
                allsprites.add(plantje)

    def gethit(self, impact, rotation, angle):
        if liz.ammotype != 2:
            normalchance = randint(0, 1)
            hyperchance = randint(0, 2)
            if (
                self.type == "edge"
                or self.type == "edgereverse"
                or self.type == "corner"
                or self.type == "cornerreverse"
                or self.type == "top"
            ):
                if (liz.ammotype == 0 and normalchance == 0) or (
                    liz.ammotype == 1 and hyperchance == 0
                ):
                    pief = groundimpact(impact, angle)
                    allsprites.add(pief)
            else:
                orig = vec(impact)
                finder = vec(impact)
                xin = finder.x - self.rect.left
                threshold = self.thresholder(xin, self.type)
                while (
                    finder.y < threshold
                    and abs(finder.y - orig.y) < 100
                    and abs(finder.x - orig.x) < 100
                ):
                    finder.x += sin(radians(angle)) * 10
                    finder.y += cos(radians(angle)) * 10
                    xin = finder.x - self.rect.left
                    threshold = self.thresholder(xin, self.type)
                if finder.y >= threshold:
                    if (liz.ammotype == 0 and normalchance == 0) or (
                        liz.ammotype == 1 and hyperchance == 0
                    ):
                        pief = groundimpact(finder, angle)
                        allsprites.add(pief)

    def thresholder(self, xinput, type):
        xcor = xinput
        degree = pi / 400
        degreecor = xcor * degree + pi
        threshold0 = 0
        if type == "flattop":
            threshold0 = self.rect.top
        elif type == "startramp":
            threshold0 = self.rect.bottom - (cos(degreecor) + 1) * 100

        elif type == "startrampreverse":
            threshold0 = self.rect.bottom - (cos(degreecor - pi / 2) + 1) * 100

        elif type == "slant":
            threshold0 = self.rect.bottom - xcor / 2

        elif type == "slantreverse":
            threshold0 = self.rect.bottom - (200 - xcor) / 2

        elif type == "tallslant":
            threshold0 = self.rect.bottom - xcor

        elif type == "tallslantreverse":
            threshold0 = self.rect.bottom - (200 - xcor)

        elif type == "stopramp":
            threshold0 = self.rect.bottom - (cos(degreecor + pi / 2)) * 100

        elif type == "stoprampreverse":
            threshold0 = self.rect.bottom - (cos(degreecor - pi)) * 100
        return threshold0

    def topcheck(self, type):
        xcor = liz.rect.centerx - self.rect.left
        threshold = self.thresholder(xcor, type)

        tik = pg.sprite.collide_rect(self, liz)
        if tik:
            if liz.vel.y > 25:
                liz.rect.bottom = threshold + 1

            if (threshold + 50) > liz.rect.bottom > threshold:
                if self.type != "mid":
                    liz.rect.bottom = threshold + 1
                else:
                    liz.rect.bottom = threshold - 1
                liz.pos.y = liz.rect.bottom
                if not gatling.firing:
                    liz.vel.y = 15
                liz.grounded = True
                self.treaded = True
        if not tik and self.treaded:
            self.treaded = False

    def leftcheck(self):
        tik = pg.sprite.collide_rect(self, liz)
        if tik and not self.treaded:
            if liz.rect.right > self.rect.centerx:
                liz.rect.right = self.rect.right
                liz.pos = vec(liz.rect.midbottom)
                liz.vel.x = 0

    def rightcheck(self):
        tik = pg.sprite.collide_rect(self, liz)
        if tik and not self.treaded:
            if liz.rect.left < self.rect.centerx:
                liz.rect.left = self.rect.right
                liz.pos = vec(liz.rect.midbottom)
                liz.vel.x = 0

    def update(self):
        screen.blit(self.surf, self.rect)

    def playercheck(self):
        tik = pg.sprite.collide_rect(self, liz)
        if not tik:
            self.treaded = False
        if self.type == "top" or self.type == "mid":
            self.topcheck("flattop")
        elif self.type == "corner":
            if tik and liz.rect.bottom < self.rect.top + 70:
                self.topcheck("flattop")
            self.leftcheck()
        elif self.type == "cornerreverse":
            if tik and liz.rect.bottom < self.rect.top + 70:
                self.topcheck("flattop")
            self.rightcheck()

        elif self.type == "edge":
            self.leftcheck()
        elif self.type == "edgereverse":
            self.rightcheck()

        elif self.type == "startramp":
            self.topcheck("startramp")

        elif self.type == "startrampreverse":
            self.topcheck("startrampreverse")

        elif self.type == "slant":
            self.topcheck("slant")

        elif self.type == "slantreverse":
            self.topcheck("slantreverse")

        elif self.type == "stopramp":
            self.topcheck("stopramp")

        elif self.type == "stoprampreverse":
            self.topcheck("stoprampreverse")

        elif self.type == "tallslant":
            self.topcheck("tallslant")

        elif self.type == "tallslantreverse":
            self.topcheck("tallslantreverse")

            # self.rightcheck()


def hardblockplacement(hbcoords, image):
    for i in range(len(hbcoords)):
        hblock = hardblock(image, hbcoords[i])
        # platforms.add(hblock)
        hardblocks.add(hblock)
        allsprites.add(hblock)


def groundconstructor(list):
    for block in list:
        ground = groundblock(block[0], block[1])
        allsprites.add(ground)
        hardblocks.add(ground)


# generating a level

hardblocklist = [
    (200, 600),
    (300, 600),
    (0, 900),
    (0, 800),
    (0, 700),
    (0, 600),
    (100, 600),
    (600, 700),
]

basicplatformconstructor((400, 800), 5)
basicplatformconstructor((1000, 900), 2)
basicplatformconstructor((1700, 900), 2)
basicplatformconstructor((2600, 200), 2)
basicplatformconstructor((2300, 400), 2)
basicplatformconstructor((2400, 600), 3)
basicplatformconstructor((2200, 800), 5)
basicplatformconstructor((0, 1000), 15)
basicplatformconstructor((2000, 1000), 10)

groundlist = [
    ["corner", (3150, 1100)],
    ["top", (3300, 1100)],
    ["startramp", (3500, 1000)],
    ["slant", (3700, 900)],
    ["stopramp", (3900, 800)],
    ["top", (4100, 800)],
    ["tallslant", (4300, 700)],
    ["stopramp", (4500, 500)],
    ["cornerreverse", (4650, 500)],
    ["corner", (4850, 600)],
    ["stoprampreverse", (5000, 600)],
    ["tallslantreverse", (5200, 800)],
    ["startrampreverse", (5400, 900)],
    ["top", (5600, 1000)],
    ["cornerreverse", (5750, 1000)],
]

groundconstructor(groundlist)


hardblockplacement(hardblocklist, rocktile)

kamaker1 = kamaker((1000, 600))
kamaker2 = kamaker((2200, 600))
enemies.add(kamaker1)
enemies.add(kamaker2)
allsprites.add(kamaker1)
allsprites.add(kamaker2)


depthcenter = vec(screen.get_size()) / 2
depth = depthbg(depthcenter)
