import pygame
import os

Lizhit = pygame.image.load(os.path.join("images", "lizhit.png")).convert_alpha()

crocwalk = [
    pygame.image.load(os.path.join("images", "crocwalk0000.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocwalk0001.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocwalk0002.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocwalk0003.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocwalk0004.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocwalk0005.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocwalk0006.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocwalk0007.png")).convert_alpha(),
]

crocrotate = [
    pygame.image.load(os.path.join("images", "crocrotate0000.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocrotate0001.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocrotate0002.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocrotate0003.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocrotate0004.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocrotate0005.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocrotate0006.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocrotate0007.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocrotate0008.png")).convert_alpha(),
]

crocdeath = [
    pygame.image.load(os.path.join("images", "crocdeath0000.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocdeath0001.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocdeath0002.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocdeath0003.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocdeath0004.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocdeath0005.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocdeath0006.png")).convert_alpha(),
]

crocflamedeath = [
    pygame.image.load(os.path.join("images", "crocflamedeath0000.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocflamedeath0001.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocflamedeath0002.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocflamedeath0003.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocflamedeath0004.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocflamedeath0005.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocflamedeath0006.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocflamedeath0007.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocflamedeath0008.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocflamedeath0009.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocflamedeath0010.png")).convert_alpha(),
]

crocextra = [
    pygame.image.load(os.path.join("images", "crocxarm.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocxhead.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocxhose.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "crocxtorso.png")).convert_alpha(),
]

decals = [
    pygame.image.load(os.path.join("images", "jarichblue.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "jarichpoppy.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "jarichsunflower.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "jarichtree.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "jarichshrub.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "jarichshrub2.png")).convert_alpha(),
]

groundblocks = [
    pygame.image.load(os.path.join("images", "groundboxstraight.png")).convert(),
    pygame.image.load(os.path.join("images", "groundboxstraightmid.png")).convert(),
    pygame.image.load(os.path.join("images", "groundboxupramp.png")).convert_alpha(),
    pygame.image.load(
        os.path.join("images", "groundboxstraightramp.png")
    ).convert_alpha(),
    pygame.image.load(os.path.join("images", "groundboxdownramp.png")).convert_alpha(),
    pygame.transform.flip(
        (
            pygame.image.load(
                os.path.join("images", "groundboxupramp.png")
            ).convert_alpha()
        ),
        True,
        False,
    ),
    pygame.transform.flip(
        (
            pygame.image.load(
                os.path.join("images", "groundboxstraightramp.png")
            ).convert_alpha()
        ),
        True,
        False,
    ),
    pygame.transform.flip(
        (
            pygame.image.load(
                os.path.join("images", "groundboxdownramp.png")
            ).convert_alpha()
        ),
        True,
        False,
    ),
    pygame.image.load(os.path.join("images", "groundboxcorner.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "groundboxedge.png")).convert(),
    pygame.image.load(
        os.path.join("images", "groundboxstraightramptall.png")
    ).convert_alpha(),
    pygame.transform.flip(
        (
            pygame.image.load(
                os.path.join("images", "groundboxcorner.png")
            ).convert_alpha()
        ),
        True,
        False,
    ),
    pygame.transform.flip(
        (pygame.image.load(os.path.join("images", "groundboxedge.png")).convert()),
        True,
        False,
    ),
    pygame.transform.flip(
        (
            pygame.image.load(
                os.path.join("images", "groundboxstraightramptall.png")
            ).convert_alpha()
        ),
        True,
        False,
    ),
]

Lizmelee = [
    pygame.image.load(os.path.join("images", "melee01.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "melee02.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "melee03.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "melee04.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "melee05.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "melee06.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "melee07.png")).convert_alpha(),
]


Lizdeath = [
    pygame.image.load(os.path.join("images", "lizdeath01.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "lizdeath02.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "lizdeath03.png")).convert_alpha(),
]

kamakerbody = pygame.image.load(
    os.path.join("images", "kamakerbody2.png")
).convert_alpha()
kamakerhead = pygame.image.load(
    os.path.join("images", "kamakerhead.png")
).convert_alpha()
kamakerpaw = pygame.image.load(os.path.join("images", "kamakerpaw.png")).convert_alpha()
kamakertail = pygame.image.load(
    os.path.join("images", "kamakertail.png")
).convert_alpha()

rocktile = pygame.image.load(os.path.join("images", "rockblock.png")).convert_alpha()

tracer = [
    pygame.image.load(os.path.join("images", "tracer.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "tracerblue.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "tracerred.png")).convert_alpha(),
]

ammoboxes = [
    pygame.image.load(os.path.join("images", "ammoyellow.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "ammoblue.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "ammored.png")).convert_alpha(),
]

hitpix = [
    pygame.image.load(os.path.join("images", "hit1.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "hit2.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "hit3.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "hit4.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "hit5.png")).convert_alpha(),
]

barrelpix = [
    pygame.image.load(os.path.join("images", "barrels01.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "barrels02.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "barrels03.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "barrels04.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "barrels05.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "barrels06.png")).convert_alpha(),
]

groundtiles = [
    pygame.image.load(os.path.join("images", "groundlefttop.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "groundmidtop.png")).convert(),
    pygame.image.load(os.path.join("images", "groundbotleft.png")).convert(),
    pygame.image.load(os.path.join("images", "groundbotmid.png")).convert(),
    pygame.transform.flip(
        (
            pygame.image.load(
                os.path.join("images", "groundlefttop.png")
            ).convert_alpha()
        ),
        True,
        False,
    ),
    pygame.transform.flip(
        (pygame.image.load(os.path.join("images", "groundbotleft.png")).convert()),
        True,
        False,
    ),
]

Lizlegstill = pygame.image.load(
    os.path.join("images", "walkstilla.png")
).convert_alpha()
Liztorsostill = pygame.image.load(
    os.path.join("images", "torso01a.png")
).convert_alpha()
Lizlegsair = [
    pygame.image.load(os.path.join("images", "jump1.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "jump2.png")).convert_alpha(),
]
Lizlegsaireverse = [
    pygame.transform.flip(
        (pygame.image.load(os.path.join("images", "jump1.png")).convert_alpha()),
        True,
        False,
    ),
    pygame.transform.flip(
        (pygame.image.load(os.path.join("images", "jump2.png")).convert_alpha()),
        True,
        False,
    ),
]
Lizlegsrun = [
    pygame.image.load(os.path.join("images", "walk01a.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "walk02a.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "walk03a.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "walk04a.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "walk05a.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "walk06a.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "walk07a.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "walk08a.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "walk09a.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "walk10a.png")).convert_alpha(),
]
Lizlegsreverse = []
for i in range(len(Lizlegsrun)):
    Lizlegsreverse.append(pygame.transform.flip((Lizlegsrun[i]), True, False))

Liztorsopix = [
    pygame.image.load(os.path.join("images", "torsosmall00.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "torsosmall01.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "torsosmall02.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "torsosmall03.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "torsosmall04.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "torsosmall05.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "torsosmall06.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "torsosmall07.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "torsosmall08.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "torsosmall09.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "torsosmall10.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "torsosmall11.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "torsosmall12.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "torsosmall13.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "torsosmall14.png")).convert_alpha(),
    pygame.image.load(os.path.join("images", "torsosmall15.png")).convert_alpha(),
]
Liztorsoreverse = []
for i in range(len(Liztorsopix)):
    Liztorsoreverse.append(pygame.transform.flip((Liztorsopix[i]), True, False))
