import pygame
import math
import random

from settings import *
from functions_math import *


class Bullet:
    speed = 10
    radius = 3
    hit_box_radius = 3

    def __init__(self, coord, angle, max_distance, min_distance, player_id, team_id, power):
    # initialization of the bullet
        self.is_alive = True

        self.coord = coord
        self.angle = angle
        self.player_id = player_id
        self.team_id = team_id
        self.power = power

        self.distance = 0
        self.max_distance = max_distance
        self.min_distance = min_distance


    def draw(self, win, offset_x, offset_y, scale):
    # draw the bullet on the screen
        pygame.draw.circle(win, YELLOW, world2screen(self.coord, offset_x, offset_y, scale), self.radius*scale, 0)


    def run(self, map, list_of_units):
    # life-cycle of the bullet 
     
        for unit in list_of_units:
            if self.is_hit(unit):
                unit.get_hit(self.power)
                self.is_alive = False    

        if self.distance > self.max_distance:
            x_id, y_id = map.world2id(self.coord)
            map.BOARD[y_id][x_id].degrade(2)
            self.is_alive = False
        
        if self.is_alive:
            self.move()


    def move(self):
    # move the bullet forward
        self.distance += self.speed
        self.coord = move_point(self.coord, self.speed, self.angle)

    
    def is_hit(self, object):
    # function checks if the object is hit
    # return True if yes
        if object.is_alive and object.team_id != self.team_id and self.distance > self.min_distance:
            if dist_two_points(self.coord, object.coord) < object.hit_box_radius + self.hit_box_radius:
                return True
        
        return False