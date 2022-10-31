import pygame
import math
import random

from settings import *
from functions_math import *
from functions_player import *
from classes_vehicles import *
from classes_turrets import *


class Unit:
    def __init__(self, coord, angle, player_id, team_id):
    # initialization of the unit
        self.base = Vehicle(coord, angle, player_id, team_id)
        self.weapon = Turret(coord, angle, player_id, team_id)

        self.coord = coord
        self.angle = angle
        self.player_id = player_id
        self.team_id = team_id


    def draw(self, win, offset_x, offset_y, scale):
    # draw the unit on the screen
        self.base.draw(win, offset_x, offset_y, scale)
        self.weapon.draw(win, offset_x, offset_y, scale)


    def draw_extra_data(self, win, offset_x, offset_y, scale):
    # draw extra data about the unit on the screen
        self.base.draw_extra_data(win, offset_x, offset_y, scale)
        self.weapon.draw_extra_data(win, offset_x, offset_y, scale)


    def run(self, map, list_with_units):
    # life-cycle of the unit
        self.base.run(map)
        self.coord = self.base.get_position()
        self.weapon.set_position(self.coord)
        self.angle = self.base.get_angle()
        self.weapon.set_angle(self.angle)
        self.weapon.run(list_with_units)


class Land_unit(Unit):
    def __init__(self, coord, angle, player_id, team_id):
    # initialization of the land unit
        Unit.__init__(self, coord, angle, player_id, team_id)


class Light_tank(Land_unit):
    def __init__(self, coord, angle, player_id, team_id):
    # initialization of the light tank
        Land_unit.__init__(self, coord, angle, player_id, team_id)
        self.base = Vehicle(coord, angle, player_id, team_id)
        self.weapon = Turret(coord, angle, player_id, team_id)


    def draw(self, win, offset_x, offset_y, scale):
    # draw the light tank on the screen
        Land_unit.draw(self, win, offset_x, offset_y, scale)

        coord_on_screen = world2screen(self.coord, offset_x, offset_y, scale)

        # draw level indicator
        pygame.draw.line(win, BLACK, coord_on_screen, [coord_on_screen[0], coord_on_screen[1] + 8], 3)
        pygame.draw.line(win, WHITE, coord_on_screen, [coord_on_screen[0], coord_on_screen[1] + 7], 1)

        # draw team circle
        pygame.draw.circle(win, player_color(self.player_id), coord_on_screen, 6, 0)

        # draw unit indicator
        pygame.draw.circle(win, WHITE, coord_on_screen, 3, 1)


