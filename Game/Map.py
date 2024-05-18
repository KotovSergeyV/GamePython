import pygame


class Border(pygame.sprite.Sprite):

    def __init__(self, width, height, center, direction, spriteGroup):

        super().__init__(spriteGroup)
        self.image = pygame.surface.Surface((width, height))
        self.image.fill("red")
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = center
        self.direction = direction


def boxGenerate(upperLeft, lowerRight, size, spriteGroup):
    x1, y1, x2, y2 = upperLeft[0], upperLeft[1], lowerRight[0], lowerRight[1]

    width = x2 - x1
    height = y2 - y1

    spriteGroup.add(Border(width, size, (x1+width/2, y1-size/2), (0, 1), spriteGroup))
    spriteGroup.add(Border(width, size, (x1+width/2, y2+size/2), (0, -1), spriteGroup))
    spriteGroup.add(Border(size, height, (x1-size/2, y1+height/2), (1, 0), spriteGroup))
    spriteGroup.add(Border(size, height, (x2+size/2, y1+height/2), (-1, 0), spriteGroup))
