import pygame
import math
import random

from settings import *
from functions_math import *

class Turret:
    path = LIGHT_TURRET_PATH
    # v_max = 1
    # acceleration = 0.1
    # turn_speed = 0.04
    radar_radius = 200

    def __init__(self, coord, base_angle):
    # initialization of the weapon
        self.coord = coord
        self.base_angle = base_angle
        self.turret_angle = 0
        
        # self.v_current = 0
        # self.movement_target = coord

        self.body = pygame.image.load(os.path.join(*self.path))
        self.body.convert()
        self.body.set_colorkey(BLACK)


    def draw(self, win, offset_x, offset_y, scale):
    # draw the weapon on the screen
        
        body = self.body.get_rect()
        scaled_image = pygame.transform.scale(self.body, (scale*body.width, scale*body.height))
        rotated_image = pygame.transform.rotate(scaled_image, -math.degrees(self.base_angle + self.turret_angle))
        new_rect = rotated_image.get_rect(center = world2screen(self.coord, offset_x, offset_y, scale))
        win.blit(rotated_image, new_rect.topleft)
        # win.blit(scaled_image, move_point(self.orgin, offset_x, offset_y, scale))


    def draw_extra_data(self, win, offset_x, offset_y, scale):
    # draw extra data about the weapon on the screen
        
        # target
        # pygame.draw.line(win, BLUE, world2screen(self.coord, offset_x, offset_y, scale), world2screen(self.movement_target, offset_x, offset_y, scale))
        # pygame.draw.circle(win, BLUE, world2screen(self.movement_target, offset_x, offset_y, scale), 10*scale, 1)

        # radar radius
        pygame.draw.circle(win, YELLOW, world2screen(self.coord, offset_x, offset_y, scale), self.radar_radius*scale, 1)


    def run(self):
    # life-cycle of the weapon
        pass

    def set_position(self, coord):
    # set new position of weapon
        self.coord = coord

    def set_angle(self, angle):
    # set new base angle of weapon
        self.base_angle = angle