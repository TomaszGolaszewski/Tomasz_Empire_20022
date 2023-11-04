import pygame

from settings import *
from setup import *


class FixText:
    def __init__(self, coord, text="Base Fix Text", size=20, font="arial", color=LIME):
    # initialization of the text
        font_obj = pygame.font.SysFont(font, size)
        self.coord = coord #.copy()
        self.text_obj = font_obj.render(text, True, color)
        self.text_rect = self.text_obj.get_rect(center=self.coord)

    def draw(self, win):
    # draw text on the screen
        win.blit(self.text_obj, self.text_rect)


class DynamicText(FixText):
    def __init__(self, coord, text="Dynamic Text", size=20, font="arial", color=LIME):
    # initialization of the text
        FixText.__init__(self, coord, text, size, font, color)
        self.text = text
        self.size = size
        self.font = font
        self.color = color

    def set_text(self, text):
    # set new text and next recalculate object attributes
        self.text = text
        font_obj = pygame.font.SysFont(self.font, self.size)
        self.text_obj = font_obj.render(text, True, self.color)
        self.text_rect = self.text_obj.get_rect(center=self.coord)


class BaseButton(FixText):
    def __init__(self, coord, text="Base Button", size=20, font="arial", color=LIME):
    # initialization of the button
        FixText.__init__(self, coord, text, size, font, color)

    def is_inside(self, sample_coord):
    # check if the coordinates are inside the button
    # return True if yes
        if self.text_rect.collidepoint(sample_coord): return True
        else: return False
