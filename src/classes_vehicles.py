import pygame
import math
import random

from settings import *
from functions_math import *


class Vehicle:
    path = LIGHT_TANK_PATH
    v_max = 1
    acceleration = 0.1
    turn_speed = 0.04
    hit_box_radius = 13

    def __init__(self, coord, angle):
    # initialization of the vehicle
        self.coord = coord
        self.angle = angle
        
        self.v_current = 0
        self.movement_target = coord

        self.body = pygame.image.load(os.path.join(*self.path))
        self.body.convert()
        self.body.set_colorkey(BLACK)
        # print(self.body.get_at((0,10)))
        # self.rotated_image = pygame.transform.rotate(self.body, -math.degrees(self.angle))


    def draw(self, win, offset_x, offset_y, scale):
    # draw the vehicle on the screen
        
        body = self.body.get_rect()
        scaled_image = pygame.transform.scale(self.body, (scale*body.width, scale*body.height))
        rotated_image = pygame.transform.rotate(scaled_image, -math.degrees(self.angle))
        new_rect = rotated_image.get_rect(center = world2screen(self.coord, offset_x, offset_y, scale))
        win.blit(rotated_image, new_rect.topleft)
        # win.blit(scaled_image, move_point(self.orgin, offset_x, offset_y, scale))


    def draw_extra_data(self, win, offset_x, offset_y, scale):
    # draw extra data about the vehicle on the screen
        
        # target
        pygame.draw.line(win, BLUE, world2screen(self.coord, offset_x, offset_y, scale), world2screen(self.movement_target, offset_x, offset_y, scale))
        pygame.draw.circle(win, BLUE, world2screen(self.movement_target, offset_x, offset_y, scale), 10*scale, 1)

        # hit box radius
        pygame.draw.circle(win, RED, world2screen(self.coord, offset_x, offset_y, scale), self.hit_box_radius*scale, 1)


    def run(self, Map):
    # life-cycle of the vehicle
        self.accelerate()
        self.turn_to_target()
        self.move()

        x_id, y_id = Map.world2id(self.coord)
        Map.BOARD[y_id][x_id].degrade(1)

    def accelerate(self):
    # accelerate the vehicle - calculate the current speed
        dist_to_target = dist_two_points(self.coord,self.movement_target)

        if dist_to_target > 20:
            self.v_current += self.acceleration
            if self.v_current > self.v_max: self.v_current = self.v_max
        else: 
            self.v_current -= self.acceleration
            if self.v_current < 0: self.v_current = 0

    def turn_to_target(self):
    # change vehicle's angle to target the movement target
        dist_to_target = dist_two_points(self.coord,self.movement_target)

        if dist_to_target > 20:
            target_angle = math.atan2(self.movement_target[1] - self.coord[1], self.movement_target[0] - self.coord[0])
            if target_angle < 0: target_angle += 2*math.pi

            if abs(target_angle - self.angle) > 0.05:
                if self.angle > target_angle:
                    self.angle -= self.turn_speed
                else:
                    self.angle += self.turn_speed

                if self.angle > 2*math.pi: self.angle -= 2*math.pi
                elif self.angle < 0: self.angle += 2*math.pi

                # print(str(self.angle) + "\t" + str(target_angle))

    def move(self):
    # move the vehicle forward
        self.coord = move_point(self.coord, self.v_current, self.angle)

    
    def get_position(self):
    # return coordinates
        return self.coord

    def get_angle(self):
    # return angle
        return self.angle