import pygame
from SysConst import TIME_TICK, SCALE_X, SCALE_Y

BaseSpriteGroup = pygame.sprite.Group()

class BaseEntity(pygame.sprite.Sprite):

    def __init__(self, pos: tuple, speed: float, image="Images/Enemy.png", xScaleMultiplier=70, yScaleMultiplier=80, spriteGroup=None):
        if spriteGroup is not None:
            super().__init__(spriteGroup, BaseSpriteGroup)
        else:
            super().__init__()
        tt = TIME_TICK / 10
        self.posX = pos[0]
        self.posY = pos[1]
        self.speedX = speed / tt * SCALE_X
        self.speedY = speed / tt * SCALE_Y

        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (xScaleMultiplier*SCALE_X,  yScaleMultiplier*SCALE_Y))

        self.rect = self.image.get_rect()
        self.rect.center = self.posX, self.posY
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, movement):
        self.posX += movement[0]
        self.posY += movement[1]
        self.rect.center = self.posX, self.posY
