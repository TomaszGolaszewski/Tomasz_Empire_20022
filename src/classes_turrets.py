import pygame
import pygame.gfxdraw
import math
import random

from settings import *
# from setup import *
from functions_math import *
from classes_bullets import *
from classes_base import *


class Turret(Base_object):
    path = MINIGUN_PATH

    Ammunition_class = Bullet
    
    turn_speed = 0.04
    max_radar_radius = 200
    min_radar_radius = 50

    max_bullet_range = 400
    barrel_length = 10

    power = 100
    description = "Turret"

    countdown_time_to_search = FRAMERATE // 6
    countdown_time_to_shot = FRAMERATE

    def __init__(self, id, coord, base_angle, initial_angle, player_id, team_id):
    # initialization of the weapon    
        self.id = id           
        self.base_angle = base_angle # angle of the base of the unit     
        angle = base_angle + initial_angle
        if angle > 2*math.pi: angle -= 2*math.pi
        self.angle_to_target = angle # angle to current target
        self.initial_angle = initial_angle # initial angle of the turret
        Base_object.__init__(self, coord, angle)

        self.player_id = player_id
        self.team_id = team_id

        self.target_coord = coord
        self.dist_to_target = 0
        self.countdown_to_search = 0
        self.countdown_to_shot = 0
        self.target_locked = False


    def draw_extra_data(self, win, offset_x, offset_y, scale):
    # draw extra data about the weapon on the screen
        
        # target
        if self.target_locked:
            pygame.draw.line(win, RED, world2screen(self.coord, offset_x, offset_y, scale), 
                        world2screen(self.target_coord, offset_x, offset_y, scale))
            pygame.draw.circle(win, RED, world2screen(self.target_coord, offset_x, offset_y, scale), 10*scale, 1)

        # draw current position
        pygame.draw.line(win, YELLOW, world2screen(self.coord, offset_x, offset_y, scale), 
                        world2screen(move_point(self.coord, self.max_radar_radius, self.angle), offset_x, offset_y, scale))

        # radar radius
        pygame.draw.circle(win, YELLOW, world2screen(self.coord, offset_x, offset_y, scale), self.max_radar_radius*scale, 1)
        pygame.draw.circle(win, LIME, world2screen(self.coord, offset_x, offset_y, scale), self.min_radar_radius*scale, 1)


    def draw_range(self, win, offset_x, offset_y, scale):
    # draw extra data about the range of the weapon on the screen
        pygame.draw.circle(win, YELLOW, world2screen(self.coord, offset_x, offset_y, scale), self.max_radar_radius*scale, 1)
        pygame.draw.circle(win, LIME, world2screen(self.coord, offset_x, offset_y, scale), self.min_radar_radius*scale, 1)


    def run(self, dict_with_units, list_with_bullets):
    # life-cycle of the weapon
        if not self.countdown_to_search:
            # try to find target
            self.find_target(dict_with_units)
            self.countdown_to_search = self.countdown_time_to_search          
        else:
            self.countdown_to_search -= 1

        if not self.countdown_to_shot:
            if self.target_locked and abs(self.angle - self.angle_to_target) < 0.02:
                # make and shot the bullet
                self.make_bullets(list_with_bullets)
                self.countdown_to_shot = self.countdown_time_to_shot
        else:
            self.countdown_to_shot -= 1

        if not self.target_locked:
            self.angle_to_target = self.base_angle + self.initial_angle
            if self.angle_to_target > 2*math.pi: self.angle_to_target -= 2*math.pi

        self.angle = turn_to_target_angle(self.angle, self.angle_to_target, self.turn_speed) # , 0.02) # damping


    def find_target(self, dict_with_units):
    # find closest target
    # set new target_coord, angle_to_target and dist_to target

        temp_coord = [0, 0]
        temp_dist = 9999
        temp_found_new_target = False
        
        for unit_id in dict_with_units:
            if dict_with_units[unit_id].team_id != self.team_id and dict_with_units[unit_id].player_id and dict_with_units[unit_id].is_alive:
                # dist = dist_two_points(unit.coord, self.coord)
                dist = math.hypot(self.coord[0]-dict_with_units[unit_id].coord[0], self.coord[1]-dict_with_units[unit_id].coord[1])
                if self.is_valid_target(dict_with_units[unit_id].unit_type) \
                        and dist < self.max_radar_radius \
                        and dist < temp_dist \
                        and dist > self.min_radar_radius:
                    temp_coord = dict_with_units[unit_id].coord
                    temp_dist = dist
                    temp_target_type = dict_with_units[unit_id].unit_type
                    temp_found_new_target = True
        
        if temp_found_new_target:
            self.target_coord = temp_coord
            self.angle_to_target = angle_to_target(self.coord, temp_coord)
            self.dist_to_target = temp_dist
            self.target_type = temp_target_type
            self.target_locked = True
        else:
            self.target_coord = self.coord
            self.target_locked = False

    
    def make_bullets(self, list_with_bullets):
    # function makes and shoot the bullet
    # return list_with_bullets
        bullet_coord = move_point(self.coord, self.barrel_length, self.angle)
        list_with_bullets.append(self.Ammunition_class(bullet_coord, self.angle, self.max_bullet_range, self.min_radar_radius, self.player_id, self.team_id, self.power, self.target_type))            
        return list_with_bullets

    
    def is_valid_target(self, unit_type):
    # checks (by unit type) if the target can be targeted
    # return True if target is valid
        return True


    def set_angle(self, angle):
    # set new base angle of weapon
        self.base_angle = angle


# ======================================================================
# Tanks' turrets


class Light_cannon(Turret): 
    path = LIGHT_CANNON_PATH

    Ammunition_class = Plasma

    turn_speed = 0.08
    max_radar_radius = 300
    min_radar_radius = 50

    max_bullet_range = 600
    barrel_length = 15

    power = 40
    description = "Cannon: 40dps (40p1s)"

    countdown_time_to_search = FRAMERATE // 6
    countdown_time_to_shot = FRAMERATE

    def is_valid_target(self, unit_type):
    # checks (by unit type) if the target can be targeted
    # return True if target is valid
        # anti land units
        if unit_type == "land" or unit_type == "navy" or unit_type == "building": return True
        else: return False


class Medium_cannon(Turret): 
    path = MEDIUM_CANNON_PATH

    Ammunition_class = Plasma

    turn_speed = 0.04
    max_radar_radius = 400
    min_radar_radius = 75

    max_bullet_range = 800
    barrel_length = 25

    power = 80
    description = "Cannon: 80dps (80p1s)"

    countdown_time_to_search = FRAMERATE // 6
    countdown_time_to_shot = FRAMERATE

    def is_valid_target(self, unit_type):
    # checks (by unit type) if the target can be targeted
    # return True if target is valid
        # anti land units
        if unit_type == "land" or unit_type == "navy" or unit_type == "building": return True
        else: return False

class Heavy_cannon(Turret): 
    path = HEAVY_CANNON_PATH

    Ammunition_class = Plasma

    turn_speed = 0.02
    max_radar_radius = 700
    min_radar_radius = 100

    max_bullet_range = 1000
    barrel_length = 30

    power = 150
    description = "Cannon: 75dps (150p2s)"

    countdown_time_to_search = FRAMERATE // 6
    countdown_time_to_shot = FRAMERATE * 2

    def is_valid_target(self, unit_type):
    # checks (by unit type) if the target can be targeted
    # return True if target is valid
        # anti land units
        if unit_type == "land" or unit_type == "navy" or unit_type == "building": return True
        else: return False


# ======================================================================
# Side cannons


class Side_cannon(Turret): 
    path = SIDE_CANNON_PATH

    Ammunition_class = Plasma

    turn_speed = 0.04
    max_radar_radius = 500
    min_radar_radius = 75

    max_bullet_range = 800
    barrel_length = 25

    power = 80
    description = "SideCannon: 80dps (80p1s)"

    countdown_time_to_search = FRAMERATE // 6
    countdown_time_to_shot = FRAMERATE

    turn_limit = math.pi / 4

    def draw_extra_data(self, win, offset_x, offset_y, scale):
    # draw extra data about the weapon on the screen
        
        # target
        if self.target_locked:
            pygame.draw.line(win, RED, world2screen(self.coord, offset_x, offset_y, scale), 
                        world2screen(self.target_coord, offset_x, offset_y, scale))
            pygame.draw.circle(win, RED, world2screen(self.target_coord, offset_x, offset_y, scale), 10*scale, 1)

        # draw current position
        pygame.draw.line(win, YELLOW, world2screen(self.coord, offset_x, offset_y, scale), 
                        world2screen(move_point(self.coord, self.max_radar_radius, self.angle), offset_x, offset_y, scale))

        # radar radius
        coord_x, coord_y = world2screen(self.coord, offset_x, offset_y, scale)
        pygame.gfxdraw.arc(win, int(coord_x), int(coord_y), 
                           int(self.max_radar_radius*scale), 
                           int(math.degrees(self.base_angle + self.initial_angle - self.turn_limit)), 
                           int(math.degrees(self.base_angle + self.initial_angle + self.turn_limit)),
                           YELLOW) # pygame.gfxdraw.pie
        pygame.gfxdraw.arc(win, int(coord_x), int(coord_y), 
                           int(self.min_radar_radius*scale), 
                           int(math.degrees(self.base_angle + self.initial_angle - self.turn_limit)), 
                           int(math.degrees(self.base_angle + self.initial_angle + self.turn_limit)),
                           LIME)

    def draw_range(self, win, offset_x, offset_y, scale):
    # draw extra data about the range of the weapon on the screen
        coord_x, coord_y = world2screen(self.coord, offset_x, offset_y, scale)
        pygame.gfxdraw.pie(win, int(coord_x), int(coord_y), 
                           int(self.max_radar_radius*scale), 
                           int(math.degrees(self.base_angle + self.initial_angle - self.turn_limit)), 
                           int(math.degrees(self.base_angle + self.initial_angle + self.turn_limit)),
                           YELLOW)
        pygame.gfxdraw.arc(win, int(coord_x), int(coord_y), 
                           int(self.min_radar_radius*scale), 
                           int(math.degrees(self.base_angle + self.initial_angle - self.turn_limit)), 
                           int(math.degrees(self.base_angle + self.initial_angle + self.turn_limit)),
                           LIME)

    def find_target(self, dict_with_units):
    # find closest target - difference that movement is limited
    # set new target_coord, angle_to_target and dist_to target

        temp_coord = [0, 0]
        temp_dist = 9999
        temp_found_new_target = False
        temp_angle_to_target = 0

        current_initial_angle = self.base_angle + self.initial_angle
        if current_initial_angle > 2*math.pi: current_initial_angle -= 2*math.pi
        
        for unit_id in dict_with_units:
            if dict_with_units[unit_id].team_id != self.team_id and dict_with_units[unit_id].player_id and dict_with_units[unit_id].is_alive:
                # dist = dist_two_points(unit.coord, self.coord)
                dist = math.hypot(self.coord[0]-dict_with_units[unit_id].coord[0], self.coord[1]-dict_with_units[unit_id].coord[1])
                angle = angle_to_target(self.coord, dict_with_units[unit_id].coord)
                if self.is_valid_target(dict_with_units[unit_id].unit_type) \
                        and dist < self.max_radar_radius \
                        and dist < temp_dist \
                        and dist > self.min_radar_radius \
                        and dist_two_angles(angle, current_initial_angle) < self.turn_limit:
                    # print(str(angle) + "\t" + str(current_initial_angle) + "\t" + str(dist_two_angles(angle, current_initial_angle)))
                    temp_coord = dict_with_units[unit_id].coord
                    temp_angle_to_target = angle
                    temp_dist = dist
                    temp_target_type = dict_with_units[unit_id].unit_type
                    temp_found_new_target = True
        
        if temp_found_new_target:
            self.target_coord = temp_coord
            self.angle_to_target = temp_angle_to_target
            self.dist_to_target = temp_dist
            self.target_type = temp_target_type
            self.target_locked = True
        else:
            self.target_coord = self.coord
            self.target_locked = False

    def is_valid_target(self, unit_type):
    # checks (by unit type) if the target can be targeted
    # return True if target is valid
        # anti land units
        if unit_type == "land" or unit_type == "navy" or unit_type == "building": return True
        else: return False


class Medium_naval_cannon(Side_cannon): 
    path = MEDIUM_NAVAL_CANNON_PATH

    Ammunition_class = Plasma

    turn_speed = 0.02
    max_radar_radius = 700
    min_radar_radius = 100

    max_bullet_range = 1000
    barrel_length = 32

    power = 150
    description = "Naval: 150dps (2x150p2s)"

    countdown_time_to_search = FRAMERATE // 6
    countdown_time_to_shot = FRAMERATE * 2

    turn_limit = math.pi / 2

    def make_bullets(self, list_with_bullets):
    # function makes and shoot the bullet
    # return list_with_bullets
        barrel_width = 4
        bullet_coord1 = move_point_by_vector(self.coord, (self.barrel_length, barrel_width), self.angle)
        bullet_coord2 = move_point_by_vector(self.coord, (self.barrel_length, -barrel_width), self.angle)     
        list_with_bullets.append(self.Ammunition_class(bullet_coord1, self.angle, self.max_bullet_range, self.min_radar_radius, self.player_id, self.team_id, self.power, self.target_type)) 
        list_with_bullets.append(self.Ammunition_class(bullet_coord2, self.angle, self.max_bullet_range, self.min_radar_radius, self.player_id, self.team_id, self.power, self.target_type))
        return list_with_bullets

    def is_valid_target(self, unit_type):
    # checks (by unit type) if the target can be targeted
    # return True if target is valid
        # anti land units
        if unit_type == "land" or unit_type == "navy" or unit_type == "building": return True
        else: return False


class Heavy_naval_cannon(Side_cannon): 
    path = HEAVY_NAVAL_CANNON_PATH

    Ammunition_class = Plasma

    turn_speed = 0.02
    max_radar_radius = 1100
    min_radar_radius = 200

    max_bullet_range = 1500
    barrel_length = 42

    power = 250
    description = "Naval: 250dps (3x250p3s)"

    countdown_time_to_search = FRAMERATE // 6
    countdown_time_to_shot = FRAMERATE * 3

    turn_limit = math.pi / 2

    def make_bullets(self, list_with_bullets):
    # function makes and shoot the bullet
    # return list_with_bullets
        barrel_width = 9
        bullet_coord1 = move_point_by_vector(self.coord, (self.barrel_length, barrel_width), self.angle)
        bullet_coord2 = move_point(self.coord, self.barrel_length, self.angle)
        bullet_coord3 = move_point_by_vector(self.coord, (self.barrel_length, -barrel_width), self.angle)    
        list_with_bullets.append(self.Ammunition_class(bullet_coord1, self.angle, self.max_bullet_range, self.min_radar_radius, self.player_id, self.team_id, self.power, self.target_type))
        list_with_bullets.append(self.Ammunition_class(bullet_coord2, self.angle, self.max_bullet_range, self.min_radar_radius, self.player_id, self.team_id, self.power, self.target_type))
        list_with_bullets.append(self.Ammunition_class(bullet_coord3, self.angle, self.max_bullet_range, self.min_radar_radius, self.player_id, self.team_id, self.power, self.target_type))            
        return list_with_bullets

    def is_valid_target(self, unit_type):
    # checks (by unit type) if the target can be targeted
    # return True if target is valid
        # anti land units
        if unit_type == "land" or unit_type == "navy" or unit_type == "building": return True
        else: return False


# ======================================================================
# Space marines

class Space_marine_top(Side_cannon): 
    path = SPACE_MARINE_TOP_PATH

    Ammunition_class = Plasma

    turn_speed = 0.08
    max_radar_radius = 300
    min_radar_radius = 50

    max_bullet_range = 600
    barrel_length = 12

    power = 5
    description = "Minigun: 50dps (5x10/s)"

    countdown_time_to_search = FRAMERATE // 6
    countdown_time_to_shot = FRAMERATE // 10

    turn_limit = math.pi / 2

    def make_bullets(self, list_with_bullets):
    # function makes and shoot the bullet
    # return list_with_bullets
        barrel_width = 6
        bullet_coord = move_point_by_vector(self.coord, (self.barrel_length, barrel_width), self.angle)  
        list_with_bullets.append(self.Ammunition_class(bullet_coord, self.angle, self.max_bullet_range, self.min_radar_radius, self.player_id, self.team_id, self.power, self.target_type))         
        return list_with_bullets

    # minigun is for all targets
    def is_valid_target(self, unit_type):
    # checks (by unit type) if the target can be targeted
    # return True if target is valid
        return True
    
class Super_space_marine_top(Side_cannon): 
    path = SUPER_SPACE_MARINE_TOP_PATH

    Ammunition_class = Plasma

    turn_speed = 0.08
    max_radar_radius = 400
    min_radar_radius = 50

    max_bullet_range = 600
    barrel_length = 16

    power = 10
    description = "Minigun: 150dps (10x15/s)"

    countdown_time_to_search = FRAMERATE // 6
    countdown_time_to_shot = FRAMERATE // 15

    turn_limit = math.pi / 2

    def make_bullets(self, list_with_bullets):
    # function makes and shoot the bullet
    # return list_with_bullets
        barrel_width = 7
        bullet_coord = move_point_by_vector(self.coord, (self.barrel_length, barrel_width), self.angle)  
        list_with_bullets.append(self.Ammunition_class(bullet_coord, self.angle, self.max_bullet_range, self.min_radar_radius, self.player_id, self.team_id, self.power, self.target_type))         
        return list_with_bullets

    # minigun is for all targets
    def is_valid_target(self, unit_type):
    # checks (by unit type) if the target can be targeted
    # return True if target is valid
        return True
    
class Commander_top(Super_space_marine_top): 
    path = COMMANDER_TOP_PATH
    
# ======================================================================
# Miniguns


class Minigun(Turret): 
    path = MINIGUN_PATH

    Ammunition_class = Plasma

    turn_speed = 0.08
    max_radar_radius = 400
    min_radar_radius = 50

    max_bullet_range = 600
    barrel_length = 15

    power = 10
    description = "Minigun: 150dps (10x15/s)"

    countdown_time_to_search = FRAMERATE // 6
    countdown_time_to_shot = FRAMERATE // 15

    # minigun is for all targets
    def is_valid_target(self, unit_type):
    # checks (by unit type) if the target can be targeted
    # return True if target is valid
        return True


class Plane_minigun(Turret): 
    path = PLANE_MINIGUN_PATH

    Ammunition_class = Plasma

    turn_speed = 0.08
    max_radar_radius = 400
    min_radar_radius = 50

    max_bullet_range = 600
    barrel_length = 15

    power = 10
    description = "Minigun: 100dps (10x10/s)"

    countdown_time_to_search = FRAMERATE // 6
    countdown_time_to_shot = FRAMERATE // 10

    def is_valid_target(self, unit_type):
    # checks (by unit type) if the target can be targeted
    # return True if target is valid
        # anti-aircrafts
        if unit_type == "air": return True
        else: return False


# ======================================================================
# Plane gun


class Plane_fixed_gun(Turret):
    Ammunition_class = Plasma

    turn_speed = 0.2
    max_radar_radius = 400
    min_radar_radius = 100
    search_radius = 10 # 50

    max_bullet_range = 600
    barrel_length = 15

    power = 20
    description = "Minigun: 400dps (20x20/s)"

    countdown_time_to_search = 1
    countdown_time_to_shot = FRAMERATE // 20

    def draw(self, win, offset_x, offset_y, scale): pass


    def find_target(self, dict_with_units):
    # find closest target in front of gun
    # set new target_coord, angle_to_target and dist_to target

        temp_coord = move_point(self.coord, self.min_radar_radius, self.base_angle)
        temp_dist = self.min_radar_radius
        temp_found_new_target = False 
        step = 15
        
        while temp_dist <= self.max_radar_radius:
            for unit_id in dict_with_units:
                if dict_with_units[unit_id].team_id != self.team_id and dict_with_units[unit_id].player_id and self.is_valid_target(dict_with_units[unit_id].unit_type) and dict_with_units[unit_id].is_alive:
                    if dict_with_units[unit_id].is_inside_hitbox(temp_coord, self.search_radius):
                    # dist = dist_two_points(unit.coord, temp_coord)
                    # if dist < self.search_radius:
                        temp_target_type = dict_with_units[unit_id].unit_type
                        temp_found_new_target = True
                        break
            if temp_found_new_target:
                break
            else:
                temp_dist += step
                temp_coord = move_point(temp_coord, step, self.base_angle)
        
        if temp_found_new_target:
            self.target_coord = temp_coord
            self.angle_to_target = self.base_angle # angle_to_target(self.coord, temp_coord)
            self.dist_to_target = temp_dist
            self.target_type = temp_target_type
            self.target_locked = True
        else:
            self.target_coord = self.coord
            self.target_locked = False


    def is_valid_target(self, unit_type):
    # checks (by unit type) if the target can be targeted
    # return True if target is valid
        # anti-aircrafts
        if unit_type == "air": return True
        else: return False


# ======================================================================
# Bomb dispensers


class Bomb_dispenser(Plane_fixed_gun):
    Ammunition_class = Bomb

    turn_speed = 0.2
    max_radar_radius = 200
    min_radar_radius = 170
    search_radius = 10

    max_bullet_range = 210
    barrel_length = 0

    power = 100
    description = "Bomb: 500dps (5x100ps)"
    drift_steps = 2

    countdown_time_to_search = FRAMERATE // 20
    countdown_time_to_shot = FRAMERATE

    number_of_bombs = 5

    def make_bullets(self, list_with_bullets):
    # function makes and shoot the bullet
    # return list_with_bullets
        bullet_coord = move_point(self.coord, self.barrel_length, self.angle)
        for _ in range(self.number_of_bombs):
            drift = random.randint(0, 2 * self.drift_steps) - self.drift_steps
            list_with_bullets.append(self.Ammunition_class(bullet_coord, self.angle + drift * 0.05, self.max_bullet_range, self.min_radar_radius, self.player_id, self.team_id, self.power, self.target_type))            
        return list_with_bullets


    def is_valid_target(self, unit_type):
    # checks (by unit type) if the target can be targeted
    # return True if target is valid
        # anti-aircrafts
        if unit_type == "land" or unit_type == "navy" or unit_type == "building": return True
        else: return False


class Advanced_bomb_dispenser(Bomb_dispenser):
    max_bullet_range = 270
    power = 100
    description = "Bomb: 1500dps (15x100ps)"
    number_of_bombs = 15
    drift_steps = 4
    search_radius = 10


# ======================================================================
# Missile launchers

class ASM_Launcher(Turret):
    # air-to-surface missile
    Ammunition_class = ASMissile

    max_radar_radius = 500
    min_radar_radius = 150
    search_radius = 10
    max_bullet_range = 1500
    power = 100
    description = "ASM: 100dps (3x100p3s)"

    countdown_time_to_search = FRAMERATE // 6
    countdown_time_to_shot = FRAMERATE * 3
    countdown_time_between_shots = FRAMERATE // 3

    number_of_bombs = 3

    def draw(self, win, offset_x, offset_y, scale): pass

    def run(self, dict_with_units, list_with_bullets):
    # life-cycle of the weapon
        if not self.countdown_to_search:
            # try to find target
            self.missiles_left = 0
            for unit_id in dict_with_units:
                if dict_with_units[unit_id].team_id != self.team_id and dict_with_units[unit_id].player_id and dict_with_units[unit_id].is_alive:
                    if self.is_valid_target(dict_with_units[unit_id].unit_type):             
                        dist = math.hypot(self.coord[0]-dict_with_units[unit_id].coord[0], self.coord[1]-dict_with_units[unit_id].coord[1])
                        if dist < self.max_radar_radius \
                                and dist > self.min_radar_radius:
                            self.missiles_left = self.number_of_bombs
                            self.countdown_to_search = self.countdown_time_to_shot # don't search until next shot
                            break
            if not self.missiles_left:
                self.countdown_to_search = self.countdown_time_to_search # wait for next search
        else:
            self.countdown_to_search -= 1

        if self.missiles_left:
            if not self.countdown_to_shot:
                # make missile
                self.make_bullets(list_with_bullets)
                self.missiles_left -=1
                self.countdown_to_shot = self.countdown_time_between_shots
            else:
                self.countdown_to_shot -= 1

    def make_bullets(self, list_with_bullets):
    # function makes and shoot the bullet
    # return list_with_bullets
        list_with_bullets.append(self.Ammunition_class(self.coord, self.base_angle, self.max_bullet_range, self.min_radar_radius, self.player_id, self.team_id, self.power, "surface"))            
        return list_with_bullets

    def is_valid_target(self, unit_type):
    # checks (by unit type) if the target can be targeted
    # return True if target is valid
        # anti-aircrafts
        if unit_type == "land" or unit_type == "navy" or unit_type == "building": return True
        else: return False


# ======================================================================
# Empty slot


class Empty_slot(Turret): 
    description = ""
    def draw(self, win, offset_x, offset_y, scale): pass
    def draw_extra_data(self, win, offset_x, offset_y, scale): pass
    def draw_range(self, win, offset_x, offset_y, scale): pass
    def run(self, list_with_units, list_with_bullets): pass

class Capture(Turret): 
    description = "Capture"
    def draw(self, win, offset_x, offset_y, scale): pass
    def draw_extra_data(self, win, offset_x, offset_y, scale): pass
    def draw_range(self, win, offset_x, offset_y, scale): pass
    def run(self, list_with_units, list_with_bullets): pass
