import pygame

# from settings import *
from setup import *
from functions_math import *
from functions_player import *


class Base_slide_button:
    path = BUTTON_1_PATH

    def __init__(self, coord):
    # initialization of the object

        # basic variables
        self.coord = coord
        self.to_remove = False

        # load and prepare sprite
        self.sprite = pygame.image.load(os.path.join(*self.path))
        self.sprite.convert()
        # self.sprite.convert_alpha()
        self.sprite.set_colorkey(BLACK)
        # self.sprite.set_alpha(50)

        # calculate frame size
        sprite_rect = self.sprite.get_rect()
        self.frame_width = sprite_rect.width
        self.frame_height = sprite_rect.height

    def draw(self, win):
    # draw the object on the screen
        new_rect = self.sprite.get_rect(center = self.coord)
        win.blit(self.sprite, new_rect.topleft)

    def press(self, list_with_units, press_coord, target, is_ctrl_down):
    # handle actions after button is pressed
        # check if center is pressed
        dist = math.hypot(self.coord[0]-press_coord[0], self.coord[1]-press_coord[1])
        if dist < 25:
            # print("center")
            set_new_target_move(list_with_units, target, is_ctrl_down)
        else:
            # check sector       
            angle = math.degrees(angle_to_target(self.coord, press_coord))
            if angle < 270 and angle > 90:
                # print("left")
                set_new_target_regroup(list_with_units, target, is_ctrl_down)
            else:
                # print("right")
                set_new_target_move(list_with_units, target, is_ctrl_down)
        print()
        self.to_remove = True