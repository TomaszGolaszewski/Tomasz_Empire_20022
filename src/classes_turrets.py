import pygame
import math
import random
from classes_bullets import Bullet

from settings import *
from functions_math import *

class Turret:
    path = TURRET_PATH
    
    turn_speed = 0.04
    max_radar_radius = 200
    min_radar_radius = 50

    max_bullet_range = 400
    barrel_length = 10

    power = 100

    countdown_time_to_search = FRAMERATE // 6
    countdown_time_to_shot = FRAMERATE

    def __init__(self, coord, base_angle, player_id, team_id):
    # initialization of the weapon
        self.coord = coord
        self.base_angle = base_angle
        self.turret_angle = base_angle
        self.player_id = player_id
        self.team_id = team_id
        
        self.target_coord = coord
        self.angle_to_target = base_angle
        self.dist_to_target = 0
        self.countdown_to_search = 0
        self.countdown_to_shot = 0
        self.target_locked = False
        # self.show_target = False

        self.body = pygame.image.load(os.path.join(*self.path))
        self.body.convert()
        self.body.set_colorkey(BLACK)


    def draw(self, win, offset_x, offset_y, scale):
    # draw the weapon on the screen
        
        body = self.body.get_rect()
        scaled_image = pygame.transform.scale(self.body, (scale*body.width, scale*body.height))
        rotated_image = pygame.transform.rotate(scaled_image, -math.degrees(self.turret_angle))
        new_rect = rotated_image.get_rect(center = world2screen(self.coord, offset_x, offset_y, scale))
        win.blit(rotated_image, new_rect.topleft)
        # win.blit(scaled_image, move_point(self.orgin, offset_x, offset_y, scale))


    def draw_extra_data(self, win, offset_x, offset_y, scale):
    # draw extra data about the weapon on the screen
        
        # target
        if self.target_locked:
            pygame.draw.line(win, RED, world2screen(self.coord, offset_x, offset_y, scale), world2screen(self.target_coord, offset_x, offset_y, scale))
            pygame.draw.circle(win, RED, world2screen(self.target_coord, offset_x, offset_y, scale), 10*scale, 1)

        # radar radius
        pygame.draw.circle(win, YELLOW, world2screen(self.coord, offset_x, offset_y, scale), self.max_radar_radius*scale, 1)
        pygame.draw.circle(win, LIME, world2screen(self.coord, offset_x, offset_y, scale), self.min_radar_radius*scale, 1)


    def run(self, list_with_units, list_with_bullets):
    # life-cycle of the weapon
        if not self.countdown_to_search:
            # try to find target
            self.find_target(list_with_units)
            self.countdown_to_search = self.countdown_time_to_search          
        else:
            self.countdown_to_search -= 1

        if not self.countdown_to_shot:
            if self.target_locked and abs(self.turret_angle - self.angle_to_target) < 0.05:
                # make and shot the bullet
                bullet_coord = move_point(self.coord, self.barrel_length, self.turret_angle)
                list_with_bullets.append(Bullet(bullet_coord, self.turret_angle, self.max_bullet_range, self.min_radar_radius, self.player_id, self.team_id, self.power))
                self.countdown_to_shot = self.countdown_time_to_shot
        else:
            self.countdown_to_shot -= 1

        self.turret_angle = turn_to_target_angle(self.turret_angle, self.angle_to_target, self.turn_speed, 0.02)


    def find_target(self, list_with_units):
    # find closest target
    # set new target_coord, angle_to_target and dist_to target

        temp_coord = [0, 0]
        temp_angle = self.base_angle
        temp_dist = 9999
        temp_found_new_target = False
        
        for unit in list_with_units:
            if unit.team_id != self.team_id:
                dist = dist_two_points(unit.coord, self.coord)
                if dist < self.max_radar_radius and dist < temp_dist and dist > self.min_radar_radius:
                    temp_coord = unit.coord
                    temp_dist = dist
                    temp_found_new_target = True
        
        if temp_found_new_target:
            self.target_coord = temp_coord
            self.angle_to_target = angle_to_target(self.coord, temp_coord)
            self.dist_to_target = temp_dist
            self.target_locked = True
        else:
            self.target_coord = self.coord
            self.target_locked = False

    def set_position(self, coord):
    # set new position of weapon
        self.coord = coord

    def set_angle(self, angle):
    # set new base angle of weapon
        self.base_angle = angle


class Light_cannon(Turret): 
    path = LIGHT_CANNON_PATH

    turn_speed = 0.04
    max_radar_radius = 300
    min_radar_radius = 50

    max_bullet_range = 600
    barrel_length = 15

    power = 40

    countdown_time_to_search = FRAMERATE // 6
    countdown_time_to_shot = FRAMERATE

    def __init__(self, coord, base_angle, player_id, team_id):
    # initialization of the light cannon
        Turret.__init__(self, coord, base_angle, player_id, team_id)


class Medium_cannon(Turret): 
    path = MEDIUM_CANNON_PATH

    turn_speed = 0.04
    max_radar_radius = 400
    min_radar_radius = 75

    max_bullet_range = 800
    barrel_length = 25

    power = 80

    countdown_time_to_search = FRAMERATE // 6
    countdown_time_to_shot = FRAMERATE

    def __init__(self, coord, base_angle, player_id, team_id):
    # initialization of the light cannon
        Turret.__init__(self, coord, base_angle, player_id, team_id)