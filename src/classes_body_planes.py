import pygame
import math
import random

# from settings import *
from setup import *
from functions_math import *
from classes_body_vehicles import *


class Plane(Vehicle):
    path = PLANE_PATH
    number_of_frames = PLANE_FRAMES
    min_scale_to_be_visible = 0.5

    v_max = 4
    acceleration = 0.1
    turn_speed = 0.03

    hit_box_radius = 11
    base_HP = 100
    base_fuel = FRAMERATE * 100

    def __init__(self, id, coord, angle, player_id, team_id, factory_id=0):
    # initialization of the Plane
        Vehicle.__init__(self, id, coord, angle, player_id, team_id, factory_id)
        self.fuel = self.base_fuel
        self.airport = coord

    def draw_extra_data(self, win, offset_x, offset_y, scale):
    # draw extra data about the Plane on the screen
        Vehicle.draw_extra_data(self, win, offset_x, offset_y, scale)
        # draw line to airport
        pygame.draw.line(win, YELLOW, world2screen(self.coord, offset_x, offset_y, scale), world2screen(self.airport, offset_x, offset_y, scale))
        pygame.draw.circle(win, YELLOW, world2screen(self.airport, offset_x, offset_y, scale), 10*scale, 1)
        
    def draw_movement_target(self, win, offset_x, offset_y, scale):
    # draw extra data about the Plane movement target
        Vehicle.draw_movement_target(self, win, offset_x, offset_y, scale)
        # draw line to airport if fuel level is low
        if self.fuel < 0.5 * self.base_fuel:
            pygame.draw.line(win, YELLOW, world2screen(self.coord, offset_x, offset_y, scale), world2screen(self.airport, offset_x, offset_y, scale))
            pygame.draw.circle(win, YELLOW, world2screen(self.airport, offset_x, offset_y, scale), 10*scale, 1)

    def run(self, map, dict_with_units):
    # life-cycle of the Plane
        if self.fuel > 0.5 * self.base_fuel:
            if len(self.movement_target):
                dist_to_target = dist_two_points(self.coord, self.movement_target[0]) # TODO: check movement target mechanics
                self.accelerate()
                self.angle = self.get_new_angle()
                self.coord = move_point(self.coord, self.v_current, self.angle)

                if dist_to_target < 20 and len(self.movement_target) >= 2:
                    self.movement_target.pop(0) # remove the achieved target
        else:
            self.accelerate()
            target_angle = angle_to_target(self.coord, self.airport)
            self.angle = turn_to_target_angle(self.angle, target_angle, self.turn_speed)
            self.coord = move_point(self.coord, self.v_current, self.angle)

        if self.v_current < 1.5: # self.v_max:
            map.degrade(self.coord, 1)

    def run_after_death(self):
    # life-cycle of the vehicle after death
        self.coord = move_point(self.coord, self.v_current, self.angle)


class Plane_bomber(Plane):
    path = BOMBER_PATH
    number_of_frames = BOMBER_FRAMES
    min_scale_to_be_visible = 0.5

    v_max = 3
    acceleration = 0.1
    turn_speed = 0.02

    hit_box_radius = 15
    base_HP = 100


class Plane_strategic_bomber(Plane):
    path = STRATEGIC_BOMBER_PATH
    number_of_frames = STRATEGIC_BOMBER_FRAMES
    min_scale_to_be_visible = 0.5

    v_max = 2
    acceleration = 0.05
    turn_speed = 0.01

    hit_box_radius = 20
    base_HP = 300

