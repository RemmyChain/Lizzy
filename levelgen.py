import pygame
from initialising import *
from images import *
from enemies import *
from FX import *


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
        self.surf.blit(self.hole, (20,20))
        screen.blit(self.surf, self.rect)

# hard block class (blocks player movement and normal attacks, also is a platform)

class hardblock(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.surf = image
        self.rect = self.surf.get_rect()
        self.rect.topleft = position
    def update(self):
        screen.blit(self.surf, self.rect)
    def gethit(self, impactsite, rotation):
        if liz.ammotype == 1:
            chance = random.randint(0, 4)
        else:
            chance = random.randint(0, 2)
        if chance == 0:
            pow = spriticle(impactsite, rotation)
            allsprites.add(pow)

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

hardblockplacement(hardblocklist, rocktile)

kamaker1 = kamaker((1000, 600))
kamaker2 = kamaker((2200, 600))
enemies.add(kamaker1)
enemies.add(kamaker2)
allsprites.add(kamaker1)
allsprites.add(kamaker2)
