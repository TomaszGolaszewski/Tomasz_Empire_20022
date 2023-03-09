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
    base_HP = 100

    path = LIGHT_TRACK_PATH
    number_of_frames = LIGHT_TRACK_FRAMES
    min_scale_to_be_visible = 0.125

    def __init__(self, id, coord, angle, player_id, team_id):
    # initialization of the building

    # basic variables     
        self.id = id  
        self.coord = coord
        self.angle = angle
        self.player_id = player_id
        self.team_id = team_id

        self.HP = self.base_HP

    # variables to optimise display
        self.body_radius = 50
        self.hit_box_radius = 50
        self.is_on_screen = True

    # other variables
        self.is_alive = True
        self.to_remove = False
        self.is_selected = False

    def draw(self, win, offset_x, offset_y, scale):
    # draw the building on the screen
        self.is_on_screen = False
        coord_on_screen = world2screen(self.coord, offset_x, offset_y, scale) # coordinates of the unit in the window coordinate system
        body_radius_on_screen = self.body_radius * scale # radius of the body in the scale of the window

        # checking if the unit is on the screen
        if coord_on_screen[0] > - body_radius_on_screen \
                and coord_on_screen[0] < WIN_WIDTH + body_radius_on_screen \
                and coord_on_screen[1] > - body_radius_on_screen \
                and coord_on_screen[1] < WIN_HEIGHT + body_radius_on_screen:

            self.is_on_screen = True
            
            if self.min_scale_to_be_visible <= scale:
                # pygame.draw.circle(win, player_color(self.player_id), coord_on_screen, int(self.body_radius * scale), 0)
                pygame.draw.circle(win, GRAY, coord_on_screen, int(self.body_radius * scale), 0)
                pygame.draw.circle(win, BLACK, coord_on_screen, int(self.body_radius * scale), 1)

            self.draw_level_indicator(win, coord_on_screen)
            self.draw_unit_type_icon(win, coord_on_screen)
            self.draw_unit_application_icon(win, coord_on_screen)

        if self.is_selected:
            pygame.draw.circle(win, LIME, coord_on_screen, 20, 3)       
    
    def draw_level_indicator(self, win, coord_on_screen):
    # draw level indicator
        if self.unit_level == 1:
            pygame.draw.line(win, BLACK, coord_on_screen, [coord_on_screen[0], coord_on_screen[1] + 9], 4)
            pygame.draw.line(win, WHITE, coord_on_screen, [coord_on_screen[0], coord_on_screen[1] + 8], 2)
        elif self.unit_level == 2:
            pygame.draw.line(win, BLACK, coord_on_screen, [coord_on_screen[0], coord_on_screen[1] + 9], 7)
            pygame.draw.line(win, WHITE, [coord_on_screen[0] - 2, coord_on_screen[1]], [coord_on_screen[0] - 2, coord_on_screen[1] + 8], 2)
            pygame.draw.line(win, WHITE, [coord_on_screen[0] + 1, coord_on_screen[1]], [coord_on_screen[0] + 1, coord_on_screen[1] + 8], 2)
        elif self.unit_level == 3:
            pygame.draw.line(win, BLACK, coord_on_screen, [coord_on_screen[0], coord_on_screen[1] + 9], 10)
            pygame.draw.line(win, WHITE, [coord_on_screen[0] - 3, coord_on_screen[1]], [coord_on_screen[0] - 3, coord_on_screen[1] + 8], 2)
            pygame.draw.line(win, WHITE, coord_on_screen, [coord_on_screen[0], coord_on_screen[1] + 8], 2)
            pygame.draw.line(win, WHITE, [coord_on_screen[0] + 3, coord_on_screen[1]], [coord_on_screen[0] + 3, coord_on_screen[1] + 8], 2)

    def draw_unit_type_icon(self, win, coord_on_screen):
    # draw building type icon - factory / generator etc.
        width = 16
        height = 10
        icon_rect = pygame.Rect(coord_on_screen[0] - width / 2, coord_on_screen[1] - height / 2, width, height)
        pygame.draw.rect(win, player_color(self.player_id), icon_rect, 0)
       
    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        pass

    def draw_extra_data(self, win, offset_x, offset_y, scale):
    # draw extra data about the building on the screen
        pass

    def draw_HP(self, win, offset_x, offset_y, scale):
    # draw HP bar
        if self.is_on_screen:   
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
        self.target_for_units = [move_point(coord, 200, angle)]

    def draw_extra_data(self, win, offset_x, offset_y, scale):
    # draw extra data about the building on the screen
        # target
        if len(self.target_for_units):
            last_target = self.coord
            for target in self.target_for_units:
                pygame.draw.line(win, BLUE, world2screen(last_target, offset_x, offset_y, scale), world2screen(target, offset_x, offset_y, scale))
                pygame.draw.circle(win, BLUE, world2screen(target, offset_x, offset_y, scale), 10*scale, 1)
                last_target = target

    def draw_HP(self, win, offset_x, offset_y, scale):
    # draw HP bar
        Building.draw_HP(self, win, offset_x, offset_y, scale)
        # draw status of building queue
        if self.is_on_screen and self.production_is_on: 
            start_point = [self.coord[0] - 12 * scale, self.coord[1] + 15 * scale]
            percentage_of_BP = self.BP / self.base_BP
            pygame.draw.line(win, BLUE, 
                    world2screen(start_point, offset_x, offset_y, scale), 
                    world2screen([start_point[0] + 24 * percentage_of_BP * scale, start_point[1]], offset_x, offset_y, scale), int(3 * scale))

    def run(self, map, dict_with_game_state, dict_with_units, list_with_bullets):
    # life-cycle of the building
        if self.production_is_on and dict_with_game_state["list_with_energy"][self.player_id] > self.current_production_force:
            self.BP += self.current_production_force
            dict_with_game_state["list_with_energy"][self.player_id] -= self.current_production_force
            if self.BP > self.base_BP:
                # make new unit
                new_id = dict_with_game_state["lowest_free_id"]
                dict_with_game_state["lowest_free_id"] += 1
                dict_with_game_state["dict_with_new_units"][new_id] = self.list_building_queue[0].__class__(new_id, self.coord, self.angle, self.player_id, self.team_id, self.id)
                for target in self.target_for_units:
                    dict_with_game_state["dict_with_new_units"][new_id].set_new_target(target)
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


class Land_factory(Factory):
    name = "Land factory"

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw building application icon - land factory / navy factory etc.
        # turned U
        pygame.draw.arc(win, WHITE, [coord_on_screen[0] - 4, coord_on_screen[1] - 3, 8, 8], 0, math.pi, 1)

class Navy_factory(Factory):
    name = "Navy factory"
    unit_level = 2 # TEMP

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw building application icon - land factory / navy factory etc.
        # U
        pygame.draw.arc(win, WHITE, [coord_on_screen[0] - 4, coord_on_screen[1] - 6, 8, 8], math.pi, 0, 1)


# ======================================================================


class Generator(Building):
    name = "Generator"
    unit_type = "building"
    unit_level = 1
    base_HP = 100

    path = LIGHT_TRACK_PATH
    number_of_frames = LIGHT_TRACK_FRAMES
    min_scale_to_be_visible = 0.5

    def __init__(self, id, coord, angle, player_id, team_id):
    # initialization of the building
        Building.__init__(self, id, coord, angle, player_id, team_id)

        # TEMP
        # variables to optimise display
        self.body_radius = 20
        self.hit_box_radius = 20

    def draw_unit_type_icon(self, win, coord_on_screen):
    # draw building type icon - factory / generator etc.
        width = 12
        height = 12
        icon_rect = pygame.Rect(coord_on_screen[0] - width / 2, coord_on_screen[1] - height / 2, width, height)
        pygame.draw.rect(win, player_color(self.player_id), icon_rect, 0)

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw building application icon - land factory / navy factory etc.
        points = [
            (coord_on_screen[0], coord_on_screen[1] - 4), # top
            (coord_on_screen[0] - 3, coord_on_screen[1]), # left
            (coord_on_screen[0] + 2, coord_on_screen[1]), # right
            (coord_on_screen[0], coord_on_screen[1] + 3), # bottom
        ]
        pygame.draw.lines(win, WHITE, False, points, 1)

    def run(self, map, dict_with_game_state, dict_with_units, list_with_bullets):
        # life-cycle of the building
            dict_with_game_state["list_with_energy"][self.player_id] += 1