import pygame
import math
import random

from setup import *
from functions_player import *
from classes_base import *
from classes_units import *
# from classes_ui import *


class Building(Base_animated_object):
    name = "Building"
    unit_type = "building"
    unit_level = 0
    price = 0
    base_HP = 1000

    path = GENERATOR_PATH
    number_of_frames = GENERATOR_FRAMES
    number_of_states = 1
    min_scale_to_be_visible = 0.125

    body_radius = 50
    hit_box_radius = 50
    capture_radius = 100

    def __init__(self, id, coord, angle, player_id, team_id):
    # initialization of the building
        Base_animated_object.__init__(self, coord, angle)

        # basic variables     
        self.id = id  
        self.coord = coord
        self.angle = angle
        self.player_id = player_id
        self.team_id = team_id

        self.HP = self.base_HP

        # variables to optimise display
        self.is_on_screen = True

        # other variables
        self.time_to_capture_search = FRAMERATE
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
                # # pygame.draw.circle(win, player_color(self.player_id), coord_on_screen, int(self.body_radius * scale), 0)
                # pygame.draw.circle(win, GRAY, coord_on_screen, int(self.body_radius * scale), 0)
                # pygame.draw.circle(win, BLACK, coord_on_screen, int(self.body_radius * scale), 1)
                Base_animated_object.draw(self, win, offset_x, offset_y, scale)

            self.draw_level_indicator(win, coord_on_screen)
            self.draw_unit_type_icon(win, coord_on_screen)
            self.draw_unit_application_icon(win, coord_on_screen)

        # draw capture circle
        if not self.player_id:
            pygame.draw.circle(win, GRAY, coord_on_screen, int(self.capture_radius * scale), 1)

        # draw select circle
        if self.is_selected:
            pygame.draw.circle(win, LIME, coord_on_screen, 20, 3)     

    def get_frame_index(self):
    # count frame index to get sprite from sprite list
        if self.player_id:
            return self.number_of_frames * (self.unit_level - 1) + self.frame 
        else:
            return self.number_of_frames * (self.unit_level - 1)      
    
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
        # hit box radius
        pygame.draw.circle(win, RED, world2screen(self.coord, offset_x, offset_y, scale), self.hit_box_radius*scale, 1)
        # body radius
        pygame.draw.circle(win, WHITE, world2screen(self.coord, offset_x, offset_y, scale), self.body_radius*scale, 1)

    def draw_movement_target(self, win, offset_x, offset_y, scale):
    # draw extra data about the building movement target
        pass

    def draw_HP(self, win, offset_x, offset_y, scale):
    # draw HP bar
        if self.is_on_screen and self.HP > 0:   
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
        if not self.player_id:
            if not self.time_to_capture_search:
                for unit_id in dict_with_units:
                    if dict_with_units[unit_id].is_alive and \
                                (dict_with_units[unit_id].name == "Space Marine" \
                                or dict_with_units[unit_id].name == "Super Space Marine" \
                                or dict_with_units[unit_id].name == "Commander"):
                        if math.hypot(self.coord[0]-dict_with_units[unit_id].coord[0], self.coord[1]-dict_with_units[unit_id].coord[1]) < self.capture_radius:
                            # capture the building
                            self.player_id = dict_with_units[unit_id].player_id
                            self.team_id = dict_with_units[unit_id].team_id
                            self.HP = self.base_HP
                            break
                self.time_to_capture_search = FRAMERATE
            else:
                self.time_to_capture_search -= 1

    def AI_run(self, map, dict_with_game_state, dict_with_units):
    # AI activity
        pass

    def get_hit(self, map, power):
    # function that subtracts damage from HP and reset building if necessary
        self.HP -= power
        if self.HP < 0:
            self.player_id = 0
            self.team_id = 0
            self.HP = 0

    def is_inside_hitbox(self, point, range_of_explosion=0):
    # function checks if the unit is hit - point is inside hitbox
    # return True if yes
        if self.player_id:
            if math.hypot(self.coord[0]-point[0], self.coord[1]-point[1]) < self.hit_box_radius + range_of_explosion:
                return True    
        return False
    

# ======================================================================


class Factory(Building):
    name = "Factory"
    unit_type = "building"
    unit_level = 1

    path = LAND_FACTORY_PATH
    number_of_frames = LAND_FACTORY_FRAMES
    number_of_states = 3

    def __init__(self, id, coord, angle, player_id, team_id):
    # initialization of the building
        Building.__init__(self, id, coord, angle, player_id, team_id)
        self.list_building_queue = []
        self.production_is_on = False
        self.loop_mode_is_on = False
        self.base_BP = 100
        self.BP = 0
        self.current_production_force = 1
        self.target_for_units = [move_point(coord, 200, angle)]

        # AI variables
        self.energy_spent = 0
        self.countdown_to_AI_activity = FRAMERATE

    def get_frame_index(self):
    # count frame index to get sprite from sprite list
        if self.player_id and self.production_is_on:
            return self.number_of_frames * (self.unit_level - 1) + self.frame 
        else:
            return self.number_of_frames * (self.unit_level - 1)  
        
    def draw_level_indicator(self, win, coord_on_screen):
    # draw level indicator
        Building.draw_level_indicator(self, win, coord_on_screen)
        # upgrade for production speed
        if self.current_production_force > 1:
            pygame.draw.rect(win, BLACK, [coord_on_screen[0] - 12, coord_on_screen[1] - 3 * self.current_production_force + 9, 7, 3 * self.current_production_force + 1], 0)
            for i in range(self.current_production_force):
                pygame.draw.line(win, YELLOW, [coord_on_screen[0] - 11, coord_on_screen[1] + 7 - 3*i], [coord_on_screen[0] - 7, coord_on_screen[1] + 7 - 3*i], 2)

    def draw_extra_data(self, win, offset_x, offset_y, scale):
    # draw extra data about the building on the screen
        # target
        if len(self.target_for_units):
            last_target = self.coord
            for target in self.target_for_units:
                pygame.draw.line(win, BLUE, world2screen(last_target, offset_x, offset_y, scale), world2screen(target, offset_x, offset_y, scale))
                pygame.draw.circle(win, BLUE, world2screen(target, offset_x, offset_y, scale), 10*scale, 1)
                last_target = target
        # hit box radius
        pygame.draw.circle(win, RED, world2screen(self.coord, offset_x, offset_y, scale), self.hit_box_radius*scale, 1)
        # body radius
        pygame.draw.circle(win, WHITE, world2screen(self.coord, offset_x, offset_y, scale), self.body_radius*scale, 1)

    def draw_movement_target(self, win, offset_x, offset_y, scale):
    # draw extra data about the building movement target
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
        Building.run(self, map, dict_with_game_state, dict_with_units, list_with_bullets)
        if self.production_is_on:
            self.BP += self.current_production_force
            if self.BP > self.base_BP:
                # make new unit
                # get a new index
                new_id = dict_with_game_state["lowest_free_id"]
                dict_with_game_state["lowest_free_id"] += 1
                # make new unit
                angle = angle_to_target(self.coord, self.target_for_units[0])
                dict_with_game_state["dict_with_new_units"][new_id] = self.list_building_queue[0].__class__(new_id, self.coord, angle, self.player_id, self.team_id, self.id)
                for target in self.target_for_units:
                    dict_with_game_state["dict_with_new_units"][new_id].set_new_target(target)
                dict_with_game_state["dict_with_new_units"][new_id].set_new_path(self.target_for_units[0], overwrite=True)
                # handle building queue
                if self.loop_mode_is_on:
                    self.move_unit_in_queue_to_end(dict_with_game_state)
                else:
                    self.remove_unit_from_queue(0)

    def AI_run(self, map, dict_with_game_state, dict_with_units):
    # AI activity
        if self.is_alive and dict_with_game_state["list_with_player_type"][self.player_id] == "AI":
            if not self.countdown_to_AI_activity:
                self.countdown_to_AI_activity = FRAMERATE
                # decide about upgrade
                if self.decide_about_upgrade(dict_with_game_state, dict_with_units):
                    # purchase of upgrades
                    self.unit_level += 1
                    dict_with_game_state["list_with_energy"][self.player_id] -= 10000
                    dict_with_game_state["list_with_energy_spent"][self.player_id] += 10000
                # decide and buy new unit
                if self.decide_about_purchase(dict_with_game_state, dict_with_units):
                    selected_class = self.select_unit_for_production(dict_with_game_state, dict_with_units)
                    self.add_unit_to_queue(dict_with_game_state, selected_class(0, self.coord, self.angle, self.player_id, self.team_id))
            else:
                self.countdown_to_AI_activity -= 1

    def decide_about_upgrade(self, dict_with_game_state, dict_with_units):
    # decide on the purchase of upgrades
        if self.unit_level == 1 and self.energy_spent > 1000 \
                    and dict_with_game_state["list_with_energy"][self.player_id] >= 10000:
            return True
        elif self.unit_level == 2 and dict_with_game_state["list_with_energy"][self.player_id] >= 10000:
            for unit_id in dict_with_units:
                if dict_with_units[unit_id].is_alive and \
                        dict_with_units[unit_id].player_id == self.player_id and \
                        dict_with_units[unit_id].unit_level == 1 and \
                        (dict_with_units[unit_id].name == "Land factory" or \
                         dict_with_units[unit_id].name == "Navy factory"):
                    return False
            return True              
        else:
            return False
            
    def decide_about_purchase(self, dict_with_game_state, dict_with_units):
    # decide on the purchase of unit
        if len(self.list_building_queue) < 2 and \
                    ((self.unit_level == 1 and self.energy_spent < 2000) or \
                    (self.unit_level == 2 and self.energy_spent < 10000) or \
                    self.unit_level == 3):
            return True
        else:
            return False

    def select_unit_for_production(self, dict_with_game_state, dict_with_units):
    # select a unit for production based on current indicator levels
        return Space_marine

    def start_production(self):
    # start production of new unit
        self.BP = 0
        if len(self.list_building_queue) > 0:
            self.base_BP = self.list_building_queue[0].price
            self.production_is_on = True
        else:
            self.base_BP = 100
            self.production_is_on = False

    def add_unit_to_queue(self, dict_with_game_state, unit):
    # add new unit to building queue
        if len(self.list_building_queue) < 10 \
                    and dict_with_game_state["list_with_energy"][self.player_id] >= unit.price:
            self.list_building_queue.append(unit)
            dict_with_game_state["list_with_energy"][self.player_id] -= unit.price
            dict_with_game_state["list_with_energy_spent"][self.player_id] += unit.price
            self.energy_spent += unit.price
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

    def move_unit_in_queue_to_end(self, dict_with_game_state):
    # move unit in the queue from the begining (index 0) to the end
        temp_unit_container = self.list_building_queue.pop(0)
        if dict_with_game_state["list_with_energy"][self.player_id] >= temp_unit_container.price:
            self.list_building_queue.append(temp_unit_container)
            dict_with_game_state["list_with_energy"][self.player_id] -= temp_unit_container.price
            dict_with_game_state["list_with_energy_spent"][self.player_id] += temp_unit_container.price
            self.energy_spent += temp_unit_container.price
        self.start_production()

    def get_hit(self, map, power):
    # function that subtracts damage from HP and reset building if necessary
        self.HP -= power
        if self.HP < 0:
            self.player_id = 0
            self.team_id = 0
            self.HP = 0
            self.list_building_queue = []
            self.production_is_on = False
            self.loop_mode_is_on = False
            self.base_BP = 100
            self.BP = 0
            self.energy_spent = 0


class Land_factory(Factory):
    name = "Land factory"

    path = LAND_FACTORY_PATH
    number_of_frames = LAND_FACTORY_FRAMES
    number_of_states = 3

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw building application icon - land factory / navy factory etc.
        # turned U
        pygame.draw.arc(win, WHITE, [coord_on_screen[0] - 4, coord_on_screen[1] - 3, 8, 8], 0, math.pi, 1)

    def select_unit_for_production(self, dict_with_game_state, dict_with_units):
    # select a unit for production based on current indicator levels

        # TODO: add conditions based on used energy
        # if dict_with_game_state["list_with_energy_spent"][self.player_id] > 10000:
        # if dict_with_game_state["list_with_energy_current_production"][self.player_id] > 40:

        if self.unit_level == 1:
            return Space_marine
        
        elif self.unit_level == 2:
            selected_number = random.randint(0,4)
            if selected_number == 0:
                return Super_space_marine
            elif selected_number == 1:
                return Main_battle_tank
            elif selected_number == 2:
                return Spider_tank
            elif selected_number == 3:
                return Bomber
            else:
                return Space_marine
            
        elif self.unit_level == 3:
            selected_number = random.randint(0,4)
            if selected_number == 0:
                return Super_space_marine
            elif selected_number == 1:
                return Heavy_tank
            elif selected_number == 2:
                return Heavy_artillery
            elif selected_number == 3:
                return Strategic_bomber
            else:
                return Space_marine
            
        else:
            return Space_marine

class Navy_factory(Factory):
    name = "Navy factory"

    path = NAVAL_FACTORY_PATH
    number_of_frames = NAVAL_FACTORY_FRAMES
    number_of_states = 3

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw building application icon - land factory / navy factory etc.
        # U
        pygame.draw.arc(win, WHITE, [coord_on_screen[0] - 4, coord_on_screen[1] - 6, 8, 8], math.pi, 0, 1)

    def decide_about_purchase(self, dict_with_game_state, dict_with_units):
    # decide on the purchase of unit
        if len(self.list_building_queue) < 2 and \
                    ((self.unit_level == 1 and self.energy_spent < 2000) or \
                    (self.unit_level == 2 and self.energy_spent < 10000) or \
                    self.unit_level == 3):
            for unit_id in dict_with_units:
                if dict_with_units[unit_id].is_alive and \
                        dict_with_units[unit_id].team_id != self.team_id and \
                        dict_with_units[unit_id].unit_type == "navy":
                    return True
            return False   
        else:
            return False
        
    def select_unit_for_production(self, dict_with_game_state, dict_with_units):
    # select a unit for production based on current indicator levels

        # TODO: add conditions based on used energy
        # if dict_with_game_state["list_with_energy_current_production"][self.player_id] < 0:
        #     self.production_is_on = False
        # elif dict_with_game_state["list_with_energy_current_production"][self.player_id] > 40:
        #     self.production_is_on = True

        # if dict_with_game_state["list_with_energy_spent"][self.player_id] > 10000:

        if self.unit_level == 1:
            return Small_AA_ship
        
        if self.unit_level == 2:
            return Battle_cruiser
        
        if self.unit_level == 3:
            selected_number = random.randint(0,4)
            if selected_number:
                return Destroyer
            else:
                return Battleship
        
        else:
            return Small_AA_ship


# ======================================================================


class Generator(Building):
    name = "Generator"
    unit_type = "building"
    unit_level = 1
    base_HP = 500

    path = GENERATOR_PATH
    number_of_frames = GENERATOR_FRAMES
    number_of_states = 1
    min_scale_to_be_visible = 0.5

    body_radius = 20
    hit_box_radius = 20
    capture_radius = 70

    # def __init__(self, id, coord, angle, player_id, team_id):
    # # initialization of the building
    #     Building.__init__(self, id, coord, angle, player_id, team_id)

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
        Building.run(self, map, dict_with_game_state, dict_with_units, list_with_bullets)
        if self.player_id:
            dict_with_game_state["list_with_energy"][self.player_id] += 1