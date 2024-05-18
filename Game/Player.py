import time
import pygame

from Bullet import Bullet, EnemyBullet_Sprite_Group
from SysConst import SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_Y, SCALE_X, GAME_STATES, SCALE
from BaseEntity import BaseEntity
from Map import boxGenerate


class Player(BaseEntity):

    def __init__(self, pos: tuple, speed: float):
        super().__init__(pos, speed, "Images/Flyer.png")

        xScaleMultiplier = 35
        yScaleMultiplier = 35

        self.defaultImage = self.image.copy()

        self.damagedImage = pygame.image.load("Images/FlyerDamaged.png")
        self.damagedImage = pygame.transform.scale(self.damagedImage, self.image.get_size())
        self.invicibilityTimer = 0
        self.invicibilityTimerDefault = 2
        self.invInd = 0
        self.defaultImageDamaged = self.damagedImage.copy()

        self.superiorShipImage = pygame.image.load("Images/FlyerMaxed.png")
        self.superiorShipImage = pygame.transform.scale(self.superiorShipImage, self.image.get_size())

        self.hpImage = pygame.image.load("Images/Hp.png")
        self.hpImage = pygame.transform.scale(self.hpImage, (xScaleMultiplier * SCALE_X, yScaleMultiplier * SCALE_Y))

        self.keys = []

        self.defaultFireTimer = 0.4
        self.speedFeature = 0.075
        self.fireTimer = 0
        self.prevFireTime = 0

        self.borders = pygame.sprite.Group()
        boxGenerate((SCREEN_WIDTH / 30, SCREEN_HEIGHT / 3), (SCREEN_WIDTH / 30 * 29, SCREEN_HEIGHT / 30 * 29),
                    5, self.borders)

        self.stage = 1
        self.hp = 3
        self.killCount = 0
        self.killed = False

        self.score = 0

    def upgrade(self):
        if self.stage < 5:
            self.stage += 1
            self.defaultFireTimer -= self.speedFeature
            if self.stage == 5:
                self.image = self.superiorShipImage.copy()

    def addKill(self, stage):
        self.killCount += 1
        self.score += (stage+2)
        if self.killCount % 5 == 0:
            self.upgrade()


    def getDamage(self):
        if self.invicibilityTimer <= 0 and not self.killed:
            self.killCount = 0
            if self.stage > 1:
                self.stage -= 1
                self.defaultFireTimer += self.speedFeature
            self.hp -= 1
            if self.hp == 0:
                BlowAnimation(self.rect.center, self)
                self.killed = True

            self.invicibilityTimer = self.invicibilityTimerDefault
            self.imageChangeOnDamage(0)

    def imageChangeOnDamage(self, deltaTime):
        self.invicibilityTimer -= deltaTime
        if self.invicibilityTimer <= 0:
            self.image = self.defaultImage.copy()
            self.damagedImage = self.defaultImageDamaged.copy()
            self.invInd = 0
        x = [i for i in range(20, -1, -2)]
        if round(self.invicibilityTimer, 2) == x[self.invInd] / 10:
            self.image, self.damagedImage = self.damagedImage, self.image
            self.invInd += 1

    def checkHit(self):
        for bullet in EnemyBullet_Sprite_Group:
            if pygame.sprite.collide_mask(self, bullet):
                bullet.kill()
                self.getDamage()

    def movement(self):

        directionX = 0
        directionY = 0

        if self.keys[pygame.K_a]:
            directionX -= 1
        if self.keys[pygame.K_d]:
            directionX += 1
        if self.keys[pygame.K_s]:
            directionY += 1
        if self.keys[pygame.K_w]:
            directionY -= 1

        if (directionY != 0 and directionX != 0):
            directionX *= 0.75
            directionY *= 0.75

        movement = directionX * self.speedX, directionY * self.speedY
        self.move(movement)
        self.checkCollision()

    def checkCollision(self):
        hits = pygame.sprite.spritecollide(self, self.borders, False)
        for hit in hits:
            while hit.rect.colliderect(self):
                self.move(hit.direction)

    def fire(self, deltaTime):

        if self.keys[pygame.K_SPACE] and self.fireTimer <= 0:
            Bullet(self.rect.center)
            self.fireTimer = self.defaultFireTimer
        else:
            self.fireTimer -= deltaTime

    def updateKeys(self):
        self.keys = pygame.key.get_pressed()

    def update(self):
        if not self.killed:
            deltaTime = time.time() - self.prevFireTime

            self.updateKeys()

            self.movement()
            self.fire(deltaTime)

            self.checkHit()

            if self.invicibilityTimer > 0:
                self.imageChangeOnDamage(deltaTime)
            self.prevFireTime = time.time()


BlowAnimGroup = pygame.sprite.Group()


class BlowAnimation(pygame.sprite.Sprite):
    def __init__(self, pos, player):
        super().__init__(BlowAnimGroup)
        ScaleMultiplier = 30
        self.blowSheet = pygame.image.load("Images/BlowSpSheet.png").convert_alpha()

        self.width, self.height = ScaleMultiplier * SCALE_X, ScaleMultiplier * SCALE_Y
        self.image = pygame.Surface((self.width, self.height)).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.center = pos

        self.timer = 0
        self.frameIndex = 0
        self.prevFireTime = time.time()
        self.animate()
        self.player = player

    def animate(self):
        self.image = pygame.Surface((self.width, self.height)).convert_alpha()
        self.image.blit(self.blowSheet, (0, 0), (self.width * self.frameIndex, 0, self.width, self.height))
        self.image = pygame.transform.scale(self.image, (
        self.width * (1 + self.frameIndex / 2), self.height * (1 + self.frameIndex / 2)))
        self.image.set_colorkey((0, 0, 0))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.center

        if self.frameIndex == 5:
            self.player.kill()

    def update(self, current_state):

        self.timer += time.time() - self.prevFireTime

        for i in [i / 10 for i in range(0, 41, 2)]:
            if round(self.timer, 2) == i:
                self.frameIndex += 1
                self.animate()
                if round(self.timer, 2) >= 4:
                    return GAME_STATES[3]
        self.prevFireTime = time.time()

        return current_state
