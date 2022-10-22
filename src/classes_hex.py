import pygame
import random

from settings import *
from functions_math import *

class HexTile:

    def __init__(self, coord_id, coord_world, edge_length):
    # initialization of the HexTile
        self.coord_id = coord_id
        self.coord_world = coord_world
        self.coord_screen = coord_world

        self.edge_length_world = edge_length

        self.corners_world = self.compute_corners(coord_world, edge_length)
        self.corners_screen = self.corners_world.copy()

        self.color = [MARS_RED[0] - random.randint(0, 20), MARS_RED[1] + random.randint(0, 20), MARS_RED[2]]


    def draw(self, win):
    # draw the HexTile on the screen
        pygame.draw.polygon(win, self.color, self.corners_screen)


    def update_screen_corners(self, offset_x, offset_y, scale = 1):
    # update the hexagon's corners' coordinates in screen coordinate system
        self.coord_screen = world2screen(self.coord_world, offset_x, offset_y, scale)
        self.corners_screen = self.compute_corners(self.coord_screen, self.edge_length_world * scale)


    def compute_corners(self, center_coord, edge_length):
    # compute a list of the hexagon's corners
    # return list with corners' coordinates
    
        x, y = center_coord
        outer_tile_radius = edge_length # outer radius = length of the edge
        inner_tile_radius = edge_length * SQRT3 / 2 # inner radius        

        # self.coord is in the center, 
        # hex is pointy topped,
        # corners are listed clockwise
        return [
                (x, y - outer_tile_radius ),
                (x + inner_tile_radius, y - outer_tile_radius / 2),
                (x + inner_tile_radius, y + outer_tile_radius / 2),
                (x, y + outer_tile_radius),
                (x - inner_tile_radius, y + outer_tile_radius / 2),
                (x - inner_tile_radius, y - outer_tile_radius / 2),
            ]
