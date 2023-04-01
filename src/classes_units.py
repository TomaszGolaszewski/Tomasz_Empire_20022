import pygame
import math
import random

# from settings import *
from setup import *
from functions_math import *
from functions_player import *
from classes_body_vehicles import *
from classes_body_ships import *
from classes_body_planes import *
from classes_turrets import *


class Unit:
    Vehicle_class = Vehicle
    # [(class, (x, y, alpha))]
    Weapon_classes = [(Turret, (0, 0, 0))]
    name = "Unit"
    unit_type = "none"
    unit_level = 0
    price = FRAMERATE * 5
    visibility_after_death = FRAMERATE * 10

    def __init__(self, id, coord, angle, player_id, team_id, factory_id=0):
    # initialization of the unit

        # basic variables
        self.id = id       
        self.coord = coord
        self.angle = angle
        self.player_id = player_id
        self.team_id = team_id

        # initialization of the base
        self.base = self.Vehicle_class(id, coord, angle, player_id, team_id, factory_id)
        self.hit_box_radius = self.base.hit_box_radius
        self.base_HP = self.base.base_HP
        self.HP = self.base.base_HP
        self.v_max = self.base.v_max

        # variables to optimise display
        self.body_radius = self.base.body_radius
        self.min_scale_to_be_visible = self.base.min_scale_to_be_visible
        # self.visibility_after_death = FRAMERATE * 5
        self.is_on_screen = False

        # initialization of the weapon
        self.Weapons = []
        for weapon_class in self.Weapon_classes:
            x = weapon_class[1][0]
            y = weapon_class[1][1]
            weapon_x = self.coord[0] + x * math.cos(self.angle) + y * math.sin(self.angle)
            weapon_y = self.coord[1] + x * math.sin(self.angle) - y * math.cos(self.angle)
            self.Weapons.append(weapon_class[0](id, (weapon_x, weapon_y), angle, weapon_class[1][2], player_id, team_id))

        # other variables
        self.is_alive = True
        self.to_remove = False
        self.is_selected = False
        self.countdown_to_AI_activity = FRAMERATE

    def draw(self, win, offset_x, offset_y, scale):
    # draw the unit on the screen
        self.is_on_screen = False
        coord_on_screen = world2screen(self.coord, offset_x, offset_y, scale) # coordinates of the unit in the window coordinate system
        body_radius_on_screen = self.body_radius * scale # radius of the body in the scale of the window

        # checking if the unit is on the screen
        if coord_on_screen[0] > - body_radius_on_screen \
                and coord_on_screen[0] < WIN_WIDTH + body_radius_on_screen \
                and coord_on_screen[1] > - body_radius_on_screen \
                and coord_on_screen[1] < WIN_HEIGHT + body_radius_on_screen:

            self.is_on_screen = True
            
            # checking if the unit is still alive
            if self.is_alive:
                if self.min_scale_to_be_visible <= scale:
                    self.base.draw(win, offset_x, offset_y, scale)
                    for weapon in self.Weapons:
                        weapon.draw(win, offset_x, offset_y, scale)
      
                self.draw_level_indicator(win, coord_on_screen)
                self.draw_unit_type_icon(win, coord_on_screen)
                self.draw_unit_application_icon(win, coord_on_screen)

                if self.is_selected:
                    pygame.draw.circle(win, LIME, coord_on_screen, 20, 3)
            # if the unit is dead
            else:
                # pygame.draw.circle(win, player_color(self.player_id), coord_on_screen, int(body_radius_on_screen), 0)
                self.base.draw(win, offset_x, offset_y, scale)

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
    # draw unit type icon - land / air / navy / etc.
    # previously: draw team circle
        pygame.draw.circle(win, player_color(self.player_id), coord_on_screen, 7, 0)
       
    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        pass

    def draw_extra_data(self, win, offset_x, offset_y, scale):
    # draw extra data about the unit on the screen
        self.base.draw_extra_data(win, offset_x, offset_y, scale)
        for weapon in self.Weapons:
            weapon.draw_extra_data(win, offset_x, offset_y, scale)

    def draw_HP(self, win, offset_x, offset_y, scale):
    # draw HP bar     
        if self.is_alive:   
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
    # life-cycle of the unit     
        if self.is_alive:
            # running the base
            self.base.run(map, dict_with_units)
            self.coord = self.base.get_position()
            self.angle = self.base.get_angle()
            # running the weapons
            i = 0 # only to get position of the weapon on the unit from Weapon_classes list
            for weapon in self.Weapons:
                x = self.Weapon_classes[i][1][0]
                y = self.Weapon_classes[i][1][1]
                weapon_x = self.coord[0] + x * math.cos(self.angle) + y * math.sin(self.angle)
                weapon_y = self.coord[1] + x * math.sin(self.angle) - y * math.cos(self.angle)
                weapon.set_position((weapon_x, weapon_y))
                weapon.set_angle(self.angle)
                weapon.run(dict_with_units, list_with_bullets)
                i += 1
        else:
            # self.body_radius -= 1
            # if self.body_radius <= 0:
            self.base.run_after_death()
            self.visibility_after_death -= 1
            if self.visibility_after_death <= 0:
                # map.degrade(self.coord, 2)
                self.to_remove = True

    def AI_run(self, map, dict_with_game_state, dict_with_units):
    # AI activity
        if self.is_alive and dict_with_game_state["list_with_player_type"][self.player_id] == "AI":
            if not self.countdown_to_AI_activity:
                self.countdown_to_AI_activity = FRAMERATE

                # try to find closest target
                temp_coord = [0, 0]
                temp_dist = 9999
                for unit_id in dict_with_units:
                    if dict_with_units[unit_id].team_id != self.team_id and dict_with_units[unit_id].player_id and dict_with_units[unit_id].is_alive:
                        if self.is_valid_target_for_AI(dict_with_units[unit_id].unit_type):
                            dist = math.hypot(self.coord[0]-dict_with_units[unit_id].coord[0], self.coord[1]-dict_with_units[unit_id].coord[1])
                            if dist < temp_dist:
                                temp_coord = dict_with_units[unit_id].coord
                                temp_dist = dist
                # self.set_new_target(temp_coord, True)
                self.set_new_target_with_path_checking(map, temp_coord)
            else:
                self.countdown_to_AI_activity -= 1

    def is_valid_target_for_AI(self, unit_type):
    # checks (by unit type) if the target can be targeted
    # return True if target is valid
        if unit_type == "land" or unit_type == "building": return True
        else: return False

    def get_hit(self, map, power):
    # function that subtracts damage from HP and kills the unit if necessary
        self.HP -= power
        if self.HP <= 0:
            self.is_alive = False
            self.base.state = 'dead'
            map.degrade(self.coord, 2)

    def is_inside_hitbox(self, point, range_of_explosion=0):
    # function checks if the unit is hit - point is inside hitbox
    # return True if yes
        if self.is_alive:
            # if dist_two_points(self.coord, point) < self.hit_box_radius + range_of_explosion:
            if math.hypot(self.coord[0]-point[0], self.coord[1]-point[1]) < self.hit_box_radius + range_of_explosion:
                return True    
        return False

    def set_v_max_squad(self, v_max_squad):
    # set new max velocity for moving unit with his squad
        self.base.v_max_squad = v_max_squad

    def set_new_id(self, new_id):
    # set new id to all elements of the unit
        self.id = new_id
        self.base.id = new_id
        for weapon in self.Weapons:
            weapon.id = new_id

    def set_new_target(self, new_target, overwrite=False):
    # set new target of the unit's movement
        if overwrite:
            self.base.movement_target = [new_target]
        else:
            self.base.movement_target.append(new_target)

    def set_new_target_with_path_checking(self, map, new_target):
    # set new target of the unit's movement
        new_path = self.find_safe_path(map, self.coord, new_target, 0)
        new_path.append(new_target)
        self.base.movement_target = new_path

    def find_safe_path(self, map, start_point, end_point, recursion_depth):
    # recursive function returning a list with safe points of the new path
        # check recursion depth
        if recursion_depth > 5: return []
        # for air units, all paths are save
        elif self.unit_type == "air": return []
        # for land units
        elif self.unit_type == "land":
            if map.check_land_path(start_point, end_point): return []
            else:
                middle_point = [(start_point[0] + end_point[0]) / 2, (start_point[1] + end_point[1]) / 2]
                angle = angle_to_target(start_point, end_point)
                middle_point = map.find_safe_middle_point(middle_point, angle, is_land_unit=True)
                path_begining = self.find_safe_path(map, start_point, middle_point, recursion_depth + 1)
                path_begining.append(middle_point)
                return path_begining + self.find_safe_path(map, middle_point, end_point, recursion_depth + 1)
        # for naval units
        elif self.unit_type == "navy":
            if map.check_water_path(start_point, end_point): return []
            else:
                middle_point = [(start_point[0] + end_point[0]) / 2, (start_point[1] + end_point[1]) / 2]
                angle = angle_to_target(start_point, end_point)
                middle_point = map.find_safe_middle_point(middle_point, angle, is_land_unit=False)
                path_begining = self.find_safe_path(map, start_point, middle_point, recursion_depth + 1)
                path_begining.append(middle_point)
                return path_begining + self.find_safe_path(map, middle_point, end_point, recursion_depth + 1)
         # rest of units
        else:
            return []
        

# ======================================================================


class Land_unit(Unit):
    name = "Land unit"
    unit_type = "land"

    def draw_unit_type_icon(self, win, coord_on_screen):
    # draw unit type icon - LAND / air / navy / etc.
        pygame.draw.circle(win, player_color(self.player_id), coord_on_screen, 7, 0)

    def is_valid_target_for_AI(self, unit_type):
    # checks (by unit type) if the target can be targeted
    # return True if target is valid
        if unit_type == "land" or unit_type == "building": return True
        else: return False


class Light_tank(Land_unit):
    name = "Light tank"
    Vehicle_class = Light_track
    Weapon_classes = [(Light_cannon, (0, 0, 0))]
    unit_level = 1
    price = FRAMERATE * 3

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        # o
        pygame.draw.circle(win, WHITE, coord_on_screen, 4, 1)


class Main_battle_tank(Land_unit):
    name = "Main battle tank"
    Vehicle_class = Medium_track
    Weapon_classes = [(Medium_cannon, (0, 0, 0))]
    unit_level = 2
    price = FRAMERATE * 10

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        # o
        pygame.draw.circle(win, WHITE, coord_on_screen, 4, 1)


class Heavy_artillery(Land_unit):
    name = "Heavy artyllery"
    Vehicle_class = Heavy_track_basic
    Weapon_classes = [(Heavy_cannon, (0, 0, 0))]
    unit_level = 3
    price = FRAMERATE * 30

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        # o
        pygame.draw.circle(win, WHITE, coord_on_screen, 4, 1)
        # +
        pygame.draw.line(win, WHITE, [coord_on_screen[0] - 3, coord_on_screen[1]], [coord_on_screen[0] + 3, coord_on_screen[1]], 1) # -
        pygame.draw.line(win, WHITE, [coord_on_screen[0], coord_on_screen[1] - 3], [coord_on_screen[0], coord_on_screen[1] + 3], 1) # |


class Heavy_tank(Land_unit):
    name = "Heavy tank"
    Vehicle_class = Heavy_track
    Weapon_classes = [(Minigun, (0, 0, 0)),
                    (Side_cannon, (0, 16, 7 * math.pi / 4)),
                    (Side_cannon, (0, -16, math.pi / 4))]
    unit_level = 3
    price = FRAMERATE * 30

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        # o
        pygame.draw.circle(win, WHITE, coord_on_screen, 4, 1)


class Spider_tank(Land_unit):
    name = "Spider tank"
    Vehicle_class = Ant
    Weapon_classes = [(Minigun, (0, 0, 0))]
    unit_level = 2
    price = FRAMERATE * 10

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        # +
        pygame.draw.line(win, WHITE, [coord_on_screen[0] - 3, coord_on_screen[1]], [coord_on_screen[0] + 3, coord_on_screen[1]], 1) # -
        pygame.draw.line(win, WHITE, [coord_on_screen[0], coord_on_screen[1] - 3], [coord_on_screen[0], coord_on_screen[1] + 3], 1) # |


class Space_marine(Land_unit):
    name = "Space Marine"
    Vehicle_class = Space_marine_legs
    Weapon_classes = [(Space_marine_top, (0, 0, 0)),
                      (Capture, (0, 0, 0))]
    unit_level = 1
    price = FRAMERATE * 3

    def draw_unit_type_icon(self, win, coord_on_screen):
    # draw unit type icon - LAND / air / navy / etc.
        pygame.draw.circle(win, player_color(self.player_id), coord_on_screen, 7, 0)

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        # o
        pygame.draw.circle(win, WHITE, (coord_on_screen[0], coord_on_screen[1] - 2), 2, 1)
        # |
        pygame.draw.line(win, WHITE, (coord_on_screen[0], coord_on_screen[1]), (coord_on_screen[0], coord_on_screen[1] + 2), 1)
        # leg /
        pygame.draw.line(win, WHITE, (coord_on_screen[0], coord_on_screen[1] + 2), (coord_on_screen[0] - 2, coord_on_screen[1] + 4), 1)
        # leg \
        pygame.draw.line(win, WHITE, (coord_on_screen[0], coord_on_screen[1] + 2), (coord_on_screen[0] + 2, coord_on_screen[1] + 4), 1)
        # arm /
        pygame.draw.line(win, WHITE, (coord_on_screen[0], coord_on_screen[1] - 1), (coord_on_screen[0] - 2, coord_on_screen[1] + 1), 1)
        # arm \
        pygame.draw.line(win, WHITE, (coord_on_screen[0], coord_on_screen[1] - 1), (coord_on_screen[0] + 2, coord_on_screen[1] + 1), 1)

    def AI_run(self, map, dict_with_game_state, dict_with_units):
    # AI activity
        if self.is_alive and dict_with_game_state["list_with_player_type"][self.player_id] == "AI":
            if not self.countdown_to_AI_activity:
                self.countdown_to_AI_activity = FRAMERATE

                # try to find closest target
                temp_coord = [0, 0]
                temp_dist = 9999
                temp_id = 0
                for unit_id in dict_with_units:
                    if dict_with_units[unit_id].team_id != self.team_id and dict_with_units[unit_id].is_alive:
                        if self.is_valid_target_for_AI(dict_with_units[unit_id].unit_type):
                            dist = math.hypot(self.coord[0]-dict_with_units[unit_id].coord[0], self.coord[1]-dict_with_units[unit_id].coord[1])
                            if dist < temp_dist:
                                temp_coord = dict_with_units[unit_id].coord
                                temp_dist = dist
                                temp_id = unit_id
                # if building found, stop the unit in front of that building
                if temp_id:
                    if dict_with_units[temp_id].unit_type == "building":
                        if dict_with_units[temp_id].name == "Land factory": offset = 80
                        elif dict_with_units[temp_id].name == "Navy factory": offset = 80
                        elif dict_with_units[temp_id].name == "Generator": offset = 45
                        else: offset = 10

                        angle = angle_to_target(temp_coord, self.coord)
                        temp_coord = move_point(temp_coord, offset, angle)

                self.set_new_target_with_path_checking(map, temp_coord)
                # self.set_new_target(temp_coord, True)
            else:
                self.countdown_to_AI_activity -= 1

    def is_valid_target_for_AI(self, unit_type):
    # checks (by unit type) if the target can be targeted
    # return True if target is valid
        if unit_type == "land" or unit_type == "building": return True
        else: return False

class Super_space_marine(Space_marine):
    name = "Super Space Marine"
    Vehicle_class = Super_space_marine_legs
    Weapon_classes = [(Super_space_marine_top, (0, 0, 0)),
                      (Capture, (0, 0, 0))]
    unit_level = 2
    price = FRAMERATE * 10

class Commander(Super_space_marine):
    name = "Commander"
    Vehicle_class = Commander_legs
    Weapon_classes = [(Commander_top, (0, 0, 0)),
                      (Capture, (0, 0, 0))]
    
    def draw_unit_application_icon(self, win, coord_on_screen):
        # draw unit application icon - tank / anti-aircraft / bomber / etc.
            # o
            pygame.draw.circle(win, YELLOW, (coord_on_screen[0], coord_on_screen[1] - 2), 2, 0)
            # |
            pygame.draw.line(win, YELLOW, (coord_on_screen[0], coord_on_screen[1]), (coord_on_screen[0], coord_on_screen[1] + 2), 1)
            # leg /
            pygame.draw.line(win, YELLOW, (coord_on_screen[0], coord_on_screen[1] + 2), (coord_on_screen[0] - 2, coord_on_screen[1] + 4), 1)
            # leg \
            pygame.draw.line(win, YELLOW, (coord_on_screen[0], coord_on_screen[1] + 2), (coord_on_screen[0] + 2, coord_on_screen[1] + 4), 1)
            # arm /
            pygame.draw.line(win, YELLOW, (coord_on_screen[0], coord_on_screen[1] - 1), (coord_on_screen[0] - 2, coord_on_screen[1] + 1), 1)
            # arm \
            pygame.draw.line(win, YELLOW, (coord_on_screen[0], coord_on_screen[1] - 1), (coord_on_screen[0] + 2, coord_on_screen[1] + 1), 1)

    def AI_run(self, map, dict_with_game_state, dict_with_units):
    # AI activity
        pass


# ======================================================================


class Air_unit(Unit):
    name = "Air unit"
    unit_type = "air"
    visibility_after_death = FRAMERATE * 3

    def draw_unit_type_icon(self, win, coord_on_screen):
    # draw unit type icon - land / AIR / navy / etc.

        pygame.draw.polygon(win, player_color(self.player_id), [
            (coord_on_screen[0], coord_on_screen[1] - 8),
            (coord_on_screen[0] - 6, coord_on_screen[1] + 5),
            (coord_on_screen[0] + 6, coord_on_screen[1] + 5)
        ], 0)    

    def is_valid_target_for_AI(self, unit_type):
    # checks (by unit type) if the target can be targeted
    # return True if target is valid
        if unit_type == "air": return True
        else: return False


class Fighter(Air_unit):
    name = "Fighter"
    Vehicle_class = Plane
    Weapon_classes = [(Plane_fixed_gun, (0, 0, 0))]
    unit_level = 2
    price = FRAMERATE * 10

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        # A
        pygame.draw.line(win, WHITE, [coord_on_screen[0] - 3, coord_on_screen[1] + 3], [coord_on_screen[0], coord_on_screen[1] - 3], 1) # /
        pygame.draw.line(win, WHITE, [coord_on_screen[0] + 3, coord_on_screen[1] + 3], [coord_on_screen[0], coord_on_screen[1] - 3], 1) # \

    def is_valid_target_for_AI(self, unit_type):
    # checks (by unit type) if the target can be targeted
    # return True if target is valid
        if unit_type == "air": return True
        else: return False


class Bomber(Air_unit):
    name = "Bomber"
    Vehicle_class = Plane_bomber
    Weapon_classes = [(ASM_Launcher, (0, 0, 0)), # (Bomb_dispenser, (0, 0, 0)),
                    (Plane_minigun, (0, 0, 0))]
    unit_level = 2
    price = FRAMERATE * 20

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        pygame.draw.line(win, WHITE, [coord_on_screen[0] - 3, coord_on_screen[1] - 3], [coord_on_screen[0], coord_on_screen[1] + 3], 1) # \
        pygame.draw.line(win, WHITE, [coord_on_screen[0] + 3, coord_on_screen[1] - 3], [coord_on_screen[0], coord_on_screen[1] + 3], 1) # /

    def is_valid_target_for_AI(self, unit_type):
    # checks (by unit type) if the target can be targeted
    # return True if target is valid
        if unit_type == "land" or unit_type == "navy" or unit_type == "building": return True
        else: return False


class Strategic_bomber(Air_unit):
    name = "Strategic bomber"
    Vehicle_class = Plane_strategic_bomber
    Weapon_classes = [(Advanced_bomb_dispenser, (0, 0, 0)),
                    (Plane_minigun, (-6, 16, 0)),
                    (Plane_minigun, (-6, -16, 0))]
    unit_level = 3
    price = FRAMERATE * 30

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        pygame.draw.line(win, WHITE, [coord_on_screen[0] - 3, coord_on_screen[1] - 3], [coord_on_screen[0], coord_on_screen[1] + 3], 1) # \
        pygame.draw.line(win, WHITE, [coord_on_screen[0] + 3, coord_on_screen[1] - 3], [coord_on_screen[0], coord_on_screen[1] + 3], 1) # /

    def is_valid_target_for_AI(self, unit_type):
    # checks (by unit type) if the target can be targeted
    # return True if target is valid
        if unit_type == "land" or unit_type == "navy" or unit_type == "building": return True
        else: return False


# ======================================================================


class Naval_unit(Unit):
    name = "Naval unit"
    unit_type = "navy"

    def draw_unit_type_icon(self, win, coord_on_screen):
    # draw unit type icon - LAND / air / navy / etc.
        pygame.draw.circle(win, player_color(self.player_id), [coord_on_screen[0], coord_on_screen[1]+4], 9, 0, draw_top_left=True, draw_top_right=True)

    def is_valid_target_for_AI(self, unit_type):
    # checks (by unit type) if the target can be targeted
    # return True if target is valid
        if unit_type == "navy": return True
        else: return False


class Small_artillery_ship(Naval_unit):
    name = "Small artillery ship"
    Vehicle_class = Small_ship
    Weapon_classes = [(Medium_cannon, (0, 0, 0))]
    unit_level = 1
    price = FRAMERATE * 10

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        # o
        pygame.draw.circle(win, WHITE, coord_on_screen, 4, 1)


class Small_AA_ship(Naval_unit):
    name = "Small AA ship"
    Vehicle_class = Small_ship
    Weapon_classes = [(Minigun, (0, 0, 0))]
    unit_level = 1
    price = FRAMERATE * 10

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        # +
        pygame.draw.line(win, WHITE, [coord_on_screen[0] - 3, coord_on_screen[1]], [coord_on_screen[0] + 3, coord_on_screen[1]], 1) # -
        pygame.draw.line(win, WHITE, [coord_on_screen[0], coord_on_screen[1] - 3], [coord_on_screen[0], coord_on_screen[1] + 3], 1) # |


class Battle_cruiser(Small_artillery_ship):
    name = "Battle cruiser"
    Vehicle_class = Medium_ship
    Weapon_classes = [(Medium_naval_cannon, (24, 0, 0)),
                    (Medium_naval_cannon, (-32, 0, math.pi))]
    unit_level = 2
    price = FRAMERATE * 30

class Destroyer(Small_artillery_ship):
    name = "Destroyer"
    Vehicle_class = Destroyer_body
    Weapon_classes = [(Heavy_naval_cannon, (43, 0, 0)),
                    (Heavy_naval_cannon, (-64, 0, math.pi)),
                    (Minigun, (16, -8, 0)),
                    (Minigun, (16, 8, 0)),
                    (Minigun, (-22, -11, math.pi)),
                    (Minigun, (-22, 11, math.pi))]
    unit_level = 3
    price = FRAMERATE * 60

class Battleship(Small_AA_ship):
    name = "Battleship"
    Vehicle_class = Battleship_body
    Weapon_classes = [(Heavy_naval_cannon, (85, 0, 0)),
                    (Heavy_naval_cannon, (44, 0, 0)),
                    (Heavy_naval_cannon, (-106, 0, math.pi)),
                    (Heavy_naval_cannon, (-65, 0, math.pi)),
                    (Minigun, (-4, 23, 0)),
                    (Minigun, (-23, 23, 3*math.pi/2)),
                    (Minigun, (-40, 23, math.pi)),
                    (Minigun, (-4, -23, 0)),
                    (Minigun, (-23, -23, math.pi/2)),
                    (Minigun, (-40, -23, math.pi))]
    unit_level = 3
    price = FRAMERATE * 120