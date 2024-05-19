import pygame, os
from SysConst import GAME_STATES, SCALE, SCREEN_WIDTH, SCREEN_HEIGHT


class MainMenu:
    def __init__(self):
        self.button = 0
        self.select = pygame.mixer.Sound("Sounds/Select.mp3")

    def update(self, currentState):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.select.play()
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

        font = pygame.font.Font("Fonts/joystix monospace.otf", int(75 * SCALE))
        text = font.render("Космическая баталия", 0, (255, 120, 0))
        textRect = text.get_rect()
        textRect.center = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 5
        screen.blit(text, textRect)

        font = pygame.font.Font("Fonts/joystix monospace.otf", int(50 * SCALE))
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
        self.select = pygame.mixer.Sound("Sounds/Select.mp3")
        self.currentRow = 0

    def writeResult(self, sScore, sName):

        incert = False
        x = []
        if os.path.exists('res.txt'):
            with open("res.txt", "r+") as file:
                x = file.readlines()

        with open("res.txt", "w") as file:
            for i in range(0, 5):
                try:
                    if not incert:
                        score, name = x[i].split(";")
                        if sScore > int(score):
                            incert = True
                            file.write(str(sScore) + ";" + str(sName) + "\n")
                        else:
                            file.write(score + ";" + name)
                    else:
                        file.write(x[i - 1])
                except IndexError:
                    file.write(str(sScore) + ";" + str(sName) + "\n")
                    break

    def update(self, currentState):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if self.currentRow == 1:
                    if (event.key == pygame.K_c or event.key == pygame.K_RETURN):

                        self.select.play()
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

        font = pygame.font.Font("Fonts/joystix monospace.otf", int(70 * SCALE))
        text = font.render("Счёт: " + str(self.score), 0, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - textRect.height*2.3

        screen.blit(text, textRect)

        font = pygame.font.Font("Fonts/joystix monospace.otf", int(55 * SCALE))
        if self.currentRow == 0:
            color = (255, 255, 0)
        else:
            color = (255, 255, 255)
        text = font.render("Игрок: " + self.name, 0, color)
        textRect = text.get_rect()
        textRect.center = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - textRect.height

        screen.blit(text, textRect)

        font = pygame.font.Font("Fonts/joystix monospace.otf", int(50 * SCALE))
        if self.currentRow == 0:
            color = (255, 255, 255)
        else:
            color = (255, 255, 0)
        text = font.render("Выход", 0, color)
        textRect = text.get_rect()
        textRect.center = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + textRect.height

        screen.blit(text, textRect)





class ResultScreen:
    def __init__(self):
        self.results = self.readResults()
        self.select = pygame.mixer.Sound("Sounds/Select.mp3")
    def readResults(self):
        x = []
        if os.path.exists('res.txt'):
            with open("res.txt", "r") as file:
                x = file.readlines()
        return x

    def update(self, result):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_c or event.key == pygame.K_RETURN):
                    self.select.play()
                    return GAME_STATES[1]
        return result
    def drawResults(self, screen):

        font = pygame.font.Font("Fonts/joystix monospace.otf", int(70 * SCALE))
        text = font.render("Результат", 0, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 5

        screen.blit(text, textRect)

        for i in range(len(self.results)):
            res, name = self.results[i].strip('\n').split(';')

            font = pygame.font.Font("Fonts/joystix monospace.otf", int(45 * SCALE))
            text = font.render(name + " " + res, 0, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 5*1.5 + textRect.height * i*1.5

            screen.blit(text, textRect)

        font = pygame.font.Font("Fonts/joystix monospace.otf", int(50 * SCALE))

        text = font.render("Выход", 0, (255, 255, 0))
        textRect = text.get_rect()
        textRect.center = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 5*4

        screen.blit(text, textRect)





class Pause:
    def __init__(self):
        self.row = 0
        self.select = pygame.mixer.Sound("Sounds/Select.mp3")
    def update(self, currentState):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.select.play()
                if (event.key == pygame.K_c or event.key == pygame.K_RETURN):
                    if self.row == 0:
                        return GAME_STATES[2]
                    elif self.row == 1:
                        return GAME_STATES[3]
                if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.row == 0:
                    self.row = 1
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and self.row == 1:
                    self.row = 0
        return currentState
    def writeOnScreen(self, screen, text, color, plus):
        font = pygame.font.Font("Fonts/joystix monospace.otf", int(60 * SCALE))
        text = font.render(text, 0, color)
        textRect = text.get_rect()
        textRect.center = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + plus*textRect.height
        screen.blit(text, textRect)
    def draw(self, screen):

        if self.row == 0:
            c1 = (255, 255, 0)
            c2 = (255, 255, 255)
        else:
            c1 = (255, 255, 255)
            c2 = (255, 255, 0)

        sc = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        sc.fill(pygame.color.Color(0, 0, 0))
        sc.set_alpha(128)
        screen.blit(sc, sc.get_rect())

        self.writeOnScreen(screen, "Продолжить", c1, -1)
        self.writeOnScreen(screen, "Выйти", c2, 1)
