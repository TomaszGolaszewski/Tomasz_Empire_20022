import pygame
import math

from settings import *
from classes_hex import *

class Map:
    Tile_generation = HexTile

    def __init__(self, map_width, map_height, tile_edge_length):
    # initialization of the map
        self.map_width = map_width # number of tiles horizontally
        self.map_height = map_height # number of tiles vertically

        self.tile_edge_length = tile_edge_length
        self.outer_tile_radius = tile_edge_length # outer radius = length of the edge
        self.inner_tile_radius = tile_edge_length * SQRT3 / 2 # inner radius

        self.BOARD = [] # 2D list with HexTiles

        for y in range(self.map_height):
            row = []
            for x in range(self.map_width):
                row.append(self.Tile_generation((x, y), self.id2world((x, y)), tile_edge_length))
            self.BOARD.append(row)

        self.old_offset_x = 0
        self.old_offset_y = 0
        self.old_scale = 1


    def draw(self, win):
    # draw the Map on the screen
        for row in self.BOARD:
            for tile in row:
                tile.draw(win)


    def update_screen_corners(self, offset_x, offset_y, scale = 1):
    # upload coordinates of the HexTiles

        if self.old_offset_x != offset_x or self.old_offset_y != offset_y or self.old_scale != scale:
            self.old_offset_x = offset_x
            self.old_offset_y = offset_y
            self.old_scale = scale

            for row in self.BOARD:
                for tile in row:
                    tile.update_screen_corners(offset_x, offset_y, scale)


    def degrade(self, coord, level):
    # degrade the tile - it will be darker
        x_id, y_id = self.world2id(coord)
        if 0 <= x_id  and x_id < self.map_width and 0 <= y_id  and y_id < self.map_height:
            self.BOARD[y_id][x_id].degrade(level)


    def id2world(self, id):
    # calculate coordinates from tile's id to world coordinate system
    # return coordinates in the world coordinate system

        x_id, y_id = id

        if y_id % 2:
            x_world = (2 * x_id + 1) * self.inner_tile_radius
        else:
            x_world = 2 * x_id * self.inner_tile_radius

        y_world = 3 / 2 * self.outer_tile_radius * y_id

        return (x_world, y_world)

    
    def world2id(self, coord):
    # calculate coordinates from world coordinate system to tile's id
    # return tile's id coordinates

        x_world, y_world = coord
        
        y_id = int(2 / 3 * y_world / self.outer_tile_radius + 0.5)

        if y_id % 2:
            x_id = int(x_world / self.inner_tile_radius / 2)
        else:
            x_id = int(x_world / self.inner_tile_radius / 2 + 0.5)

        return (x_id, y_id)


class Map_v2(Map):
    Tile_generation = HexTile_v2
    
    def __init__(self, map_width, map_height, tile_edge_length):
    # initialization of the map
        Map.__init__(self, map_width, map_height, tile_edge_length)

        self.map_sprite_width_world = (self.map_width * 2 - 1) * self.inner_tile_radius
        self.map_sprite_height_world = (self.map_height - 1) * self.outer_tile_radius * 3 / 2

        # load and prepare mipmap sprites
        self.MIPMAP_BOARD = []
        for mipmap_level in range(5):
            scale = self.mipmap2scale(mipmap_level)
            sprite = pygame.Surface([self.map_sprite_width_world * scale, self.map_sprite_height_world * scale])
            # sprite.fill(GREEN)
            # sprite.fill(BLACK)
            sprite.convert()
            # sprite.set_colorkey(BLACK)

            for row in self.BOARD:
                for tile in row:
                    tile.draw(sprite, scale)
            self.MIPMAP_BOARD.append(sprite)


    def draw(self, win, offset_x, offset_y, scale):
    # draw the Map on the screen
        win.blit(self.MIPMAP_BOARD[self.scale2mipmap(scale)], (0, 0), (- offset_x * scale, - offset_y * scale, WIN_WIDTH - 1, WIN_HEIGHT - 1))


    def degrade(self, coord, level):
    # degrade the tile - it will be darker
        x_id, y_id = self.world2id(coord)
        if 0 <= x_id  and x_id < self.map_width and 0 <= y_id  and y_id < self.map_height:
            if self.BOARD[y_id][x_id].degradation_level < level:
                self.BOARD[y_id][x_id].degrade(level)
                for mipmap_level in range(5):
                    scale = self.mipmap2scale(mipmap_level)
                    self.BOARD[y_id][x_id].draw(self.MIPMAP_BOARD[mipmap_level], scale)


    def scale2mipmap(self, scale):
    # calculate scale from regular scale to mipmap level
    # return mipmap level
        mipmap_level = int(math.log(scale, 2)) + 2
        return mipmap_level


    def mipmap2scale(self, mipmap_level):
    # calculate scale from mipmap level to regular scale
    # return regular scale
        scale = pow(2, mipmap_level - 2)
        return scale