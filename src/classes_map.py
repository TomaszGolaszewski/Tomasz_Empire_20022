import pygame
import math

from settings import *
from classes_hex import *

class Map:

    def __init__(self, map_width, map_height, tile_radius):
    # initialization of the map
        self.map_width = map_width # number of tiles horizontally
        self.map_height = map_height # number of tiles vertically
        self.outer_tile_radius = tile_radius # outer radius = lenght of the edge
        self.inner_tile_radius = self.outer_tile_radius * SQRT3 / 2 # inner radius

        self.coord = [100, 100] # map position

        self.BOARD = [] # 2D list with HexTiles

        for y in range(map_height):
            row = []
            for x in range(map_width):
                row.append(HexTile())
            self.BOARD.append(row)

        self.upload(100, 100, 1)

    def upload(self, offset_x, offset_y, scale):
    # upload coordinates of the HexTiles
        i_x = 0
        i_y = 0
        for row in self.BOARD:
            if i_y % 2:
                for tile in row:
                    tile.compute_corners([(2 * i_x + 1) * self.inner_tile_radius * scale + offset_x, 3 / 2 * self.outer_tile_radius * i_y * scale + offset_y], self.outer_tile_radius )
                    i_x += 1
            else:
                for tile in row:
                    tile.compute_corners([2 * i_x * self.inner_tile_radius * scale + offset_x, 3 / 2 *  self.outer_tile_radius * i_y * scale + offset_y], self.outer_tile_radius )
                    i_x += 1

            i_x = 0
            i_y += 1

    def draw(self, win):
    # draw the Map on the screen
        for row in self.BOARD:
            for tile in row:
                tile.draw(win)