import pygame

from settings import *


def set_rectangle_with_two_corners(corner1, corner2):
# function that returns rectangle with two defined corners
    x1, y1 = corner1
    x2, y2 = corner2

    horizontal_edge = abs(x1 - x2)
    vertical_edge = abs(y1 - y2)

    x = min(x1, x2)
    y = min(y1, y2)

    return pygame.Rect(x, y, horizontal_edge, vertical_edge)
    
