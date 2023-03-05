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

    def run(self, map, dict_with_game_state, dict_with_units, list_with_bullets):
    # life-cycle of the building
        pass

    def is_inside_hitbox(self, point, range_of_explosion=0):
    # function checks if the unit is hit - point is inside hitbox
    # return True if yes
        return False
    

# ======================================================================


class Factory(Building):
    name = "Factory"
    unit_type = "building"
    unit_level = 1

    def __init__(self, id, coord, angle, player_id, team_id):
    # initialization of the building
        Building.__init__(self, id, coord, angle, player_id, team_id)
        self.list_building_queue = []
        self.production_is_on = False
        self.base_BP = 100
        self.BP = 0
        self.current_production_force = 1

    def run(self, map, dict_with_game_state, dict_with_units, list_with_bullets):
    # life-cycle of the building
        if self.production_is_on and dict_with_game_state["list_with_energy"][self.player_id] > self.current_production_force:
            self.BP += self.current_production_force
            dict_with_game_state["list_with_energy"][self.player_id] -= self.current_production_force
            if self.BP > self.base_BP:
                # make new unit
                new_id = dict_with_game_state["lowest_free_id"]
                dict_with_game_state["lowest_free_id"] += 1
                dict_with_game_state["dict_with_new_units"][new_id] = self.list_building_queue[0]
                # print(type(self.list_building_queue[0]))
                # print(self.list_building_queue[0].__class__) #.__name__))
                dict_with_game_state["dict_with_new_units"][new_id].set_new_id(new_id)
                dict_with_game_state["dict_with_new_units"][new_id].set_new_target((0,0))
                self.remove_unit_from_queue(0)

    def start_production(self):
    # start production of new unit
        if len(self.list_building_queue) > 0:
            self.BP = 0
            self.base_BP = self.list_building_queue[0].price
            self.production_is_on = True

    def add_unit_to_queue(self, unit):
    # add new unit to building queue
        if len(self.list_building_queue) < 10:
            self.list_building_queue.append(unit)
            if len(self.list_building_queue) == 1: # when first element was changed
                self.start_production()

    def remove_unit_from_queue(self, no_of_slot):
    # remove unit from building queue
        if no_of_slot < len(self.list_building_queue):
                del self.list_building_queue[no_of_slot]
                if not no_of_slot: # when first element was changed
                    self.start_production()
                if not len(self.list_building_queue): # when queue is empty
                    self.production_is_on = False
                    self.BP = 0