import pygame
import math
import random

from settings import *
from functions_math import *
from functions_player import *
from classes_vehicles import *
from classes_planes import *
from classes_turrets import *


class Unit:
    Vehicle_class = Vehicle
    Main_weapon_class = Turret

    unit_type = "none"
    unit_level = 0

    def __init__(self, coord, angle, player_id, team_id):
    # initialization of the unit
        self.base = self.Vehicle_class(coord, angle, player_id, team_id)
        self.weapon = self.Main_weapon_class(coord, angle, player_id, team_id)

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

        coord_on_screen = world2screen(self.coord, offset_x, offset_y, scale)
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
    # draw unit type icon - land / air / navy / etc.
    # previously: draw team circle
        pygame.draw.circle(win, player_color(self.player_id), coord_on_screen, 7, 0)

        
    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        pass


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
            self.base.run(map, list_with_units)
            self.coord = self.base.get_position()
            self.weapon.set_position(self.coord)
            self.angle = self.base.get_angle()
            self.weapon.set_angle(self.angle)
            self.weapon.run(list_with_units, list_with_bullets)
        else:
            map.degrade(self.coord, 2)


    def get_hit(self, power):
    # function that subtracts damage from HP and kills the unit if necessary
        self.HP -= power
        if self.HP <= 0:
            self.is_alive = False


# ======================================================================


class Land_unit(Unit):
    unit_type = "land"

    def draw_unit_type_icon(self, win, coord_on_screen):
    # draw unit type icon - LAND / air / navy / etc.
        pygame.draw.circle(win, player_color(self.player_id), coord_on_screen, 7, 0)


class Light_tank(Land_unit):
    Vehicle_class = Light_track
    Main_weapon_class = Light_cannon

    unit_level = 1

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        # o
        pygame.draw.circle(win, WHITE, coord_on_screen, 4, 1)


class Main_battle_tank(Land_unit):
    Vehicle_class = Medium_track
    Main_weapon_class = Medium_cannon

    unit_level = 2

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        # o
        pygame.draw.circle(win, WHITE, coord_on_screen, 4, 1)


class Heavy_tank(Land_unit):
    Vehicle_class = Heavy_track
    Main_weapon_class = Minigun

    unit_level = 3

    def __init__(self, coord, angle, player_id, team_id):
    # initialization of the heavy tank
        Land_unit.__init__(self, coord, angle, player_id, team_id)
        self.weapon2 = Side_cannon(coord, angle, player_id, team_id)
        self.weapon3 = Side_cannon(coord, angle, player_id, team_id)


    def draw(self, win, offset_x, offset_y, scale):
    # draw the heavy tank on the screen

        self.base.draw(win, offset_x, offset_y, scale)
        self.weapon.draw(win, offset_x, offset_y, scale)
        self.weapon2.draw(win, offset_x, offset_y, scale)
        self.weapon3.draw(win, offset_x, offset_y, scale)

        coord_on_screen = world2screen(self.coord, offset_x, offset_y, scale)
        self.draw_level_indicator(win, coord_on_screen)
        self.draw_unit_type_icon(win, coord_on_screen)
        self.draw_unit_application_icon(win, coord_on_screen)

        if self.is_selected:
            pygame.draw.circle(win, LIME, coord_on_screen, 20, 3)


    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        # o
        pygame.draw.circle(win, WHITE, coord_on_screen, 4, 1)

    
    def draw_extra_data(self, win, offset_x, offset_y, scale):
    # draw extra data about the heavy tank on the screen
        Air_unit.draw_extra_data(self, win, offset_x, offset_y, scale)
        self.weapon2.draw_extra_data(win, offset_x, offset_y, scale)
        self.weapon3.draw_extra_data(win, offset_x, offset_y, scale)

    
    def run(self, map, list_with_units, list_with_bullets):
    # life-cycle of the heavy tank
        Air_unit.run(self, map, list_with_units, list_with_bullets)
        if self.is_alive:
            x = 0
            y = 16          
            self.weapon2.set_position((self.coord[0] + x * math.cos(self.angle) + y * math.sin(self.angle), self.coord[1] + x * math.sin(self.angle) - y * math.cos(self.angle)))
            self.weapon3.set_position((self.coord[0] + x * math.cos(self.angle) - y * math.sin(self.angle), self.coord[1] + x * math.sin(self.angle) + y * math.cos(self.angle)))
            self.weapon2.set_angle(self.angle)
            self.weapon3.set_angle(self.angle)
            self.weapon2.run(list_with_units, list_with_bullets)
            self.weapon3.run(list_with_units, list_with_bullets)


class Spider_tank(Land_unit):
    Vehicle_class = Ant
    Main_weapon_class = Minigun

    unit_level = 2

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        # +
        pygame.draw.line(win, WHITE, [coord_on_screen[0] - 3, coord_on_screen[1]], [coord_on_screen[0] + 3, coord_on_screen[1]], 1) # -
        pygame.draw.line(win, WHITE, [coord_on_screen[0], coord_on_screen[1] - 3], [coord_on_screen[0], coord_on_screen[1] + 3], 1) # |


# ======================================================================


class Air_unit(Unit):
    unit_type = "air"

    def draw_unit_type_icon(self, win, coord_on_screen):
    # draw unit type icon - land / AIR / navy / etc.

        pygame.draw.polygon(win, player_color(self.player_id), [
            (coord_on_screen[0], coord_on_screen[1] - 8),
            (coord_on_screen[0] - 6, coord_on_screen[1] + 5),
            (coord_on_screen[0] + 6, coord_on_screen[1] + 5)
        ], 0)    


class Fighter(Air_unit):
    Vehicle_class = Plane
    Main_weapon_class = Plane_fixed_gun

    unit_level = 2

    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        # A
        pygame.draw.line(win, WHITE, [coord_on_screen[0] - 3, coord_on_screen[1] + 3], [coord_on_screen[0], coord_on_screen[1] - 3], 1) # /
        pygame.draw.line(win, WHITE, [coord_on_screen[0] + 3, coord_on_screen[1] + 3], [coord_on_screen[0], coord_on_screen[1] - 3], 1) # \


class Bomber(Air_unit):
    Vehicle_class = Plane_bomber
    Main_weapon_class = Empty_slot

    unit_level = 2

    def __init__(self, coord, angle, player_id, team_id):
    # initialization of the bomber
        Air_unit.__init__(self, coord, angle, player_id, team_id)
        self.weapon2 = Plane_minigun(coord, angle, player_id, team_id)


    def draw(self, win, offset_x, offset_y, scale):
    # draw the bomber on the screen
       
        self.base.draw(win, offset_x, offset_y, scale)
        self.weapon.draw(win, offset_x, offset_y, scale)
        self.weapon2.draw(win, offset_x, offset_y, scale)

        coord_on_screen = world2screen(self.coord, offset_x, offset_y, scale)
        self.draw_level_indicator(win, coord_on_screen)
        self.draw_unit_type_icon(win, coord_on_screen)
        self.draw_unit_application_icon(win, coord_on_screen)

        if self.is_selected:
            pygame.draw.circle(win, LIME, coord_on_screen, 20, 3)


    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        pygame.draw.line(win, WHITE, [coord_on_screen[0] - 3, coord_on_screen[1] - 3], [coord_on_screen[0], coord_on_screen[1] + 3], 1) # \
        pygame.draw.line(win, WHITE, [coord_on_screen[0] + 3, coord_on_screen[1] - 3], [coord_on_screen[0], coord_on_screen[1] + 3], 1) # /


    def draw_extra_data(self, win, offset_x, offset_y, scale):
    # draw extra data about the bomber on the screen
        Air_unit.draw_extra_data(self, win, offset_x, offset_y, scale)
        self.weapon2.draw_extra_data(win, offset_x, offset_y, scale)

    
    def run(self, map, list_with_units, list_with_bullets):
    # life-cycle of the bomber
        Air_unit.run(self, map, list_with_units, list_with_bullets)
        if self.is_alive:
            self.weapon2.set_position(self.coord)
            self.weapon2.set_angle(self.angle)
            self.weapon2.run(list_with_units, list_with_bullets)


class Strategic_bomber(Air_unit):
    Vehicle_class = Plane_strategic_bomber
    Main_weapon_class = Empty_slot

    unit_level = 3

    def __init__(self, coord, angle, player_id, team_id):
    # initialization of the strategic bomber
        Air_unit.__init__(self, coord, angle, player_id, team_id)
        self.weapon2 = Plane_minigun(coord, angle, player_id, team_id)
        self.weapon3 = Plane_minigun(coord, angle, player_id, team_id)


    def draw(self, win, offset_x, offset_y, scale):
    # draw the strategic bomber on the screen

        self.base.draw(win, offset_x, offset_y, scale)
        self.weapon.draw(win, offset_x, offset_y, scale)
        self.weapon2.draw(win, offset_x, offset_y, scale)
        self.weapon3.draw(win, offset_x, offset_y, scale)

        coord_on_screen = world2screen(self.coord, offset_x, offset_y, scale)
        self.draw_level_indicator(win, coord_on_screen)
        self.draw_unit_type_icon(win, coord_on_screen)
        self.draw_unit_application_icon(win, coord_on_screen)

        if self.is_selected:
            pygame.draw.circle(win, LIME, coord_on_screen, 20, 3)


    def draw_unit_application_icon(self, win, coord_on_screen):
    # draw unit application icon - tank / anti-aircraft / bomber / etc.
        pygame.draw.line(win, WHITE, [coord_on_screen[0] - 3, coord_on_screen[1] - 3], [coord_on_screen[0], coord_on_screen[1] + 3], 1) # \
        pygame.draw.line(win, WHITE, [coord_on_screen[0] + 3, coord_on_screen[1] - 3], [coord_on_screen[0], coord_on_screen[1] + 3], 1) # /


    def draw_extra_data(self, win, offset_x, offset_y, scale):
    # draw extra data about the strategic bomber on the screen
        Air_unit.draw_extra_data(self, win, offset_x, offset_y, scale)
        self.weapon2.draw_extra_data(win, offset_x, offset_y, scale)
        self.weapon3.draw_extra_data(win, offset_x, offset_y, scale)

    
    def run(self, map, list_with_units, list_with_bullets):
    # life-cycle of the strategic bomber
        Air_unit.run(self, map, list_with_units, list_with_bullets)
        if self.is_alive:
            x = -6
            y = 16          
            self.weapon2.set_position((self.coord[0] + x * math.cos(self.angle) + y * math.sin(self.angle), self.coord[1] + x * math.sin(self.angle) - y * math.cos(self.angle)))
            self.weapon3.set_position((self.coord[0] + x * math.cos(self.angle) - y * math.sin(self.angle), self.coord[1] + x * math.sin(self.angle) + y * math.cos(self.angle)))
            self.weapon2.set_angle(self.angle)
            self.weapon3.set_angle(self.angle)
            self.weapon2.run(list_with_units, list_with_bullets)
            self.weapon3.run(list_with_units, list_with_bullets)