import pygame
import random
import math

from settings import *

class HexTile:

    def __init__(self):
        self.coord = (0, 0)
        self.color = [MARS_RED[0] - random.randint(0, 20), MARS_RED[1] + random.randint(0, 20), MARS_RED[2]]

    def compute_corners(self, new_coord, tile_radius):
    # compute a list of the hexagon's corners
    
        self.coord = new_coord
        x, y = self.coord
        self.outer_tile_radius = tile_radius # outer radius = lenght of the edge
        self.inner_tile_radius = self.outer_tile_radius * SQRT3 / 2 # inner radius        

        # self.coord is in the center, 
        # hex is pointy topped,
        # corners are listed clockwise
        self.corners = [
                (x, y - self.outer_tile_radius ),
                (x + self.inner_tile_radius, y - self.outer_tile_radius / 2),
                (x + self.inner_tile_radius, y + self.outer_tile_radius / 2),
                (x, y + self.outer_tile_radius),
                (x - self.inner_tile_radius, y + self.outer_tile_radius / 2),
                (x - self.inner_tile_radius, y - self.outer_tile_radius / 2),
            ]

    def draw(self, win):
    # draw the HexTile on the screen
        pygame.draw.polygon(win, self.color, self.corners)