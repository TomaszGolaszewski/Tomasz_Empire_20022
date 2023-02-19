import pygame
import math
import random

from setup import *
from functions_player import *
from classes_units import *


class Building:
    unit_type = "building"
    unit_level = 0

    def __init__(self, coord, angle, player_id, team_id):
    # initialization of the building

    # basic variables       
        self.coord = coord
        self.angle = angle
        self.player_id = player_id
        self.team_id = team_id

    # variables to optimise display
        self.body_radius = 50
        self.hit_box_radius = 50
        # self.min_scale_to_be_visible = self.base.min_scale_to_be_visible
        self.is_on_screen = True

    # other variables
        self.is_alive = True
        self.to_remove = False
        self.is_selected = False

    def draw(self, win, offset_x, offset_y, scale):
    # draw the building on the screen
        coord_on_screen = world2screen(self.coord, offset_x, offset_y, scale)
        pygame.draw.circle(win, player_color(self.player_id), coord_on_screen, int(self.body_radius * scale), 0)
        pygame.draw.circle(win, BLACK, coord_on_screen, int(self.body_radius * scale), 1)

    def draw_extra_data(self, win, offset_x, offset_y, scale):
    # draw extra data about the building on the screen
        pass

    def draw_HP(self, win, offset_x, offset_y, scale):
    # draw HP bar
        pass

    def run(self, map, list_with_units, list_with_bullets):
    # life-cycle of the building
        pass

    def is_inside_hitbox(self, point, range_of_explosion=0):
    # function checks if the unit is hit - point is inside hitbox
    # return True if yes
        return False