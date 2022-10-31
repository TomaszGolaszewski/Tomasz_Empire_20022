import pygame
import math
import random

from settings import *
from functions_math import *


class Bullet:
    speed = 5
    radius = 3

    def __init__(self, coord, angle, max_distance, min_distance, player_id, team_id):
    # initialization of the bullet
        self.coord = coord
        self.angle = angle
        self.player_id = player_id
        self.team_id = team_id

        self.distance = 0
        self.max_distance = max_distance
        self.min_distance = min_distance


    def draw(self, win, offset_x, offset_y, scale):
    # draw the bullet on the screen
        pygame.draw.circle(win, YELLOW, world2screen(self.coord, offset_x, offset_y, scale), self.radius*scale, 0)


    def run(self, map):
    # life-cycle of the bullet
        if self.distance <= self.max_distance: self.move()

        if self.distance > self.max_distance:
            x_id, y_id = map.world2id(self.coord)
            map.BOARD[y_id][x_id].degrade(2)


    def move(self):
    # move the bullet forward
        self.distance += self.speed
        self.coord = move_point(self.coord, self.speed, self.angle)