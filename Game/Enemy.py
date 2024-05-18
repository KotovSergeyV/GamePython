import pygame.sprite
import random
from time import time
from BaseEntity import BaseEntity
from SysConst import SCREEN_WIDTH, SCREEN_HEIGHT
from Bullet import EnemyBullet, Bullet_Sprite_Group
from Map import boxGenerate

Enemy_Sprite_Group = pygame.sprite.Group()


class EnemyController:
    def __init__(self, player):
        self.spawnWidth = SCREEN_WIDTH/20
        self.spawnHeight = -player.rect.height
        self.player = player

        self.enCount = 0
        self.enMaxCount = 3
        self.spawnTimer = 0
        self.spawnTimerDefault = 6

        self.updCountTimer = 0
        self.updCountDefault = 15
        self.killCount = 0
        self.stage = -1
        self.bulletSpeed = 3

        for i in range(3):
            Enemy((random.randint(self.spawnWidth, SCREEN_WIDTH - self.spawnWidth), self.spawnHeight*3), 20,
                  bulletSpeed=self.bulletSpeed, generator=self)

    def resetTime(self):
        self.deltaTime = time()

    def generateEnemy(self):
        # Test
        Enemy((random.randint(self.spawnWidth, SCREEN_WIDTH - self.spawnWidth), self.spawnHeight), 20,
              bulletSpeed=self.bulletSpeed, generator=self)

    def addKill(self):
        self.killCount += 1
        self.player.addKill()

    def update(self):
        self.enCount = len(Enemy_Sprite_Group)

        timeDelta = time() - self.deltaTime
        self.spawnTimer -= timeDelta
        self.updCountTimer += timeDelta

        if (self.spawnTimer <= 0 and self.enCount < self.enMaxCount) or (self.enCount < 3):
            self.spawnTimer = self.spawnTimerDefault
            self.generateEnemy()

        self.deltaTime = time()

        if self.updCountTimer >= self.updCountDefault or self.killCount / 10 > self.updCountDefault:
            self.updCountTimer = 0
            if self.stage < 5:
                if self.stage == -1:
                    self.enMaxCount += 2
                else:
                    self.enMaxCount += 1
                self.spawnTimerDefault -= 1

                self.stage += 1

                self.bulletSpeed -= self.bulletSpeed / 10
                for enemy in Enemy_Sprite_Group:
                    enemy.setSpeedBoost(self.bulletSpeed)


class Enemy(BaseEntity):

    def __init__(self, pos: tuple, speed: int, direction=(-1, 0), hp=3, bulletSpeed=3, generator=None):
        super().__init__(pos, speed, image="Images/Enemy.png", spriteGroup=Enemy_Sprite_Group)

        self.generator = generator

        self.hp = hp

        self.directionX = direction[0]
        self.directionY = direction[1]
        self.latestDirections = [0, 0, direction]

        self.fireTimer = bulletSpeed
        self.fireTimerDefault = bulletSpeed
        self.prevFireTime = time()

        self.borders = pygame.sprite.Group()
        boxGenerate( (SCREEN_WIDTH/30, SCREEN_HEIGHT/30), (SCREEN_WIDTH /30*29, SCREEN_HEIGHT/3), 5, self.borders )

        self.firstApearence = random.randint(self.rect.height, self.rect.height*3)
        self.firstApearenceFlag = True

    def setSpeedBoost(self, bulletSpeed):
        self.fireTimerDefault = bulletSpeed

    def firstMovement(self):
        movement = 0 * self.speedX, 1 * self.speedY
        self.move(movement)

    def movement(self):
        movement = self.directionX * self.speedX, self.directionY * self.speedY

        if movement[1] != 0 and movement[0] != 0:
            movement = movement[0] * 0.75, movement[1] * 0.75

        self.move(movement)
        self.checkCollision()

    def checkCollision(self):
        hits = pygame.sprite.spritecollide(self, self.borders, False)
        for hit in hits:
            self.collided(hit)

    def collided(self, hit):
        while hit.rect.colliderect(self):
            self.move(hit.direction)
            self.changeDir()

    def changeDir(self):
        dir = (random.randint(-1, 1), random.randint(-1, 1))
        while dir in self.latestDirections or dir == (0, 0) or dir == (-self.directionX, -self.directionY):
            dir = (random.randint(-1, 1), random.randint(-1, 1))

        self.directionX, self.directionY = dir
        self.latestDirections[0] = self.latestDirections[1]
        self.latestDirections[1] = self.latestDirections[2]
        self.latestDirections[2] = dir

    def fire(self):
        if self.fireTimer <= 0:
            EnemyBullet(self.rect.center)
            self.fireTimer = self.fireTimerDefault
        else:
            self.fireTimer -= time() - self.prevFireTime

        self.prevFireTime = time()

    def checkHit(self):
        for bullet in Bullet_Sprite_Group:
            if pygame.sprite.collide_mask(self, bullet):
                bullet.kill()
                self.hp -= 1
                if self.hp == 0:
                    self.kill()
                    self.generator.addKill()

    def update(self):
        if self.firstApearenceFlag and self.rect.centery < self.firstApearence:
            self.firstMovement()
            if self.rect.centery >= self.firstApearence:
                self.firstApearenceFlag = False
                self.changeDir()
        else:
            self.movement()
            self.fire()
        self.checkHit()
