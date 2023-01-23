import pygame
import math
import random

from settings import *
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

    unit_type = "none"
    unit_level = 0
    visibility_after_death = FRAMERATE * 10

    def __init__(self, coord, angle, player_id, team_id):
    # initialization of the unit

        # basic variables       
        self.coord = coord
        self.angle = angle
        self.player_id = player_id
        self.team_id = team_id

        # initialization of the base
        self.base = self.Vehicle_class(coord, angle, player_id, team_id)
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
            self.Weapons.append(weapon_class[0]((weapon_x, weapon_y), angle, weapon_class[1][2], player_id, team_id))

        # other variables
        self.is_alive = True
        self.to_remove = False
        self.is_selected = False

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

    def run(self, map, list_with_units, list_with_bullets):
    # life-cycle of the unit     
        if self.is_alive:
            # running the base
            self.base.run(map, list_with_units)
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
                weapon.run(list_with_units, list_with_bullets)
                i += 1
        else:
            # self.body_radius -= 1
            # if self.body_radius <= 0:
            self.base.run_after_death()
            self.visibility_after_death -= 1
            if self.visibility_after_death <= 0:
                # map.degrade(self.coord, 2)
                self.to_remove = True

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
            if dist_two_points(self.coord, point) < self.hit_box_radius + range_of_explosion:
                return True    
        return False

    def set_v_max_squad(self, v_max_squad):
    # set new max velocity for moving unit with his squad
        self.base.v_max_squad = v_max_squad


# ======================================================================


class Land_unit(Unit):
    unit_type = "land"

    def draw_unit_type_icon(self, win, coord_on_screen):
    # draw unit type icon - LAND / air / navy / etc.
        pygame.draw.circle(win, player_color(self.player_id), coord_on_screen, 7, 0)


class Light_tank(Land_unit):
    Vehicle_class = Light_track
    Weapon_classes = [(Light_cannon, (0, 0, 0))]
    unit_level = 1

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        # o
        pygame.draw.circle(win, WHITE, coord_on_screen, 4, 1)


class Main_battle_tank(Land_unit):
    Vehicle_class = Medium_track
    Weapon_classes = [(Medium_cannon, (0, 0, 0))]
    unit_level = 2

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        # o
        pygame.draw.circle(win, WHITE, coord_on_screen, 4, 1)


class Heavy_artillery(Land_unit):
    Vehicle_class = Heavy_track_basic
    Weapon_classes = [(Heavy_cannon, (0, 0, 0))]
    unit_level = 3

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        # o
        pygame.draw.circle(win, WHITE, coord_on_screen, 4, 1)
        # +
        pygame.draw.line(win, WHITE, [coord_on_screen[0] - 3, coord_on_screen[1]], [coord_on_screen[0] + 3, coord_on_screen[1]], 1) # -
        pygame.draw.line(win, WHITE, [coord_on_screen[0], coord_on_screen[1] - 3], [coord_on_screen[0], coord_on_screen[1] + 3], 1) # |


class Heavy_tank(Land_unit):
    Vehicle_class = Heavy_track
    Weapon_classes = [(Minigun, (0, 0, 0)),
                    (Side_cannon, (0, 16, 7 * math.pi / 4)),
                    (Side_cannon, (0, -16, math.pi / 4))]
    unit_level = 3

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        # o
        pygame.draw.circle(win, WHITE, coord_on_screen, 4, 1)


class Spider_tank(Land_unit):
    Vehicle_class = Ant
    Weapon_classes = [(Minigun, (0, 0, 0))]
    unit_level = 2

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        # +
        pygame.draw.line(win, WHITE, [coord_on_screen[0] - 3, coord_on_screen[1]], [coord_on_screen[0] + 3, coord_on_screen[1]], 1) # -
        pygame.draw.line(win, WHITE, [coord_on_screen[0], coord_on_screen[1] - 3], [coord_on_screen[0], coord_on_screen[1] + 3], 1) # |


# ======================================================================


class Air_unit(Unit):
    unit_type = "air"
    visibility_after_death = FRAMERATE * 3

    def draw_unit_type_icon(self, win, coord_on_screen):
    # draw unit type icon - land / AIR / navy / etc.

        pygame.draw.polygon(win, player_color(self.player_id), [
            (coord_on_screen[0], coord_on_screen[1] - 8),
            (coord_on_screen[0] - 6, coord_on_screen[1] + 5),
            (coord_on_screen[0] + 6, coord_on_screen[1] + 5)
        ], 0)    


class Fighter(Air_unit):
    Vehicle_class = Plane
    Weapon_classes = [(Plane_fixed_gun, (0, 0, 0))]
    unit_level = 2

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        # A
        pygame.draw.line(win, WHITE, [coord_on_screen[0] - 3, coord_on_screen[1] + 3], [coord_on_screen[0], coord_on_screen[1] - 3], 1) # /
        pygame.draw.line(win, WHITE, [coord_on_screen[0] + 3, coord_on_screen[1] + 3], [coord_on_screen[0], coord_on_screen[1] - 3], 1) # \


class Bomber(Air_unit):
    Vehicle_class = Plane_bomber
    Weapon_classes = [(Bomb_dispenser, (0, 0, 0)),
                    (Plane_minigun, (0, 0, 0))]
    unit_level = 2


    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        pygame.draw.line(win, WHITE, [coord_on_screen[0] - 3, coord_on_screen[1] - 3], [coord_on_screen[0], coord_on_screen[1] + 3], 1) # \
        pygame.draw.line(win, WHITE, [coord_on_screen[0] + 3, coord_on_screen[1] - 3], [coord_on_screen[0], coord_on_screen[1] + 3], 1) # /


class Strategic_bomber(Air_unit):
    Vehicle_class = Plane_strategic_bomber
    Weapon_classes = [(Advanced_bomb_dispenser, (0, 0, 0)),
                    (Plane_minigun, (-6, 16, 0)),
                    (Plane_minigun, (-6, -16, 0))]
    unit_level = 3

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        pygame.draw.line(win, WHITE, [coord_on_screen[0] - 3, coord_on_screen[1] - 3], [coord_on_screen[0], coord_on_screen[1] + 3], 1) # \
        pygame.draw.line(win, WHITE, [coord_on_screen[0] + 3, coord_on_screen[1] - 3], [coord_on_screen[0], coord_on_screen[1] + 3], 1) # /


# ======================================================================


class Naval_unit(Unit):
    unit_type = "navy"

    def draw_unit_type_icon(self, win, coord_on_screen):
    # draw unit type icon - LAND / air / navy / etc.
        pygame.draw.circle(win, player_color(self.player_id), [coord_on_screen[0], coord_on_screen[1]+4], 9, 0, draw_top_left=True, draw_top_right=True)


class Small_artillery_ship(Naval_unit):
    Vehicle_class = Small_ship
    Weapon_classes = [(Medium_cannon, (0, 0, 0))]
    unit_level = 1

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        # o
        pygame.draw.circle(win, WHITE, coord_on_screen, 4, 1)


class Small_AA_ship(Naval_unit):
    Vehicle_class = Small_ship
    Weapon_classes = [(Minigun, (0, 0, 0))]
    unit_level = 1

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        # +
        pygame.draw.line(win, WHITE, [coord_on_screen[0] - 3, coord_on_screen[1]], [coord_on_screen[0] + 3, coord_on_screen[1]], 1) # -
        pygame.draw.line(win, WHITE, [coord_on_screen[0], coord_on_screen[1] - 3], [coord_on_screen[0], coord_on_screen[1] + 3], 1) # |


class Battle_cruiser(Small_artillery_ship):
    Vehicle_class = Medium_ship
    Weapon_classes = [(Medium_naval_cannon, (24, 0, 0)),
                    (Medium_naval_cannon, (-32, 0, math.pi))]
    unit_level = 2

class Destroyer(Small_artillery_ship):
    Vehicle_class = Destroyer_body
    Weapon_classes = [(Heavy_naval_cannon, (43, 0, 0)),
                    (Heavy_naval_cannon, (-64, 0, math.pi)),
                    (Minigun, (16, -8, 0)),
                    (Minigun, (16, 8, 0)),
                    (Minigun, (-22, -11, math.pi)),
                    (Minigun, (-22, 11, math.pi))]
    unit_level = 3

class Battleship(Small_AA_ship):
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