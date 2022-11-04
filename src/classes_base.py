import pygame

from settings import *
from functions_math import *


class Base_animated_object:
    path = ANT_PATH
    number_of_frames = ANT_FRAMES
    number_of_frames_in_sequence = ANT_FRAMES - 1


    def __init__(self, coord, angle):
    # initialization of the object

        # basic variables
        self.coord = coord
        self.angle = angle

        self.state = "move"

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

        # prepare clock
        self.last_time = 0
        self.frame = 0
        self.frame_interval = 1000 // self.number_of_frames_in_sequence

        # set first frame
        self.frame_sprite = self.sprite_list[0]   


    def draw(self, win, offset_x, offset_y, scale):
    # main method for preparing and drawing the object on the screen

        # count frames and load new sprite when the change will occur
        if self.frame_clock():
            self.frame_sprite = self.sprite_list[self.get_frame_index()] 

        # draw
        self.draw_sprite(win, offset_x, offset_y, scale)


    def draw_sprite(self, win, offset_x, offset_y, scale):
    # draw currently loaded sprite of the object on the screen    
        scaled_image = pygame.transform.scale(self.frame_sprite, (scale * self.frame_width, scale * self.frame_height))
        rotated_image = pygame.transform.rotate(scaled_image, -math.degrees(self.angle))
        new_rect = rotated_image.get_rect(center = world2screen(self.coord, offset_x, offset_y, scale))
        win.blit(rotated_image, new_rect.topleft)


    def frame_clock(self):
    # changes the frame as time passes
    # return true when the change will occur
        current_time = pygame.time.get_ticks()
        if current_time > self.last_time + self.frame_interval:
            self.last_time = current_time
            self.frame += 1
            if self.frame == self.number_of_frames_in_sequence: 
                self.frame = 0
            return True
        return False


    def crop_sprite(self, sprite_sheet, no_of_frame):
    # function that crops and return one frame from sprite sheet
        image = pygame.Surface((self.frame_width, self.frame_height))
        image.blit(sprite_sheet, (0, 0), (no_of_frame * self.frame_width, 0, self.frame_width, self.frame_height))
        image.convert()
        image.set_colorkey(BLACK)

        return image


    def get_frame_index(self):
    # count frame index to get sprite from sprite list
        if self.state == "stop":
            return 0
        if self.state == "move":
            offset = 0
        
        return self.number_of_frames_in_sequence * offset + self.frame + 1


    def get_position(self):
    # return coordinates
        return self.coord

    def get_angle(self):
    # return angle
        return self.angle