import pygame
import math
import random

from settings import *
from functions_math import *
from classes_base import *


class Vehicle(Base_animated_object):
    path = TANK_PATH
    number_of_frames = TANK_FRAMES
    number_of_frames_in_sequence = TANK_FRAMES - 1

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
        self.movement_target = []

        # self.body = pygame.image.load(os.path.join(*self.path))
        # self.body.convert()
        # self.body.set_colorkey(BLACK)


    # def draw(self, win, offset_x, offset_y, scale):
    # # draw the vehicle on the screen
        
    #     body = self.body.get_rect()
    #     scaled_image = pygame.transform.scale(self.body, (scale*body.width, scale*body.height))
    #     rotated_image = pygame.transform.rotate(scaled_image, -math.degrees(self.angle))
    #     new_rect = rotated_image.get_rect(center = world2screen(self.coord, offset_x, offset_y, scale))
    #     win.blit(rotated_image, new_rect.topleft)
    #     # win.blit(scaled_image, move_point(self.orgin, offset_x, offset_y, scale))


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
        if not self.is_collision(list_with_units, new_coord):
            self.coord = new_coord
            self.angle = new_angle
        else:
            self.angle += self.turn_speed

        x_id, y_id = map.world2id(self.coord)
        map.BOARD[y_id][x_id].degrade(1)


    def accelerate(self):
    # accelerate the vehicle - calculate the current speed
        
        self.state = "move"
        self.v_current += self.acceleration
        if self.v_current > self.v_max: self.v_current = self.v_max


    def decelerate(self):
    # decelerate the vehicle - calculate the current speed
        
        self.v_current -= self.acceleration
        if self.v_current < 0: 
            self.v_current = 0
            self.state = "stop"


    # def turn_to_target(self):
    # # change vehicle's angle to target the movement target
    #     dist_to_target = dist_two_points(self.coord, self.movement_target[0])

    #     if dist_to_target > 20:
    #         target_angle = angle_to_target(self.coord, self.movement_target[0])
    #         self.angle = turn_to_target_angle(self.angle, target_angle, self.turn_speed)


    def get_new_angle(self):
    # return new angle closer to the movement target
        target_angle = angle_to_target(self.coord, self.movement_target[0])
        return turn_to_target_angle(self.angle, target_angle, self.turn_speed)


    def is_collision(self, list_with_units, coord):
    # return True if collision with other object occurs
        for unit in list_with_units:
            dist = dist_two_points(coord, unit.coord)
            if dist < self.hit_box_radius + unit.hit_box_radius and dist > 5: # dist > 5 is to avoid a collision with yourself
                return True
        return False


    # def move(self, list_with_units):
    # # move the vehicle forward, if it is possible
    #     new_coord = move_point(self.coord, self.v_current, self.angle)
    #     if not self.is_collision(list_with_units, new_coord):
    #         self.coord = new_coord
    #     else:
    #         self.angle += self.turn_speed # ------------------------------------------- :( this does'n work
   


    # def get_position(self):
    # # return coordinates
    #     return self.coord

    # def get_angle(self):
    # # return angle
    #     return self.angle


class Light_track(Vehicle):
    path = LIGHT_TRACK_PATH
    number_of_frames = LIGHT_TRACK_FRAMES
    number_of_frames_in_sequence = LIGHT_TRACK_FRAMES - 1

    v_max = 1
    acceleration = 0.1
    turn_speed = 0.04

    hit_box_radius = 13
    base_HP = 100

    # def __init__(self, coord, angle, player_id, team_id):
    # # initialization of the light track
    #     Vehicle.__init__(self, coord, angle, player_id, team_id)


class Medium_track(Vehicle):
    path = MEDIUM_TRACK_PATH
    number_of_frames = MEDIUM_TRACK_FRAMES
    number_of_frames_in_sequence = MEDIUM_TRACK_FRAMES - 1

    v_max = 0.75
    acceleration = 0.1
    turn_speed = 0.04

    hit_box_radius = 17
    base_HP = 200

    # def __init__(self, coord, angle, player_id, team_id):
    # # initialization of the medium track
    #     Vehicle.__init__(self, coord, angle, player_id, team_id)


class Ant(Vehicle):
    path = ANT_PATH
    number_of_frames = ANT_FRAMES
    number_of_frames_in_sequence = ANT_FRAMES - 1

    v_max = 1
    acceleration = 0.2
    turn_speed = 0.04

    hit_box_radius = 13
    base_HP = 50