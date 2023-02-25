import pygame
import math
import random

from setup import *
from functions_player import *
from classes_units import *
# from classes_ui import *


class Building:
    name = "Building"
    unit_type = "building"
    unit_level = 0

    def __init__(self, id, coord, angle, player_id, team_id):
    # initialization of the building

    # basic variables     
        self.id = id  
        self.coord = coord
        self.angle = angle
        self.player_id = player_id
        self.team_id = team_id

    # # objects
    #     self.Shop_window = Base_notebook()

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

        if self.is_selected:
            pygame.draw.circle(win, LIME, coord_on_screen, 20, 3)       

    def draw_extra_data(self, win, offset_x, offset_y, scale):
    # draw extra data about the building on the screen
        pass

    def draw_HP(self, win, offset_x, offset_y, scale):
    # draw HP bar
        pass

    def draw_windows(self, win):
    # draw windows with unit's infos and controls
        pass
        # if self.is_selected:
        #     self.Shop_window.draw(win)

    def run(self, map, dict_with_units, list_with_bullets):
    # life-cycle of the building
        pass

    def is_inside_hitbox(self, point, range_of_explosion=0):
    # function checks if the unit is hit - point is inside hitbox
    # return True if yes
        return False