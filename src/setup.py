import pygame
import os
import math

# game setup
GAME_MAP = "island"
GAME_SHAPE = "horizontal"
GAME_SIZE = "M"
GAME_TREES = False
GAME_PLAYERS = ["AI", "AI", "player", "AI"]

# sprites - units
# land units
LIGHT_TRACK_PATH = ["imgs","vehicles","light_track.bmp"]
LIGHT_TRACK_FRAMES = 4
MEDIUM_TRACK_PATH = ["imgs","vehicles","medium_track.bmp"]
MEDIUM_TRACK_FRAMES = 4
HEAVY_TRACK_PATH = ["imgs","vehicles","heavy_track.bmp"]
HEAVY_TRACK_FRAMES = 6
HEAVY_TRACK_BASIC_PATH = ["imgs","vehicles","heavy_track_basic.bmp"]
HEAVY_TRACK_BASIC_FRAMES = 6
ANT_PATH = ["imgs","vehicles","ant.bmp"]
ANT_FRAMES = 4
SPACE_MARINE_LEGS_PATH = ["imgs","vehicles","space_marine_legs.bmp"]
SPACE_MARINE_LEGS_FRAMES = 4
SUPER_SPACE_MARINE_LEGS_PATH = ["imgs","vehicles","super_space_marine_legs.bmp"]
SUPER_SPACE_MARINE_LEGS_FRAMES = 4
COMMANDER_LEGS_PATH = ["imgs","vehicles","commander_legs.bmp"]
COMMANDER_LEGS_FRAMES = 4
# ships
SMALL_SHIP_PATH = ["imgs","vehicles","small_ship.bmp"]
SMALL_SHIP_FRAMES = 4
MEDIUM_SHIP_PATH = ["imgs","vehicles","medium_ship.bmp"]
MEDIUM_SHIP_FRAMES = 4
DESTROYER_PATH = ["imgs","vehicles","destroyer.bmp"]
DESTROYER_FRAMES = 4
BATTLESHIP_PATH = ["imgs","vehicles","battleship.bmp"]
BATTLESHIP_FRAMES = 4
AIRCRAFT_CARRIER_PATH = ["imgs","vehicles","aircraft_carrier.bmp"]
AIRCRAFT_CARRIER_FRAMES = 4
# planes
PLANE_PATH = ["imgs","vehicles","plane.bmp"]
PLANE_FRAMES = 3
BOMBER_PATH = ["imgs","vehicles","bomber.bmp"]
BOMBER_FRAMES = 3
STRATEGIC_BOMBER_PATH = ["imgs","vehicles","strategic_bomber.bmp"]
STRATEGIC_BOMBER_FRAMES = 5
# weapons
LIGHT_CANNON_PATH = ["imgs","weapons","light_cannon.bmp"]
MEDIUM_CANNON_PATH = ["imgs","weapons","medium_cannon.bmp"]
MINIGUN_PATH = ["imgs","weapons","minigun.bmp"]
PLANE_MINIGUN_PATH = ["imgs","weapons","plane_minigun.bmp"]
SIDE_CANNON_PATH = ["imgs","weapons","side_cannon.bmp"]
HEAVY_CANNON_PATH = ["imgs","weapons","heavy_cannon.bmp"]
MEDIUM_NAVAL_CANNON_PATH = ["imgs","weapons","medium_naval_cannon.bmp"]
HEAVY_NAVAL_CANNON_PATH = ["imgs","weapons","heavy_naval_cannon.bmp"]
SPACE_MARINE_TOP_PATH = ["imgs","weapons","space_marine_top.bmp"]
SUPER_SPACE_MARINE_TOP_PATH = ["imgs","weapons","super_space_marine_top.bmp"]
COMMANDER_TOP_PATH = ["imgs","weapons","commander_top.bmp"]
# buildings
GENERATOR_PATH = ["imgs","buildings","generator.bmp"]
GENERATOR_FRAMES = 4
LAND_FACTORY_PATH = ["imgs","buildings","land_factory.bmp"]
LAND_FACTORY_FRAMES = 4
NAVAL_FACTORY_PATH = ["imgs","buildings","naval_factory.bmp"]
NAVAL_FACTORY_FRAMES = 4

# sprites - map
TREES_PATH = ["imgs","map","trees.bmp"]

# sprites - buttons
BUTTON_1_PATH = ["imgs","buttons","button1.bmp"]
BUTTON_2_PATH = ["imgs","buttons","button2.bmp"]
BUTTON_3_PATH = ["imgs","buttons","button3.bmp"]
BUTTON_4_PATH = ["imgs","buttons","button4.bmp"]
BUTTON_5_PATH = ["imgs","buttons","button5.bmp"]
BUTTON_6_PATH = ["imgs","buttons","button6.bmp"]

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
WATER = (0, 100, 200)
SAND = (235, 200, 145)
GRASS = (0, 155, 25)
