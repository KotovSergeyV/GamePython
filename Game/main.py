import pygame.mixer_music

from Player import Player, BlowAnimGroup
from Enemy import EnemyController, Enemy_Sprite_Group
from Bullet import Bullet_Sprite_Group, EnemyBullet_Sprite_Group
from SysConst import SCREEN
from StarsBG import drawStars, Star_groups
from MainMenu import *
from BaseEntity import BaseSpriteGroup


def drawStarsInGame():
    for i in range(3):
        drawStars(Star_groups[i], i+1, 3-i, screen, i)

def drawInstruction():
    font = pygame.font.Font("Fonts/joystix monospace.otf", 75 * SCALE)
    text = font.render("Инструкция", 0, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = SCREEN_WIDTH/2, SCREEN_HEIGHT/5
    screen.blit(text, textRect)

    font = pygame.font.Font("Fonts/joystix monospace.otf", 50 * SCALE)
    rows = ['WASD / ←↑→↓ - передвижение', 'Пробел - стрелять', 'С / Enter - подтвердить, Esc - пауза']
    for i in range(len(rows)):
        text = font.render(rows[i], 0, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = SCREEN_WIDTH/2, SCREEN_HEIGHT / 2 + (i-1) * textRect.height*1.5
        screen.blit(text, textRect)

def updateMenu(mainMenu, currentState):
    return mainMenu.update(currentState=currentState)

def drawMenu(mainMenu):
    drawStarsInGame()
    mainMenu.draw(screen)

def updateGame(currentState, mainElements):

    Bullet_Sprite_Group.update()
    EnemyBullet_Sprite_Group.update()

    Enemy_Sprite_Group.update()
    if len(BlowAnimGroup) > 0:
        currentState = BlowAnimGroup.sprites()[0].update(current_state=currentState)
    mainElements.playerGroup.update()

    mainElements.enGenerator.update()
    if mainElements.player.pause:
        return GAME_STATES[6]
    return currentState


def drawGame(mainElements):
    drawStarsInGame()

    Bullet_Sprite_Group.draw(screen)
    EnemyBullet_Sprite_Group.draw(screen)

    Enemy_Sprite_Group.draw(screen)
    draw_hurts(mainElements)
    writeScoreInGame(mainElements)
    mainElements.playerGroup.draw(screen)
    BlowAnimGroup.draw(screen)


def draw_hurts(mainElements):
    for hp in range(mainElements.player.hp):
        screen.blit(mainElements.player.hpImage, (SCREEN_WIDTH/100, SCREEN_HEIGHT/5*4.5 -
                                                  hp*mainElements.player.image.get_height()/1.5))


def writeScoreInGame(mainElements):

    font = pygame.font.Font("Fonts/joystix monospace.otf", 30 * SCALE)
    text = font.render("Счёт: " + str(mainElements.player.score), 0, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 30

    screen.blit(text, (SCREEN_WIDTH-textRect.width, SCREEN_HEIGHT - textRect.height))

def updateDeath(deathScreen, currentState):
    return deathScreen.update(currentState)

def drawDeath(deathScreen):
    deathScreen.drawResults(screen)

def updateResults(resScreen, currentState):
    return resScreen.update(currentState)
def drawResults(resScreen):
    resScreen.drawResults(screen)

def updatePause(pauseScreen, currentState):
    return pauseScreen.update(currentState)
def drawPause(pauseScreen):
    pauseScreen.draw(screen)

def playGameMusic(sound):
    pygame.mixer_music.stop()
    pygame.mixer_music.load(sound)
    pygame.mixer_music.play(loops=-1)
    pygame.mixer_music.set_volume(0.1)

def main(currentState):
    mainElements = MainElements()

    mainMenu = MainMenu()
    deathScreen = DeathScreen(mainElements.player.score)
    resultScreen = ResultScreen()
    pauseScreen = Pause()

    running = True
    while running:

        screen.fill('black')
        if currentState == "Close":
            running = False
        if currentState == "MainMenu":
            currentState = updateMenu(mainMenu, currentState)
            if currentState == "Game":
                # enGenerator.resetTime()
                playGameMusic("Sounds/09 Uppdercut.wav")
                for el in BaseSpriteGroup:
                    el.kill()

                mainElements = MainElements()
                mainElements.enGenerator.resetTime()
            if currentState == "Results":
                resultScreen = ResultScreen()
            drawMenu(mainMenu)

        elif currentState == "Instruction":
            drawInstruction()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_c or event.key == pygame.K_RETURN):
                    currentState = GAME_STATES[1]
                    playGameMusic("Sounds/10 Player 1.wav")
                    pygame.event.clear()

        elif currentState == "InGamePause":
            drawGame(mainElements)
            currentState = updatePause(pauseScreen, currentState)
            if currentState == "Game":
                mainElements.player.pause = False
            elif currentState == "DeathScreen":
                deathScreen = DeathScreen(mainElements.player.score)
                playGameMusic("Sounds/10 Player 1.wav")
            drawPause(pauseScreen)

        elif currentState == "Game":
            deathScreen.updateScore(mainElements.player.score)
            currentState = updateGame(currentState, mainElements)
            if currentState == "DeathScreen":
                deathScreen = DeathScreen(mainElements.player.score)
                playGameMusic("Sounds/10 Player 1.wav")
            drawGame(mainElements)

        elif currentState == "DeathScreen":
            currentState = updateDeath(deathScreen, currentState)
            drawDeath(deathScreen)

        elif currentState == "Results":
            currentState = updateResults(resultScreen, currentState)
            drawResults(resultScreen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                running = False
                break

        if currentState == "Game":
            pygame.display.flip()
            clock.tick(120)
        else:
            pygame.display.flip()
            clock.tick(20)

    pygame.quit()


class MainElements:
    def __init__(self):
        self.player = Player((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3 * 2), 50)
        self.playerGroup = pygame.sprite.GroupSingle()
        self.playerGroup.sprite = self.player

        self.enGenerator = EnemyController(self.player)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    pygame.init()
    pygame.display.set_caption("Game")

    screen = pygame.display.set_mode(SCREEN, flags=pygame.FULLSCREEN) #, flags=pygame.NOFRAME)

    clock = pygame.time.Clock()

    currentState = "Instruction"

    main(currentState)
