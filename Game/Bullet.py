import pygame.sprite
from BaseEntity import BaseEntity
from SysConst import SCREEN_WIDTH, SCREEN_HEIGHT

Bullet_Sprite_Group = pygame.sprite.Group()
EnemyBullet_Sprite_Group = pygame.sprite.Group()


class Bullet(BaseEntity):

    def __init__(self, pos: tuple, speed=90, direction=(0, -1), image="Images/Bullet.png",
                 spriteGroup=Bullet_Sprite_Group):
        super().__init__(pos, speed, image, spriteGroup=spriteGroup, xScaleMultiplier=16, yScaleMultiplier=30)

        self.direction = direction

    def movement(self):
        movement = self.direction[0] * self.speedX, self.direction[1] * self.speedY
        self.move(movement)

    def update(self):
        self.movement()
        self.outOfBoundsCheck()

    def outOfBoundsCheck(self):
        if (self.rect.centerx < -self.rect.width / 2) \
                or (self.rect.centerx > SCREEN_WIDTH+self.rect.width / 2) \
                or (self.rect.centery < -self.rect.height / 2)\
                or (self.rect.centery > SCREEN_HEIGHT + self.rect.height / 2):

            self.kill()


class EnemyBullet(Bullet):

    def __init__(self, pos: tuple, speed=80, direction=(0, 1)):
        super(EnemyBullet, self).__init__(pos, speed, direction, image="Images/EnemyBulletBase.png",
                                          spriteGroup=EnemyBullet_Sprite_Group)
