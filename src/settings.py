import pygame
import os

import math

# window
WIN_WIDTH, WIN_HEIGHT = 1600, 900
# WIN_WIDTH, WIN_HEIGHT = 1260, 720
FRAMERATE = 60

# sprites - units
TANK_PATH = ["imgs","vehicles","tank.png"]
TANK_FRAMES = 2
LIGHT_TRACK_PATH = ["imgs","vehicles","light_track.bmp"]
LIGHT_TRACK_FRAMES = 5
MEDIUM_TRACK_PATH = ["imgs","vehicles","medium_track.bmp"]
MEDIUM_TRACK_FRAMES = 5
HEAVY_TRACK_PATH = ["imgs","vehicles","heavy_track.bmp"]
HEAVY_TRACK_FRAMES = 7
ANT_PATH = ["imgs","vehicles","ant.bmp"]
ANT_FRAMES = 5

TURRET_PATH = ["imgs","vehicles","turret.png"]
LIGHT_CANNON_PATH = ["imgs","vehicles","light_cannon.bmp"]
MEDIUM_CANNON_PATH = ["imgs","vehicles","medium_cannon.bmp"]
MINIGUN_PATH = ["imgs","vehicles","minigun.bmp"]
PLANE_MINIGUN_PATH = ["imgs","vehicles","plane_minigun.bmp"]
SIDE_CANNON_PATH = ["imgs","vehicles","side_cannon.bmp"]

PLANE_PATH = ["imgs","vehicles","plane.bmp"]
PLANE_FRAMES = 4
BOMBER_PATH = ["imgs","vehicles","bomber.bmp"]
BOMBER_FRAMES = 4
STRATEGIC_BOMBER_PATH = ["imgs","vehicles","strategic_bomber.bmp"]
STRATEGIC_BOMBER_FRAMES = 4

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
SNOW_WHITE = (240, 245, 255)
SHALLOW = (140, 240, 255)
SAND = (235, 200, 145)
GRASS = (0, 155, 25)
