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

        self.hit_box_radius = self.base.hit_box_radius
        self.base_HP = self.base.base_HP
        self.HP = self.base.base_HP
        self.is_alive = True
        self.is_selected = False

        self.coord = coord
        self.angle = angle
        self.player_id = player_id
        self.team_id = team_id


    def draw(self, win, offset_x, offset_y, scale):
    # draw the unit on the screen
        self.base.draw(win, offset_x, offset_y, scale)
        self.weapon.draw(win, offset_x, offset_y, scale)

        if self.is_selected:
            pygame.draw.circle(win, LIME, world2screen(self.coord, offset_x, offset_y, scale), 20, 3)


    def draw_extra_data(self, win, offset_x, offset_y, scale):
    # draw extra data about the unit on the screen
        self.base.draw_extra_data(win, offset_x, offset_y, scale)
        self.weapon.draw_extra_data(win, offset_x, offset_y, scale)


    def draw_HP(self, win, offset_x, offset_y, scale):
    # draw HP bar        
        percentage_of_HP = self.HP / self.base_HP
        start_point = [self.coord[0] - 12 * scale, self.coord[1] + 12 * scale]
        if percentage_of_HP > 0.5:
            color = LIME
        elif percentage_of_HP > 0.25:
            color = YELLOW
        else:
            color = RED
        pygame.draw.line(win, color, 
                    world2screen(start_point, offset_x, offset_y, scale), 
                    world2screen([start_point[0] + 24 * percentage_of_HP * scale, start_point[1]], offset_x, offset_y, scale), int(3 * scale))



    def run(self, map, list_with_units, list_with_bullets):
    # life-cycle of the unit

        if self.is_alive:
            self.base.run(map)
            self.coord = self.base.get_position()
            self.weapon.set_position(self.coord)
            self.angle = self.base.get_angle()
            self.weapon.set_angle(self.angle)
            self.weapon.run(list_with_units, list_with_bullets)
        else:
            x_id, y_id = map.world2id(self.coord)
            map.BOARD[y_id][x_id].degrade(2)


    def get_hit(self, power):
    # function that subtracts damage from HP and kills the unit if necessary
        self.HP -= power
        if self.HP <= 0:
            self.is_alive = False


class Land_unit(Unit):
    def __init__(self, coord, angle, player_id, team_id):
    # initialization of the land unit
        Unit.__init__(self, coord, angle, player_id, team_id)


class Light_tank(Land_unit):
    def __init__(self, coord, angle, player_id, team_id):
    # initialization of the light tank
        Land_unit.__init__(self, coord, angle, player_id, team_id)
        self.base = Light_track(coord, angle, player_id, team_id)
        self.weapon = Light_cannon(coord, angle, player_id, team_id)


    def draw(self, win, offset_x, offset_y, scale):
    # draw the light tank on the screen
        Land_unit.draw(self, win, offset_x, offset_y, scale)

        coord_on_screen = world2screen(self.coord, offset_x, offset_y, scale)

        # draw level indicator
        pygame.draw.line(win, BLACK, coord_on_screen, [coord_on_screen[0], coord_on_screen[1] + 9], 4)
        pygame.draw.line(win, WHITE, coord_on_screen, [coord_on_screen[0], coord_on_screen[1] + 8], 2)

        # draw team circle
        pygame.draw.circle(win, player_color(self.player_id), coord_on_screen, 7, 0)

        # draw unit indicator
        pygame.draw.circle(win, WHITE, coord_on_screen, 4, 1)


class Main_battle_tank(Land_unit):
    def __init__(self, coord, angle, player_id, team_id):
    # initialization of the main battle tank
        Land_unit.__init__(self, coord, angle, player_id, team_id)
        self.base = Medium_track(coord, angle, player_id, team_id)
        self.weapon = Medium_cannon(coord, angle, player_id, team_id)


    def draw(self, win, offset_x, offset_y, scale):
    # draw the main battle on the screen
        Land_unit.draw(self, win, offset_x, offset_y, scale)

        coord_on_screen = world2screen(self.coord, offset_x, offset_y, scale)

        # draw level indicator
        pygame.draw.line(win, BLACK, coord_on_screen, [coord_on_screen[0], coord_on_screen[1] + 9], 7)
        pygame.draw.line(win, WHITE, [coord_on_screen[0] - 2, coord_on_screen[1]], [coord_on_screen[0] - 2, coord_on_screen[1] + 8], 2)
        pygame.draw.line(win, WHITE, [coord_on_screen[0] + 1, coord_on_screen[1]], [coord_on_screen[0] + 1, coord_on_screen[1] + 8], 2)

        # draw team circle
        pygame.draw.circle(win, player_color(self.player_id), coord_on_screen, 7, 0)

        # draw unit indicator
        pygame.draw.circle(win, WHITE, coord_on_screen, 4, 1)


