import pygame

rocktile = pygame.image.load("rockblock.png").convert_alpha()

hitpix = [
    pygame.image.load("hit1.png").convert_alpha(),
    pygame.image.load("hit2.png").convert_alpha(),
    pygame.image.load("hit3.png").convert_alpha(),
    pygame.image.load("hit4.png").convert_alpha(),
    pygame.image.load("hit5.png").convert_alpha()

]

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
