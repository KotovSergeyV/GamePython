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



class DeathScreen:
    def __init__(self, score):
        self.score = score
        self.name = '_'
        self.currentRow = 0

    def writeResult(self, sScore, sName):
        incert = False

        with open("res.txt", "r+") as file:
            x = file.readlines()
            for i in range(0, 5):
                try:
                    if not incert:
                        score, name = x[i].split(";")
                        if sScore > score:
                            incert = True
                            file.writelines(sScore + ";" + sName)
                        else:
                            file.writelines(score + ";" + name)
                    else:
                        file.writelines(x[i-1])
                except IndexError:
                    file.writelines(str(sScore) + ";" + str(sName))
                    break
    def update(self, currentState):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if self.currentRow == 1:
                    if (event.key == pygame.K_c or event.key == pygame.K_RETURN):
                        self.writeResult(self.score, self.name)
                        return GAME_STATES[1]
                    elif event.key == pygame.K_UP:
                        self.currentRow = 0
                        self.name += "_"

                else:
                    if event.key == pygame.K_BACKSPACE:
                        if self.name != "_":
                            self.name = self.name[:-2] + "_"
                    elif event.key ==pygame.K_RETURN or event.key == pygame.K_DOWN:
                        self.name = self.name[:-1]
                        self.currentRow = 1
                    else:
                        if (event.key in range(ord("A"), ord("z")+1) or event.key in range(pygame.K_0, pygame.K_9+1))\
                                and len(self.name) < 11:
                            self.name = self.name[:-1] + event.unicode + "_"
        return currentState
    def updateScore(self, score):
        self.score = score
    def drawResults(self, screen):

        font = pygame.font.Font("Fonts/joystix monospace.otf", 70 * SCALE)
        text = font.render("Счёт: " + str(self.score), 0, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - textRect.height*2.3

        screen.blit(text, textRect)

        font = pygame.font.Font("Fonts/joystix monospace.otf", 55 * SCALE)
        if self.currentRow == 0:
            color = (255, 255, 0)
        else:
            color = (255, 255, 255)
        text = font.render("Игрок: " + self.name, 0, color)
        textRect = text.get_rect()
        textRect.center = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - textRect.height

        screen.blit(text, textRect)

        font = pygame.font.Font("Fonts/joystix monospace.otf", 50 * SCALE)
        if self.currentRow == 0:
            color = (255, 255, 255)
        else:
            color = (255, 255, 0)
        text = font.render("Выход", 0, color)
        textRect = text.get_rect()
        textRect.center = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + textRect.height

        screen.blit(text, textRect)

