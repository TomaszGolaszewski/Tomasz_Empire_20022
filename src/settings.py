import pygame
import os

import math

# window
# WIN_WIDTH, WIN_HEIGHT = 1600, 900
WIN_WIDTH, WIN_HEIGHT = 1260, 720
FRAMERATE = 60

# sprites - units
TANK_PATH = ["imgs","vehicles","tank.png"]
LIGHT_TRACK_PATH = ["imgs","vehicles","light_track.bmp"]
MEDIUM_TRACK_PATH = ["imgs","vehicles","medium_track.bmp"]

TURRET_PATH = ["imgs","vehicles","turret.png"]
LIGHT_CANNON_PATH = ["imgs","vehicles","light_cannon.bmp"]
MEDIUM_CANNON_PATH = ["imgs","vehicles","medium_cannon.bmp"]

# sprites - other
ICON_PATH = ["imgs","other","icon.png"]

# colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIME = (0, 255, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
ORANGE = (255, 95, 30)
WHITE = (255, 255, 255)

SILVER = (192, 192, 192)
GRAY = (128, 128, 128)
LIGHTSLATEGRAY = (119, 136, 153)
DARKSTEELGRAY = (67,70,75)

DEEPPINK = (255,20,147)
HOTPINK = (255,105,180)

MARS_RED = (150, 40, 50)
