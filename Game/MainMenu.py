import pygame
from SysConst import GAME_STATES, SCALE, SCREEN_WIDTH, SCREEN_HEIGHT


class MainMenu:
    def __init__(self):
        self.button = 0

    def update(self, currentState):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_c or event.key == pygame.K_RETURN):
                    if self.button == 0:
                        return GAME_STATES[2]
                    elif self.button == 1:
                        return GAME_STATES[4]
                    elif self.button == 2:
                        return GAME_STATES[5]

                if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.button < 2:
                    self.button += 1
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and self.button > 0:
                    self.button -= 1
        return currentState

    def draw(self, screen):

        font = pygame.font.Font("Fonts/joystix monospace.otf", 75 * SCALE)
        text = font.render("Космическая баталия", 0, (255, 120, 0))
        textRect = text.get_rect()
        textRect.center = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 5
        screen.blit(text, textRect)

        font = pygame.font.Font("Fonts/joystix monospace.otf", 50 * SCALE)
        rows = ['Играть', 'Рекорды', 'Выйти']
        for i in range(len(rows)):
            if self.button == i:
                color = (250, 250, 0)
            else:
                color = (250, 250, 250)
            text = font.render(rows[i], 0, color)
            textRect = text.get_rect()
            textRect.center = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + (i - 1) * textRect.height * 1.5
            screen.blit(text, textRect)

