import pygame
import math
import random

# from settings import *
from setup import *
from functions_math import *
from classes_body_vehicles import *


class Small_ship(Vehicle):
    path = SMALL_SHIP_PATH
    number_of_frames = SMALL_SHIP_FRAMES
    min_scale_to_be_visible = 0.5

    v_max = 0.5
    acceleration = 0.1
    turn_speed = 0.01

    hit_box_radius = 22
    base_HP = 200

    def is_obstacle(self, map, coord):
    # return True if collision with map occurs
        if map.get_tile_type(coord) in ["water", "shallow", "submerged_concrete"]: return False
        else: return True


class Medium_ship(Small_ship):
    path = MEDIUM_SHIP_PATH
    number_of_frames = MEDIUM_SHIP_FRAMES
    min_scale_to_be_visible = 0.25

    v_max = 0.4
    acceleration = 0.1
    turn_speed = 0.005

    hit_box_radius = 35
    base_HP = 600


class Destroyer_body(Small_ship):
    path = DESTROYER_PATH
    number_of_frames = DESTROYER_FRAMES
    min_scale_to_be_visible = 0.125

    v_max = 0.3
    acceleration = 0.1
    turn_speed = 0.005

    hit_box_radius = 60
    base_HP = 2000


class Battleship_body(Small_ship):
    path = BATTLESHIP_PATH
    number_of_frames = BATTLESHIP_FRAMES
    min_scale_to_be_visible = 0.125

    v_max = 0.2
    acceleration = 0.1
    turn_speed = 0.005

    hit_box_radius = 100
    base_HP = 10000


class Aircraft_carrier_body(Small_ship):
    path = AIRCRAFT_CARRIER_PATH
    number_of_frames = AIRCRAFT_CARRIER_FRAMES
    min_scale_to_be_visible = 0.125

    v_max = 0.2
    acceleration = 0.1
    turn_speed = 0.005

    hit_box_radius = 100
    base_HP = 2000