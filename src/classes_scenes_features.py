import pygame

from settings import *
from setup import *


class FixText:
    def __init__(self, coord, text="Base Fix Text", size=20, font="arial", color=LIME):
    # initialization of the text
        font = pygame.font.SysFont(font, size)
        self.coord = coord #.copy()
        self.text_obj = font.render(text, True, color)
        self.text_rect = self.text_obj.get_rect(center=self.coord)

    def draw(self, win):
    # draw text on the screen
        win.blit(self.text_obj, self.text_rect)


class BaseButton(FixText):
    def __init__(self, coord, text="Base Button", size=20, font="arial", color=LIME):
    # initialization of the button
        FixText.__init__(self, coord, text, size, font, color)

    def is_inside(self, sample_coord):
    # check if the coordinates are inside the button
    # return True if yes
        if self.text_rect.collidepoint(sample_coord): return True
        else: return False
