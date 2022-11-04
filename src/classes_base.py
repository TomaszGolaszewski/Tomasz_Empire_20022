import pygame

from settings import *
from functions_math import *


class Base_animated_object:
    path = ANT_PATH
    number_of_frames = ANT_FRAMES

    def __init__(self, coord, angle):
    # initialization of the object

        # basic variables
        self.coord = coord
        self.angle = angle

        self.state = "stop"

        # load and prepare sprite sheet
        self.sprite_sheet = pygame.image.load(os.path.join(*self.path))
        self.sprite_sheet.convert()
        self.sprite_sheet.set_colorkey(BLACK)

        # calculate frame size
        sprite_sheet_rect = self.sprite_sheet.get_rect()
        self.frame_width = sprite_sheet_rect.width // self.number_of_frames
        self.frame_height = sprite_sheet_rect.height

        # crop sprite sheet into frames - store frames in sprite list
        self.sprite_list = []
        for i in range(self.number_of_frames):
            self.sprite_list.append(self.crop_sprite(self.sprite_sheet, i))

        # set first frame
        self.frame = self.sprite_list[0]


    def draw(self, win, offset_x, offset_y, scale):
    # draw the object on the screen
        
        
        scaled_image = pygame.transform.scale(self.frame, (scale * self.frame_width, scale * self.frame_height))
        rotated_image = pygame.transform.rotate(scaled_image, -math.degrees(self.angle))
        new_rect = rotated_image.get_rect(center = world2screen(self.coord, offset_x, offset_y, scale))
        win.blit(rotated_image, new_rect.topleft)


    # def draw_extra_data(self, win, offset_x, offset_y, scale):
    # # draw extra data about the object on the screen
    #     pass

    # def run(self, *args):
    # # life-cycle of the object
    #     pass


    def crop_sprite(self, sprite_sheet, no_of_frame):
    # function that crops and return one frame from sprite sheet
        image = pygame.Surface((self.frame_width, self.frame_height))
        image.blit(sprite_sheet, (no_of_frame * self.frame_width, 0, self.frame_width, self.frame_height))
        image.convert()
        image.set_colorkey(BLACK)

        return image


    def get_position(self):
    # return coordinates
        return self.coord

    def get_angle(self):
    # return angle
        return self.angle