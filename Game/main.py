import pygame
from Player import Player, BlowAnimGroup
from Enemy import EnemyController, Enemy_Sprite_Group
from Bullet import Bullet_Sprite_Group, EnemyBullet_Sprite_Group
from SysConst import SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT, TIME_TICK, GAME_STATES, SCALE
from StarsBG import drawStars, Star_groups
from MainMenu import MainMenu


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
    rows = ['WASD / ←↑→↓ - передвижение', 'Пробел - стрелять', 'С / Enter - подтвердить']
    for i in range(len(rows)):
        text = font.render(rows[i], 0, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = SCREEN_WIDTH/2, SCREEN_HEIGHT / 2 + (i-1) * textRect.height*1.5
        screen.blit(text, textRect)

def updateMenu(currentState):
    return mainMenu.update(currentState=currentState)

def drawMenu():
    drawStarsInGame()
    mainMenu.draw(screen)

def updateGame(currentState):

    Bullet_Sprite_Group.update()
    EnemyBullet_Sprite_Group.update()

    Enemy_Sprite_Group.update()
    if len(BlowAnimGroup) > 0:
        currentState = BlowAnimGroup.sprites()[0].update(current_state=currentState)
    playerGroup.update()

    enGenerator.update()
    return currentState


def drawGame():
    drawStarsInGame()

    Bullet_Sprite_Group.draw(screen)
    EnemyBullet_Sprite_Group.draw(screen)

    Enemy_Sprite_Group.draw(screen)
    draw_hurts()
    writeScoreInGame()
    playerGroup.draw(screen)
    BlowAnimGroup.draw(screen)


def draw_hurts():
    for hp in range(player.hp):
        screen.blit(player.hpImage, (SCREEN_WIDTH/100, SCREEN_HEIGHT/5*4.5 - hp*player.image.get_height()/1.5))


def writeScoreInGame():

    font = pygame.font.Font("Fonts/joystix monospace.otf", 30 * SCALE)
    text = font.render("Счёт: " + str(player.score), 0, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 30

    screen.blit(text, (SCREEN_WIDTH-textRect.width, SCREEN_HEIGHT - textRect.height))

def drawResults():

    drawStarsInGame()
    font = pygame.font.Font("Fonts/joystix monospace.otf", 75 * SCALE)
    text = font.render("Счёт: " + str(player.score), 0, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-textRect.height

    screen.blit(text, textRect)

    drawStarsInGame()
    font = pygame.font.Font("Fonts/joystix monospace.otf", 50 * SCALE)
    text = font.render("Выход", 0, (255, 255, 0))
    textRect = text.get_rect()
    textRect.center = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2+textRect.height

    screen.blit(text, textRect)


def main(currentState):

    running = True

    while running:

        screen.fill('black')
        if currentState == "Close":
            running = False
        if currentState == "MainMenu":
            currentState = updateMenu(currentState)
            if currentState == "Game":
                enGenerator.resetTime()
            drawMenu()

        elif currentState == "Instruction":
            drawInstruction()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_c or event.key == pygame.K_RETURN):
                    currentState = GAME_STATES[1]
                    pygame.event.clear()

        elif currentState == "Game":
            currentState = updateGame(currentState)
            drawGame()


        elif currentState == "DeathScreen":
            drawResults()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_c or event.key == pygame.K_RETURN):
                    currentState = GAME_STATES[1]

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                running = False
                break

        clock.tick(TIME_TICK)

    pygame.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    pygame.init()
    pygame.display.set_caption("Game")

    screen = pygame.display.set_mode(SCREEN)#, flags=pygame.FULLSCREEN) #, flags=pygame.NOFRAME)

    clock = pygame.time.Clock()

    player = Player((SCREEN_WIDTH/2, SCREEN_HEIGHT/3*2), 50)
    playerGroup = pygame.sprite.GroupSingle()
    playerGroup.sprite = player

    enGenerator = EnemyController(player)
    mainMenu = MainMenu()

    currentState = "Instruction"
    main(currentState)
