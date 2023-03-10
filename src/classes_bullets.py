import pygame
import math
import random

# from settings import *
from setup import *
from functions_math import *


class Bullet:
    speed = 10
    radius = 3
    hit_box_radius = 3

    def __init__(self, coord, angle, max_distance, min_distance, player_id, team_id, power, target_type = "land"):
    # initialization of the bullet
        self.is_alive = True
        self.to_remove = False

        self.coord = coord
        self.angle = angle
        self.player_id = player_id
        self.team_id = team_id
        self.power = power
        self.explosion_radius = power // 10 + 10
        self.explosion_color = RED

        self.target_type = target_type # land / air / navy

        self.distance = 0
        self.max_distance = max_distance
        self.min_distance = min_distance

    def draw(self, win, offset_x, offset_y, scale):
    # draw the bullet on the screen
        if self.is_alive:
            if self.target_type == "air":
                color = RED # SILVER # BLUE
            elif self.target_type == "land": # or self.target_type == "navy":
                color = YELLOW
            elif self.target_type == "navy":
                color = SILVER
            elif self.target_type == "building":
                color = ORANGE
            else:
                color = BLUE # RED

            temp_radius = int(self.radius * scale)
            if temp_radius < 2: temp_radius = 2
            pygame.draw.circle(win, color, world2screen(self.coord, offset_x, offset_y, scale), temp_radius, 0)
        else:
            coord_on_screen = world2screen(self.coord, offset_x, offset_y, scale)
            pygame.draw.circle(win, self.explosion_color, coord_on_screen, int(self.explosion_radius * scale), 0)

    def run(self, map, dict_with_units):
    # life-cycle of the bullet 
        if self.is_alive:
            # checks collision with units
            for unit_id in dict_with_units:
                if self.is_hit(dict_with_units[unit_id]):
                    dict_with_units[unit_id].get_hit(map, self.power)
                    self.explosion_color = ORANGE
                    self.is_alive = False    
            # checks end of life span
            if self.distance > self.max_distance:
                if self.target_type == "land" or self.target_type == "navy" or self.target_type == "building": 
                    map.degrade(self.coord, 2)
                    if map.get_tile_type(self.coord) == "water" or map.get_tile_type(self.coord) == "shallow":
                        self.explosion_color = WHITE
                    else:
                        self.explosion_color = DARKSTEELGRAY
                else: self.explosion_radius = 1 # don't show explosion in the sky
                self.is_alive = False
            # checks collision with trees
            if not self.target_type == "air" and (map.get_tile_type(self.coord) == "forest" or map.get_tile_type(self.coord) == "snow_forest"):
                if not map.get_tile_degradation_level(self.coord):
                    map.degrade(self.coord, 2)
                    self.explosion_color = ORANGE
                    self.is_alive = False

        # if the bullet is still alive - move it
        if self.is_alive:
            self.move()
        # run explosion after death
        else:
            self.explosion_radius -= 1
            if self.explosion_radius <= 0:
                self.to_remove = True

    def move(self):
    # move the bullet forward
        self.distance += self.speed
        self.coord = move_point(self.coord, self.speed, self.angle)

    def is_hit(self, object):
    # function checks if the object is hit
    # return True if yes
        if object.is_alive and object.team_id != self.team_id and object.unit_type == self.target_type and self.distance > self.min_distance:
            return object.is_inside_hitbox(self.coord, self.hit_box_radius)
        #     if dist_two_points(self.coord, object.coord) < object.hit_box_radius + self.hit_box_radius:
        #         return True
      
        # return False



class Plasma(Bullet):
    speed = 15
    radius = 3 # width of beam
    base_length = 6
    hit_box_radius = 3

    def __init__(self, coord, angle, max_distance, min_distance, player_id, team_id, power, target_type):
    # initialization of the plasma beam
        Bullet.__init__(self, coord, angle, max_distance, min_distance, player_id, team_id, power, target_type)
        self.origin_point = coord
        self.length = self.base_length * power // 10
 
    def draw(self, win, offset_x, offset_y, scale):
    # draw the plasma beam on the screen
        if self.is_alive:
            start_point = world2screen(self.coord, offset_x, offset_y, scale)
            if dist_two_points(self.coord, self.origin_point) < self.length:
                end_point = world2screen(self.origin_point, offset_x, offset_y, scale)
            else:
                end_point = world2screen(move_point(self.coord, self.length, self.angle - math.pi), offset_x, offset_y, scale)

            if self.target_type == "air":
                color = RED # SILVER # BLUE
            elif self.target_type == "land":
                color = YELLOW
            elif self.target_type == "navy":
                color = SILVER
            elif self.target_type == "building":
                color = ORANGE
            else:
                color = BLUE # RED

            width = int(self.radius * scale)
            if width < 1: width = 1
            pygame.draw.line(win, color, start_point, end_point, width)

        else:
            coord_on_screen = world2screen(self.coord, offset_x, offset_y, scale)
            pygame.draw.circle(win, self.explosion_color, coord_on_screen, int(self.explosion_radius * scale), 0)


class Bomb(Bullet):
    speed = 1
    radius = 3
    hit_box_radius = 15

    def __init__(self, coord, angle, max_distance, min_distance, player_id, team_id, power, target_type):
    # initialization of the bomb
        self.speed += random.randint(0, 2) * 0.1
        Bullet.__init__(self, coord, angle, max_distance, min_distance, player_id, team_id, power, target_type)



class ASMissile(Bullet):
    speed = 2
    turn_speed = 0.03
    radius = 3
    hit_box_radius = 15

    # def __init__(self, coord, angle, max_distance, min_distance, player_id, team_id, power, target_type):
    # # initialization of the Missile
    #     Bullet.__init__(self, coord, angle, max_distance, min_distance, player_id, team_id, power, target_type)

    def run(self, map, dict_with_units):
    # life-cycle of the missile
        if self.is_alive:
            # checks collision with units
            if self.distance > self.min_distance:
                for unit_id in dict_with_units:
                    if self.is_hit(dict_with_units[unit_id]):
                        dict_with_units[unit_id].get_hit(map, self.power)
                        self.explosion_color = ORANGE
                        self.is_alive = False    
            # checks end of life span
            if self.distance > self.max_distance:
                if self.target_type == "land" or self.target_type == "navy" or self.target_type == "building" or self.target_type == "surface": 
                    map.degrade(self.coord, 2)
                    if map.get_tile_type(self.coord) == "water" or map.get_tile_type(self.coord) == "shallow":
                        self.explosion_color = WHITE
                    else:
                        self.explosion_color = DARKSTEELGRAY
                else: self.explosion_radius = 1 # don't show explosion in the sky
                self.is_alive = False

        # if the bullet is still alive - move it
        if self.is_alive:
            if self.distance > self.min_distance:
                # try to find closest target
                temp_coord = [0, 0]
                temp_dist = 9999
                temp_found_new_target = False

                for unit_id in dict_with_units:
                    if dict_with_units[unit_id].team_id != self.team_id and dict_with_units[unit_id].player_id and dict_with_units[unit_id].is_alive:
                        if self.is_valid_target(dict_with_units[unit_id].unit_type):
                            dist = math.hypot(self.coord[0]-dict_with_units[unit_id].coord[0], self.coord[1]-dict_with_units[unit_id].coord[1])
                            if dist < self.max_distance and dist < temp_dist:
                                temp_coord = dict_with_units[unit_id].coord
                                temp_dist = dist
                                # temp_target_type = unit.unit_type
                                temp_found_new_target = True
                
                # if found, turn to new target
                if temp_found_new_target:
                    self.angle = turn_to_target_angle(self.angle, angle_to_target(self.coord, temp_coord), self.turn_speed)
                
                self.speed += 0.1
            self.move()
        # run explosion after death
        else:
            self.explosion_radius -= 1
            if self.explosion_radius <= 0:
                self.to_remove = True

    def draw(self, win, offset_x, offset_y, scale):
    # draw the missile on the screen
        if self.is_alive:
            color = YELLOW 
            if self.distance > self.min_distance: temp_radius = int(2 * self.radius * scale)
            else: temp_radius = int(self.radius * scale)
            if temp_radius < 2: temp_radius = 2
            pygame.draw.circle(win, color, world2screen(self.coord, offset_x, offset_y, scale), temp_radius, 0)
        else:
            coord_on_screen = world2screen(self.coord, offset_x, offset_y, scale)
            pygame.draw.circle(win, self.explosion_color, coord_on_screen, int(self.explosion_radius * scale), 0)

    def is_valid_target(self, unit_type):
    # checks (by unit type) if the target can be targeted
    # return True if target is valid
        # anti-aircrafts
        if unit_type == "land" or unit_type == "navy" or unit_type == "building": return True
        else: return False

    def is_hit(self, object):
    # function checks if the object is hit
    # return True if yes
        if object.is_alive and object.team_id != self.team_id and object.player_id and (object.unit_type == "land" or object.unit_type == "navy" or object.unit_type == "building") and self.distance > self.min_distance:
            return object.is_inside_hitbox(self.coord, self.hit_box_radius)