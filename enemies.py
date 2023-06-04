from fx import *
from images import *
from initialising import *
from lizzy import liz
from math import atan, atan2, degrees, floor, sin, cos, radians, sqrt
from random import randrange, randint, random


class groundmob(pygame.sprite.Sprite):
    def __init__(self, rectdimensions, startpos, speed, health, attack):
        super().__init__()
        self.surf = pg.surface.Surface(rectdimensions)
        self.surf.fill((255, 0, 0))
        self.surf.set_alpha(0)
        self.rect = self.surf.get_rect()
        self.acc = vec(speed)
        self.vel = vec(0, 0)
        self.pos = vec(startpos)
        self.rect.center = self.pos
        self.grav = vec(0, 0)
        self.fric = vec(0.2, 0)
        self.grounded = False
        self.gothit = False
        self.health = health
        self.attack = attack
        self.reversed = False
        self.obstructed = False
        self.timer = 0
        self.timerreset = False
        self.duration = 1
        self.fatality = False
        self.dying = False
        self.playerSeen = False
        self.stop = False

    def playerdetect(self, range):
        if abs(self.pos.x - liz.pos.x) < range:
            if (not self.reversed and self.pos.x <= liz.pos.x) or (
                    self.reversed and self.pos.x >= liz.pos.x
            ):
                self.playerSeen = True
            else:
                self.playerSeen = False
        else:
            self.playerSeen = False

    def gethit(self, hitcoords, damage, type):
        if not self.dying:
            self.health -= damage
            hitfx = OrganicHit(hitcoords)
            allsprites.add(hitfx)
            if not self.gothit:
                self.gothit = True
                self.timerreset = True

    def move(self):
        self.pos = vec(self.rect.midbottom)
        if self.grounded:
            if not self.gothit and not self.dying and not self.stop:
                self.vel.x += self.acc.x
            self.vel.x -= self.fric.x * self.vel.x
        self.vel.y += self.grav.y

        self.pos += self.vel

        self.rect.midbottom = self.pos

    def groundcheck(self):
        platformhit = pg.sprite.spritecollide(self, platforms, False)
        hardblockhit = pg.sprite.spritecollide(self, hardblocks, False)
        if not platformhit and not hardblockhit:
            self.grounded = False
        if platformhit:
            for i in platformhit:
                i.playercheck()
        if hardblockhit:
            for i in hardblockhit:
                i.playercheck()
        if self.grounded or self.vel.y > 45:
            self.grav.y = 0
        else:
            self.grav.y = 2
        self.rect.midbottom = self.pos

    def wallcheck(self):
        oldpos = self.rect.midbottom
        if not self.reversed:
            self.rect.x += 50

        elif self.reversed:
            self.rect.x -= 50

        blockcheck = pg.sprite.spritecollide(self, hardblocks, False)
        if blockcheck:
            for i in blockcheck:
                i.playercheck()
        self.rect.midbottom = oldpos

    def gapcheck(self):
        if not self.reversed:
            self.rect.x += 100
            self.rect.y += 200
        elif self.reversed:
            self.rect.x -= 100
            self.rect.y += 200
        blockcheck = pg.sprite.spritecollide(self, hardblocks, False)
        platformcheck = pg.sprite.spritecollide(self, platforms, False)
        if not blockcheck and not platformcheck:
            self.obstructed = True

        else:
            self.obstructed = False
        self.rect.midbottom = self.pos


class flamecroc(groundmob):
    def __init__(self, startpos):
        super().__init__((100, 180), startpos, (2, 0), 50, 20)
        self.imageset = crocwalk
        self.image = self.imageset[0]
        self.imageframe = self.image.get_rect()
        self.sheet = pg.surface.Surface((279, 200))
        self.sheet.set_alpha(255)
        self.sheet.fill((0, 0, 0))
        self.sheetrect = self.sheet.get_rect()
        self.sheet.set_colorkey((0, 0, 0))
        self.state = "walking"
        self.aggro = False
        self.aggroTimer = 0
        self.power = 40
        self.timer2 = 0

    def utilityTimer(self):
        self.timer2 += 1
        if self.timer2 > 100:
            self.timer2 = 0

    def firingAngle(self, speed, gravity, x, y):
        flip = x
        x = abs(x)
        gravity *= -1
        y *= -1
        if x == 0:
            x = 0.01
        quadratic = speed ** 4 - gravity * (gravity * x ** 2 + 2 * speed ** 2 * y)
        if quadratic < 0:
            quadratic = 0
        divider = gravity * x
        tangent = (speed ** 2 - sqrt(quadratic)) / divider
        angle = atan(tangent)

        if flip < 0:
            angle = pi - angle

        return angle

    def watchAngle(self, x, y):
        angle = degrees(atan2(x, y))
        angle += 270
        if angle > 360:
            angle -= 360
        return angle

    def fire(self):
        self.sheet.fill((0, 0, 0))

        if self.state == "firing" and not self.stop:
            self.stop = True
        x = liz.rect.centerx - self.rect.centerx
        y = self.rect.centery - liz.rect.centery
        absx = abs(x)
        watchangle = self.watchAngle(absx, y)
        fireangle = self.firingAngle(self.power, 2, x, y)
        firerotate = degrees(self.firingAngle(self.power, 2, absx, y))
        crochead = pg.transform.rotate(crocextra[1], watchangle)
        crocrect = crochead.get_rect()
        crocrect.center = (110, 55)
        crocgun = pg.transform.rotate(crocextra[0], firerotate)
        gunrect = crocgun.get_rect()
        gunrect.center = (130, 100)
        self.sheet.blit(crocextra[2], (50, 70))
        self.sheet.blit(crocextra[3], self.sheetrect)
        self.sheet.blit(crochead, crocrect)
        self.sheet.blit(crocgun, gunrect)
        self.image = self.sheet

        if self.timer2 < 20 or self.timer2 > 70:
            self.state = "walking"
            self.stop = False
        if self.timer2 > 25:
            blob = fireBlob(self.power, fireangle, self.rect.center)
            allsprites.add(blob)
            hazards.add(blob)

    def doAggro(self):
        if not self.aggro:
            self.aggro = True
        self.aggroTimer += 1
        if self.aggroTimer >= 30:
            self.aggro = False

    def update(self):
        self.utilityTimer()
        self.move()
        if self.state == "walking" and self.grounded:
            self.gapcheck()
            self.wallcheck()
        self.playerdetect(800)
        self.groundcheck()

        self.control()
        if self.state != "firing":
            self.animate()

        self.render()

    def control(self):

        if self.obstructed and self.state == "walking":
            self.timer = 0
            self.state = "turning"
        if self.state == "walking" and self.playerSeen and 20 < self.timer2 < 70 and not self.dying:
            self.state = "firing"
        if self.playerSeen or self.gothit:
            self.aggroTimer = 0
            self.doAggro()
        elif self.aggro:
            self.doAggro()
        if self.aggro:
            if (not self.reversed and self.pos.x >= liz.pos.x) or (
                    self.reversed and self.pos.x <= liz.pos.x
            ):
                if self.state == "walking" and not self.gothit:
                    self.timer = 0
                    self.state = "turning"
        if self.state == "turning":
            self.turn()
        if self.state == "firing":
            self.fire()
        if self.gothit:
            self.hitanim()
        self.deathcheck()

    def animate(self):
        if self.dying:
            self.imageset = crocdeath
        cutoff = 3 * len(self.imageset)
        self.image = self.imageset[(self.timer // 3)]
        self.timer += 1
        if self.timer == cutoff:
            if not self.dying:
                self.timer = 0
            else:
                self.timer -= 1

    def turn(self):
        self.obstructed = False
        if self.timer == 0:
            self.imageset = crocrotate
            self.acc.x *= -1
        if self.timer == 21:
            self.imageset = crocwalk
            self.state = "walking"
            if self.reversed:
                self.reversed = False
            elif not self.reversed:
                self.reversed = True

    def deathcheck(self):
        if self.health <= 0 and not self.dying:
            self.fatality = True
            self.die(0)
        if self.pos.y > 3000:
            self.die(1)

    def hitanim(self):
        if self.timerreset:
            self.timer = 0
            self.timerreset = False
            self.imageset = crocdeath
            self.duration = randint(1, 9)
        if self.timer == self.duration:
            self.gothit = False
            self.timer = 0
            self.imageset = crocwalk

    def die(self, type):
        if type == 1:
            self.kill()
        if type == 0:
            if self.fatality:
                enemies.remove(self)
                self.timer = 0
                self.fatality = False
                self.dying = True
            self.imageset = crocdeath

    def render(self):
        self.imageframe.center = self.rect.center
        # screen.blit(self.surf, self.rect)
        if not self.reversed:
            reverseimg = pg.transform.flip(self.image, True, False)
            screen.blit(reverseimg, self.imageframe)
        else:
            screen.blit(self.image, self.imageframe)


class fireBlob(pygame.sprite.Sprite):
    def __init__(self, power, angle, coords):
        super().__init__()
        self.surf = pygame.Surface((6, 6))
        self.rect = self.surf.get_rect()
        self.surf.fill((0, 0, 0))
        self.surf.set_colorkey((0, 0, 0))
        pg.draw.circle(self.surf, ((255, 255, 50)), (3, 3), 3)
        self.glow = pygame.Surface((20, 20))
        self.glowrect = self.glow.get_rect()

        self.glow.fill((0, 0, 0))
        self.glow.set_colorkey((0, 0, 0))
        self.glow.set_alpha(70)
        pg.draw.circle(self.glow, ((180, 40, 0)), (10, 10), 10)
        self.pos = vec(coords)
        self.rect.center = self.pos
        self.glowrect.center = self.pos
        self.gravity = 2
        err = random() - 0.5

        self.speed = power + err
        self.angle = angle + err / 10
        self.vel = vec((cos(self.angle) * self.speed), (sin(self.angle) * self.speed))
        self.grounded = False
        self.obstructed = False
        self.timer = 0

    def update(self):
        if not self.grounded:
            self.gravity = 2
        self.move()
        if self.timer > 3:
            mobs.add(self)

            self.groundcheck()
        if self.timer > 3:
            self.render()
        self.timer += 1
        if self.timer > 40:
            self.kill()

    def move(self):
        self.pos = vec(self.rect.center)
        self.vel.y += self.gravity
        if self.grounded:
            self.vel.y = 0
            self.vel.x *= 0.9
        if self.obstructed:
            self.vel.x *= -0.1
        self.pos += self.vel
        self.rect.center = self.pos
        self.glowrect.center = self.pos

    def groundcheck(self):
        platformhit = pg.sprite.spritecollide(self, platforms, False)
        hardblockhit = pg.sprite.spritecollide(self, hardblocks, False)
        if not platformhit and not hardblockhit:
            self.grounded = False
        if platformhit:
            for i in platformhit:
                i.playercheck()
        if hardblockhit:
            for i in hardblockhit:
                i.playercheck()

    def render(self):

        screen.blit(self.surf, self.rect)
        screen.blit(self.glow, self.glowrect, special_flags=BLEND_RGB_ADD)


class kamaker(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__()
        self.surf = pygame.Surface((200, 100))
        self.killed = False
        self.surf.fill((0, 0, 0))
        self.surf.set_alpha(255)
        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.hardblocked = False
        self.gothit = False
        self.pos = vec(coords)
        self.rect.midbottom = self.pos
        self.speed = -5
        self.fallspeed = 0
        self.health = 25
        self.grounded = False
        self.gravity = 2
        self.reversed = False
        self.timer = 0
        self.deathtimer = 0
        self.oldpos = self.pos
        self.xpos1 = 40
        self.xpos2 = 85
        self.xpos3 = 100
        self.xpos4 = 145
        self.ypos1 = 70
        self.ypos2 = 70
        self.ypos3 = 70
        self.ypos4 = 70
        self.partlist1 = []
        self.partlist2 = []
        self.attack = 20

    def gethit(self, hitcoords, damage, type):
        self.gothit = True
        self.health -= damage
        chance = randint(0, 2)
        if type == "bullet" or type == "melee":
            if chance == 0:
                hitfx = OrganicHit(hitcoords)
                allsprites.add(hitfx)
        elif type == "explosive":
            blast = explosive(hitcoords)
            allsprites.add(blast)
        copysurf = self.surf
        if not self.killed:
            self.surf.blit(copysurf, (100, 50), special_flags=BLEND_RGB_ADD)
        if type != "explosive":
            if hitcoords[0] < self.rect.centerx:
                if not self.hardblocked:
                    self.rect.centerx += 10
                else:
                    self.rect.centerx -= 10
            if hitcoords[0] > self.rect.centerx:
                if not self.hardblocked:
                    self.rect.centerx -= 10
                else:
                    self.rect.centerx += 5

        if self.health <= 0:
            self.killed = True

    def move(self):
        self.oldpos = self.pos
        self.pos = vec(self.rect.midbottom)
        if not self.grounded:
            self.fallspeed += self.gravity
            if self.fallspeed > 20:
                self.fallspeed = 20
            self.pos.y += self.fallspeed

        if self.grounded and not self.reversed:
            self.pos.x += self.speed
        elif self.grounded and self.reversed:
            self.pos.x -= self.speed
        self.rect.midbottom = self.pos

    def edgedetect(self):
        if self.grounded:
            if not self.reversed:
                self.rect.centerx -= 150
            elif self.reversed:
                self.rect.centerx += 150
            hits = pygame.sprite.spritecollide(self, platforms, False)
            if not self.reversed:
                self.rect.centerx += 150
            elif self.reversed:
                self.rect.centerx -= 150
            if not hits:
                if self.reversed:
                    self.reversed = False
                    self.pos.x -= self.speed
                elif not self.reversed:
                    self.reversed = True
                    self.pos.x += self.speed

            # self.rect.midbottom = self.pos

    def platformcheck(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            for i in hits:
                if self.pos.y < i.rect.centery:
                    self.grounded = True
                    self.pos.y = i.rect.top + 1
                    self.rect.bottom = i.rect.top + 1
                else:
                    self.grounded = False
        else:
            self.grounded = False

    def hardblockscheck(self):
        hits = pygame.sprite.spritecollide(self, hardblocks, False)
        if hits:
            self.pos = self.oldpos
            if not self.reversed:
                self.reversed = True
            elif self.reversed:
                self.reversed = False
            self.hardblocked = True
        else:
            self.hardblocked = False

    def render(self):
        if not self.reversed:
            screen.blit(self.surf, self.rect)
            if self.gothit:
                screen.blit(self.surf, self.rect, special_flags=BLEND_RGB_ADD)
        else:
            flipped = pygame.transform.flip(self.surf, True, False)
            screen.blit(flipped, self.rect)
            if self.gothit:
                screen.blit(flipped, self.rect, special_flags=BLEND_RGB_ADD)

        if self.health < 25:
            healthrect = pygame.Rect(
                self.rect.left, self.rect.bottom, self.health * 5, 5
            )
            pygame.draw.rect(screen, ("red"), healthrect)
        self.surf.fill((0, 0, 0))

    def update(self):
        if self.timer > 19:
            self.timer = 0
        self.edgedetect()
        if not self.killed:
            self.move()
        self.platformcheck()
        self.hardblockscheck()

        if self.deathtimer < 5:
            self.animate()
            self.render()
        if self.killed:
            self.deathani()
        self.timer += 1
        self.gothit = False

    def deathani(self):
        if self.deathtimer == 0:
            for i in range(30):
                x = self.rect.centerx + (randint(-30, 30))
                y = self.rect.centery + (randint(-10, 10))
                randomcol = randint(170, 230)
                part1 = particle(
                    x, y, 0, 0, 0, 0, 1, 4, (50, randomcol, 20), screen, (0, 0, 0), True
                )
                self.partlist1.append(part1)
        if self.deathtimer < 8:
            for i in self.partlist1:
                i.draw()

        if self.deathtimer == 6:
            for i in range(50):
                x = self.rect.centerx + (randint(-40, 40))
                y = self.rect.centery + (randint(-20, 20))
                randomcol2 = randint(170, 230)
                part2 = particle(
                    x,
                    y,
                    randint(-15, 15),
                    randint(-30, 0),
                    0,
                    1,
                    8,
                    -0.4,
                    (50, randomcol2, 20),
                    screen,
                    (0, 0, 0),
                    True,
                )
                self.partlist2.append(part2)
        if 6 < self.deathtimer < 20:
            for i in self.partlist2:
                i.draw()

        if self.deathtimer > 30:
            self.kill()
        self.deathtimer += 1

    def animate(self):
        self.frontpawfront()
        self.frontpawback()
        self.backpawfront()
        self.backpawback()
        self.surf.blit(kamakerpaw, (self.xpos1, self.ypos1))
        self.surf.blit(kamakerpaw, (self.xpos3, self.ypos3))
        self.surf.blit(kamakerbody, (50, 15))
        self.surf.blit(kamakertail, (160, 50))
        self.surf.blit(kamakerpaw, (self.xpos2, self.ypos2))
        self.surf.blit(kamakerpaw, (self.xpos4, self.ypos4))
        self.surf.blit(kamakerhead, (0, 0))

    def frontpawfront(self):
        if self.timer < 10:
            self.xpos1 += 5
        elif 10 <= self.timer < 15:
            self.xpos1 -= 5
            self.ypos1 -= 5
        elif self.timer >= 15:
            self.xpos1 -= 5
            self.ypos1 += 5

    def frontpawback(self):
        if self.timer < 5:
            self.xpos2 -= 5
            self.ypos2 -= 5
        elif 5 <= self.timer < 10:
            self.xpos2 -= 5
            self.ypos2 += 5
        elif self.timer >= 10:
            self.xpos2 += 5

    def backpawfront(self):
        if self.timer < 10:
            self.xpos3 += 5
        elif 10 <= self.timer < 15:
            self.xpos3 -= 5
            self.ypos3 -= 5
        elif self.timer >= 15:
            self.xpos3 -= 5
            self.ypos3 += 5

    def backpawback(self):
        if self.timer < 5:
            self.xpos4 -= 5
            self.ypos4 -= 5
        elif 5 <= self.timer < 10:
            self.xpos4 -= 5
            self.ypos4 += 5
        elif self.timer >= 10:
            self.xpos4 += 5
