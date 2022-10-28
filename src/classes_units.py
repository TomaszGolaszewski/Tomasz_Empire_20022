import pygame
import math
import random

from settings import *
from functions_math import *
from classes_vehicles import *
from classes_turrets import *


class Unit:
    def __init__(self, coord, angle):
    # initialization of the unit
        self.base = Vehicle(coord, angle)
        self.weapon = Turret(coord, angle)

    def draw(self, win, offset_x, offset_y, scale):
    # draw the unit on the screen
        self.base.draw(win, offset_x, offset_y, scale)
        self.weapon.draw(win, offset_x, offset_y, scale)

    def draw_extra_data(self, win, offset_x, offset_y, scale):
    # draw extra data about the unit on the screen
        self.base.draw_extra_data(win, offset_x, offset_y, scale)
        self.weapon.draw_extra_data(win, offset_x, offset_y, scale)

    def run(self, Map):
    # life-cycle of the unit
        self.base.run(Map)
        self.weapon.set_position(self.base.get_position())
        self.weapon.set_angle(self.base.get_angle())
        self.weapon.run()


class Land_unit(Unit):
    def __init__(self, coord, angle):
        # initialization of the land unit
        Unit.__init__(self, coord, angle)

class Light_tank(Land_unit):
    def __init__(self, coord, angle):
        # initialization of the light tank
        Land_unit.__init__(self, coord, angle)
        self.base = Vehicle(coord, angle)
        self.weapon = Turret(coord, angle)