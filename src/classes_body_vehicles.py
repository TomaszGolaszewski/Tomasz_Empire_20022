import pygame
import math
import random

# from settings import *
from setup import *
from functions_math import *
from classes_base import *


class Vehicle(Base_animated_object):
    path = LIGHT_TRACK_PATH
    number_of_frames = LIGHT_TRACK_FRAMES
    min_scale_to_be_visible = 0.125

    v_max = 1
    acceleration = 0.1
    turn_speed = 0.04

    hit_box_radius = 13
    base_HP = 100

    def __init__(self, coord, angle, player_id, team_id):
    # initialization of the vehicle
        Base_animated_object.__init__(self, coord, angle)

        self.player_id = player_id
        self.team_id = team_id
        
        self.v_current = 0
        self.v_max_squad = self.v_max
        self.movement_target = []

        if self.frame_height > self.frame_width: self.body_radius = self.frame_height // 2
        else: self.body_radius = self.frame_width // 2


    def draw_extra_data(self, win, offset_x, offset_y, scale):
    # draw extra data about the vehicle on the screen
        
        # target
        if len(self.movement_target):
            last_target = self.coord
            for target in self.movement_target:
                pygame.draw.line(win, BLUE, world2screen(last_target, offset_x, offset_y, scale), world2screen(target, offset_x, offset_y, scale))
                pygame.draw.circle(win, BLUE, world2screen(target, offset_x, offset_y, scale), 10*scale, 1)
                last_target = target

        # hit box radius
        pygame.draw.circle(win, RED, world2screen(self.coord, offset_x, offset_y, scale), self.hit_box_radius*scale, 1)
        # body radius
        pygame.draw.circle(win, RED, world2screen(self.coord, offset_x, offset_y, scale), self.body_radius*scale, 1)


    def run(self, map, list_with_units):
    # life-cycle of the vehicle
        if len(self.movement_target):
            dist_to_target = dist_two_points(self.coord, self.movement_target[0])

            if dist_to_target > 20:
                self.accelerate()
                # self.turn_to_target()
                new_angle = self.get_new_angle()
            else:
                self.decelerate()
                new_angle = self.angle
                self.movement_target.pop(0) # remove the achieved target

        else:
            self.decelerate()
            new_angle = self.angle

        # self.move(list_with_units)
        new_coord = move_point(self.coord, self.v_current, new_angle)
        if not self.is_obstacle(map, new_coord) and not self.is_collision(list_with_units, new_coord):
            self.coord = new_coord
            self.angle = new_angle
        else:
            self.angle += self.turn_speed

        map.degrade(self.coord, 1)

    def run_after_death(self):
    # life-cycle of the vehicle after death
        pass

    def accelerate(self):
    # accelerate the vehicle - calculate the current speed     
        self.state = "move"
        self.v_current += self.acceleration
        if self.v_current > self.v_max_squad: self.v_current = self.v_max_squad

    def decelerate(self):
    # decelerate the vehicle - calculate the current speed       
        self.v_current -= self.acceleration
        if self.v_current < 0: 
            self.v_current = 0
            self.state = "stop"

    def get_new_angle(self):
    # return new angle closer to the movement target
        target_angle = angle_to_target(self.coord, self.movement_target[0])
        return turn_to_target_angle(self.angle, target_angle, self.turn_speed)

    def is_collision(self, list_with_units, coord):
    # return True if collision with other object occurs
        for unit in list_with_units:
            if unit.is_alive and (unit.unit_type == "land" or unit.unit_type == "navy" or unit.unit_type == "building"):
            # 1. first idea - using the standard square root
                # dist = dist_two_points(coord, unit.coord)
                # if dist < self.hit_box_radius + unit.hit_box_radius and dist > 5: # dist > 5 is to avoid a collision with yourself
                #     return True

            # 2. second idea - measurement using taxicab geometry
                # hit_distance = self.hit_box_radius + unit.hit_box_radius
                # # first check distance in taxicab geometry - is faster
                # dist_in_taxicab_geometry = abs(coord[0] - unit.coord[0]) + abs(coord[1] - unit.coord[1])
                # if dist_in_taxicab_geometry < 1.5 * hit_distance and dist_in_taxicab_geometry > 5: # dist > 5 is to avoid a collision with yourself
                #     # dist = dist_two_points(coord, unit.coord)
                #     dist = math.sqrt((coord[0]-unit.coord[0])**2 + (coord[1]-unit.coord[1])**2)
                #     if dist < hit_distance:
                #         return True

            # 3. third idea - don't use square root and compare in second power
                # dist2 = (coord[0]-unit.coord[0])**2 + (coord[1]-unit.coord[1])**2
                # dist2 = (coord[0]-unit.coord[0])*(coord[0]-unit.coord[0]) + (coord[1]-unit.coord[1])*(coord[1]-unit.coord[1])
                # if dist2 < (self.hit_box_radius + unit.hit_box_radius)*(self.hit_box_radius + unit.hit_box_radius) and dist2 > 25: # dist > 5 is to avoid a collision with yourself
                #     return True

            # 4. both and don't waste time for calling functions
                # hit_distance = self.hit_box_radius + unit.hit_box_radius
                # # first check distance in taxicab geometry - is faster
                # dist_in_taxicab_geometry = abs(coord[0] - unit.coord[0]) + abs(coord[1] - unit.coord[1])
                # if dist_in_taxicab_geometry < 1.5 * hit_distance and dist_in_taxicab_geometry > 5: # dist > 5 is to avoid a collision with yourself
                #     dist2 = (coord[0]-unit.coord[0])*(coord[0]-unit.coord[0]) + (coord[1]-unit.coord[1])*(coord[1]-unit.coord[1])
                #     if dist2 < (self.hit_box_radius + unit.hit_box_radius)*(self.hit_box_radius + unit.hit_box_radius):
                #         return True

            # 5. try hypot function (method returns the Euclidean norm)
                # dist = math.hypot(coord[0]-unit.coord[0], coord[1]-unit.coord[1])
                # if dist < self.hit_box_radius + unit.hit_box_radius and dist > 5: # dist > 5 is to avoid a collision with yourself
                #     return True

            # 6. try all
                hit_distance = self.hit_box_radius + unit.hit_box_radius
                # first check distance in taxicab geometry - is faster
                dist_in_taxicab_geometry = abs(coord[0] - unit.coord[0]) + abs(coord[1] - unit.coord[1])
                if dist_in_taxicab_geometry < 1.5 * hit_distance and dist_in_taxicab_geometry > 5: # dist > 5 is to avoid a collision with yourself
                    dist = math.hypot(coord[0]-unit.coord[0], coord[1]-unit.coord[1])
                    if dist < hit_distance:
                        return True
        return False

    def is_obstacle(self, map, coord):
    # return True if collision with map occurs
        if map.get_tile_type(coord) == "water": return True
        else: return False


class Light_track(Vehicle):
    path = LIGHT_TRACK_PATH
    number_of_frames = LIGHT_TRACK_FRAMES
    min_scale_to_be_visible = 1

    v_max = 1
    acceleration = 0.1
    turn_speed = 0.04

    hit_box_radius = 13
    base_HP = 100


class Medium_track(Vehicle):
    path = MEDIUM_TRACK_PATH
    number_of_frames = MEDIUM_TRACK_FRAMES
    min_scale_to_be_visible = 0.5

    v_max = 0.75
    acceleration = 0.1
    turn_speed = 0.02

    hit_box_radius = 17
    base_HP = 200


class Heavy_track(Vehicle):
    path = HEAVY_TRACK_PATH
    number_of_frames = HEAVY_TRACK_FRAMES
    min_scale_to_be_visible = 0.5

    v_max = 0.5
    acceleration = 0.1
    turn_speed = 0.01

    hit_box_radius = 22
    base_HP = 500

class Heavy_track_basic(Heavy_track):
    path = HEAVY_TRACK_BASIC_PATH
    number_of_frames = HEAVY_TRACK_BASIC_FRAMES
    min_scale_to_be_visible = 0.5


class Ant(Vehicle):
    path = ANT_PATH
    number_of_frames = ANT_FRAMES
    min_scale_to_be_visible = 1

    v_max = 1
    acceleration = 0.2
    turn_speed = 0.04

    hit_box_radius = 10
    base_HP = 50
