import pygame
import random
from SysConst import SCREEN_WIDTH, SCREEN_HEIGHT


def drawStars(group, speed, size, screen, color):
    for star in group:
        star[1] += speed/2
        if star[1] > SCREEN_HEIGHT:
            star[0] = random.randrange(0, SCREEN_WIDTH)
            star[1] = random.randrange(-20, -5)
        pygame.draw.circle(screen, COLORS[color], star, size)

Star_field_slow = []
Star_field_medium = []
Star_field_fast = []
Star_groups = [Star_field_slow, Star_field_medium, Star_field_fast]

for slow_stars in range(50):
    star_loc_x = random.randrange(0, SCREEN_WIDTH)
    star_loc_y = random.randrange(0, SCREEN_HEIGHT)
    Star_field_slow.append([star_loc_x, star_loc_y])

for medium_stars in range(25):
    star_loc_x = random.randrange(0, SCREEN_WIDTH)
    star_loc_y = random.randrange(0, SCREEN_HEIGHT)
    Star_field_medium.append([star_loc_x, star_loc_y])

for fast_stars in range(15):
    star_loc_x = random.randrange(0, SCREEN_WIDTH)
    star_loc_y = random.randrange(0, SCREEN_HEIGHT)
    Star_field_fast.append([star_loc_x, star_loc_y])

COLORS = [(192, 192, 192), (230, 230, 0), (230, 150, 0),(0, 230, 230)]


# define some commonly used colours
# WHITE = (255, 255, 255)
# LIGHTGREY = (192, 192, 192)
# DARKGREY = (128, 128, 128)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)
# GREEN = (0, 255, 0)
# BLUE = (0, 0, 255)
# YELLOW = (255, 255, 0)
# MAGENTA = (255, 0, 255)
# CYAN = (0, 255, 255)