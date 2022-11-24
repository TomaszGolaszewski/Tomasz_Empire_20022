import pygame
import math

from settings import *
from classes_hex import *

class Map:
    def __init__(self, map_width, map_height, type="mars_plain", tile_edge_length=30):
    # initialization of the map
        self.map_width = map_width # number of tiles horizontally
        self.map_height = map_height # number of tiles vertically

        self.tile_edge_length = tile_edge_length
        self.outer_tile_radius = tile_edge_length # outer radius = length of the edge
        self.inner_tile_radius = tile_edge_length * SQRT3 / 2 # inner radius
   
        self.old_offset_x = 0
        self.old_offset_y = 0
        self.old_scale = 1
        
        self.type = type
        self.BOARD = [] # 2D list with HexTiles

        # preparing the board
        if self.type == "mars_poles": self.make_mars_poles()
        elif self.type == "lake": self.make_lake()
        else: self.make_plain()

    def make_plain(self):
    # method preparing the board covered with one type of terrain
        if self.type == "mars_plain": tile_type = "mars"
        elif self.type == "snow_plain": tile_type = "snow"
        elif self.type == "grass_plain": tile_type = "grass"
        elif self.type == "concrete_floor": tile_type = "concrete"
        else: tile_type = "other"

        for y in range(self.map_height):
            row = []
            for x in range(self.map_width):
                row.append(HexTile((x, y), self.id2world((x, y)), self.tile_edge_length, tile_type))
            self.BOARD.append(row)

    def make_mars_poles(self):
    # method preparing the board covered with mars plain and two poles - north and south
        north_pole = self.map_height // 10
        south_pole = self.map_height * 9 // 10
        choose_one = ["snow", "snow", "mars", "mars"]
        for y in range(self.map_height):
            row = []           
            if y < north_pole or y > south_pole: tile_type = "snow"
            else: tile_type = "mars"
            for x in range(self.map_width):
                if y == north_pole or y == south_pole: tile_type = choose_one[random.randint(1,2)] 
                if y == north_pole-1 or y == south_pole+1: tile_type = choose_one[random.randint(0,2)] # outer
                if y == north_pole+1 or y == south_pole-1: tile_type = choose_one[random.randint(1,3)] # inner
                row.append(HexTile((x, y), self.id2world((x, y)), self.tile_edge_length, tile_type))
            self.BOARD.append(row)

    def make_lake(self):
    # method preparing the board in shape of lake
        center_x = self.map_width // 2
        center_y = self.map_height // 2
        factor = (center_x * center_y) // 2
        for y in range(self.map_height):
            row = []
            for x in range(self.map_width):
                tile_type = self.decide_type_tile(abs(center_x - x) * abs(center_y - y), factor)
                row.append(HexTile((x, y), self.id2world((x, y)), self.tile_edge_length, tile_type))
            self.BOARD.append(row)

    def decide_type_tile(self, fun, factor):
    # return type of tile depending on the result of the function
        if fun > factor * 1.5: return "grass"
        elif fun > factor: return "sand"
        elif fun > factor / 2: return "shallow"
        else: return "water"

    def draw(self, win):
    # draw the Map on the screen
        for row in self.BOARD:
            for tile in row:
                tile.draw_only(win)

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
    def __init__(self, map_width, map_height, type="snow_plain", tile_edge_length=25):
    # initialization of the map
        Map.__init__(self, map_width, map_height, type, tile_edge_length)

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
        win.blit(self.MIPMAP_BOARD[self.scale2mipmap(scale)], (1, 1), (- offset_x * scale, - offset_y * scale, WIN_WIDTH - 2, WIN_HEIGHT - 2))

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