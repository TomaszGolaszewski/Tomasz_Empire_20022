import pygame
import math
import random

from settings import *
from functions_math import *


class Bullet:
    speed = 10
    radius = 3
    hit_box_radius = 3

    def __init__(self, coord, angle, max_distance, min_distance, player_id, team_id, power, target_type = "land"):
    # initialization of the bullet
        self.is_alive = True

        self.coord = coord
        self.angle = angle
        self.player_id = player_id
        self.team_id = team_id
        self.power = power

        self.target_type = target_type # land / air

        self.distance = 0
        self.max_distance = max_distance
        self.min_distance = min_distance


    def draw(self, win, offset_x, offset_y, scale):
    # draw the bullet on the screen
        if self.target_type == "air":
            color = RED # SILVER # BLUE
        elif self.target_type == "land":
            color = YELLOW
        else:
            color = BLUE # RED
        pygame.draw.circle(win, color, world2screen(self.coord, offset_x, offset_y, scale), self.radius*scale, 0)


    def run(self, map, list_of_units):
    # life-cycle of the bullet 
        # checks collision with units
        for unit in list_of_units:
            if self.is_hit(unit):
                unit.get_hit(self.power)
                self.is_alive = False    
        # checks end of life span
        if self.distance > self.max_distance:
            if self.target_type == "land": map.degrade(self.coord, 2)
            self.is_alive = False
        # checks collision with trees
        if map.get_tile_type(self.coord) == "forest" or map.get_tile_type(self.coord) == "snow_forest":
            if not map.get_tile_degradation_level(self.coord):
                map.degrade(self.coord, 2)
                self.is_alive = False
        # if the bullet is still alive - move it
        if self.is_alive:
            self.move()


    def move(self):
    # move the bullet forward
        self.distance += self.speed
        self.coord = move_point(self.coord, self.speed, self.angle)

    
    def is_hit(self, object):
    # function checks if the object is hit
    # return True if yes
        if object.is_alive and object.team_id != self.team_id and object.unit_type == self.target_type and self.distance > self.min_distance:
            if dist_two_points(self.coord, object.coord) < object.hit_box_radius + self.hit_box_radius:
                return True
        
        return False



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
        start_point = world2screen(self.coord, offset_x, offset_y, scale)
        if dist_two_points(self.coord, self.origin_point) < self.length:
            end_point = world2screen(self.origin_point, offset_x, offset_y, scale)
        else:
            end_point = world2screen(move_point(self.coord, self.length, self.angle - math.pi), offset_x, offset_y, scale)

        if self.target_type == "air":
            color = RED # SILVER # BLUE
        elif self.target_type == "land":
            color = YELLOW
        else:
            color = BLUE # RED

        pygame.draw.line(win, color, start_point, end_point, int(self.radius * scale))


class Bomb(Bullet):
    speed = 1
    radius = 3
    hit_box_radius = 15

    def __init__(self, coord, angle, max_distance, min_distance, player_id, team_id, power, target_type):
    # initialization of the bomb
        self.speed += random.randint(0, 2) * 0.1
        Bullet.__init__(self, coord, angle, max_distance, min_distance, player_id, team_id, power, target_type)