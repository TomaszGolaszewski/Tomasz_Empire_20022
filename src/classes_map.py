import pygame
import math

from perlin_noise import PerlinNoise

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
        
        # preparing the board
        self.type = type
        self.BOARD = [] # 2D list with HexTiles
        if self.type == "mars_poles": self.make_mars_poles()
        elif self.type == "lake" or self.type == "island" or self.type == "bridge": self.make_map_based_on_ellipse()
        elif self.type == "forest" or self.type == "snow_forest": self.make_forest_map()
        elif self.type == "noise": self.make_noise_map()
        else: self.make_plain()

        # preparing land for buildings
        self.places_for_naval_factories = []
        self.places_for_land_factories = []
        self.places_for_generators = []
        self.find_places_for_naval_factories()
        self.find_places_for_land_factories()
        self.find_places_for_generators()

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

    def make_map_based_on_ellipse(self):
    # method preparing the board with an ellipse-based shape
        noise = PerlinNoise(octaves=12)
        center_x = self.map_width // 2
        center_y = self.map_height // 2
        if self.type == "lake": 
            # method preparing the board in shape of lake
            function = lambda x, y: abs(center_x - x)**2 / (center_x**2) + abs(center_y - y)**2 / (center_y**2)
            factor = 0.6
        elif self.type == "island": 
            # method preparing the board in shape of island
            function = lambda x, y: 1 - abs(center_x - x)**2 / (center_x**2) - abs(center_y - y)**2 / (center_y**2)
            factor = 0.6
        elif self.type == "bridge":
            # method preparing the board in shape of bridge
            function = lambda x, y: (center_x - abs(center_x - x))**2 / (center_x**2) * 0.5 + 1 * abs(center_y - y)**2 / (center_y**2)
            factor = 0.6

        for y in range(self.map_height):
            row = []
            for x in range(self.map_width):
                tile_type, depth = self.decide_type_tile(function(x, y) + 0.125 * noise([x / self.map_width, y / self.map_height]), factor)
                if depth > 20: depth = 20
                row.append(HexTile((x, y), self.id2world((x, y)), self.tile_edge_length, tile_type, depth))
            self.BOARD.append(row)

    def make_forest_map(self):
    # method preparing the board with forest
        if self.type == "forest":
            empty_tile = "grass"
            trees_tile = "forest"
        elif self.type == "snow_forest":
            empty_tile = "snow"
            trees_tile = "snow_forest"

        noise = PerlinNoise(octaves=12)

        for y in range(self.map_height):
            row = []
            for x in range(self.map_width):
                if noise([x / self.map_width, y / self.map_height]) > 0.02: tile_type = trees_tile
                else: tile_type = empty_tile
                row.append(HexTile((x, y), self.id2world((x, y)), self.tile_edge_length, tile_type))
            self.BOARD.append(row)

    # def make_noise_map(self):
    # # method preparing the board based on Perlin Noise
    #     noise = PerlinNoise(octaves=9, seed=1)
    #     factor = 0.5
    #     for y in range(self.map_height):
    #         row = []
    #         for x in range(self.map_width):
    #             tile_type, depth = self.decide_type_tile(3 * noise([x / self.map_width, y / self.map_height]), factor)
    #             if depth > 20: depth = 20
    #             row.append(HexTile((x, y), self.id2world((x, y)), self.tile_edge_length, tile_type, depth))
    #         self.BOARD.append(row)

    def make_noise_map(self):
    # method preparing the board based on Perlin Noise
        noise1 = PerlinNoise(octaves=3)
        noise2 = PerlinNoise(octaves=6)
        noise3 = PerlinNoise(octaves=12)
        noise4 = PerlinNoise(octaves=24)
        factor = 0.5
        for y in range(self.map_height):
            row = []
            for x in range(self.map_width):
                noise_val = noise1([x / self.map_width, y / self.map_height])
                noise_val += 0.5 * noise2([x / self.map_width, y / self.map_height])
                noise_val += 0.25 * noise3([x / self.map_width, y / self.map_height])
                noise_val += 0.125 * noise4([x / self.map_width, y / self.map_height])
                tile_type, depth = self.decide_type_tile(2 * noise_val + 0.3, factor)
                if depth > 20: depth = 20
                row.append(HexTile((x, y), self.id2world((x, y)), self.tile_edge_length, tile_type, depth))
            self.BOARD.append(row)

    def decide_type_tile(self, fun, factor, forest_on = True):
    # return type of tile depending on the result of the function
        depth = int(abs(factor - fun) * 20 / factor)
        if fun > factor * 1.9 and forest_on: tile_type = "forest"
        elif fun > factor * 1.3: tile_type = "grass"
        elif fun > factor: tile_type = "sand"
        elif fun > factor * 0.7: tile_type = "shallow"
        else: tile_type = "water"

        return tile_type, depth
    
    def find_places_for_naval_factories(self):
    # find places for naval factories
        x_id = 5
        while x_id < self.map_width:
            y_id = 7
            while y_id < self.map_height - 7:
                if self.BOARD[y_id][x_id].type == "shallow" and (self.BOARD[y_id][x_id].depth == 3 or self.BOARD[y_id][x_id].depth == 2):
                    # check for collisions with previous factories
                    place_is_good = True
                    for previous_places_coord in self.places_for_naval_factories:
                        previous_x, previous_y = self.world2id(previous_places_coord) 
                        if abs(previous_x - x_id) < 5 and abs(previous_y - y_id) < 5: place_is_good = False
                    # add new place for naval factory
                    if place_is_good: self.places_for_naval_factories.append(self.id2world([x_id, y_id]))
                # skip middle of the map
                if y_id == self.map_height // 3: y_id += self.map_height // 3
                else: y_id += 1
            x_id += 10

    def find_places_for_land_factories(self):
    # find places for land factories
        y_id = 7
        while y_id < self.map_height // 3:
            x_id = 5
            while x_id < self.map_width:
                # top half of the map
                if self.BOARD[y_id][x_id].type != "water" and self.BOARD[y_id][x_id].type != "shallow":
                    self.places_for_land_factories.append(self.id2world([x_id, y_id]))
                # bottom half of the map
                if self.BOARD[self.map_height - y_id][x_id].type != "water" and self.BOARD[self.map_height - y_id][x_id].type != "shallow":
                    self.places_for_land_factories.append(self.id2world([x_id, self.map_height - y_id]))
                x_id += 10
            y_id += 10
        

    def find_places_for_generators(self):
    # find places for generators
        x_id = self.map_width // 2
        y_id = 5
        while y_id < self.map_height:
            # x = -10
            if self.BOARD[y_id][x_id - 10].type != "water" and self.BOARD[y_id][x_id - 10].type != "shallow":
                self.places_for_generators.append(self.id2world([x_id - 10, y_id]))
            # x = 0
            if self.BOARD[y_id][x_id].type != "water" and self.BOARD[y_id][x_id].type != "shallow":
                self.places_for_generators.append(self.id2world([x_id, y_id]))
            # x = +10
            if self.BOARD[y_id][x_id + 10].type != "water" and self.BOARD[y_id][x_id + 10].type != "shallow":
                self.places_for_generators.append(self.id2world([x_id + 10, y_id]))
            y_id += 10
        # self.places_for_naval_factories = []
        # self.places_for_land_factories = []

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
        if 0 <= x_id  and x_id < self.map_width and 0 <= y_id and y_id < self.map_height:
            self.BOARD[y_id][x_id].degrade(level)

    def get_tile_type(self, coord):
    # return the tile type
        x_id, y_id = self.world2id(coord)
        if 0 <= x_id  and x_id < self.map_width and 0 <= y_id and y_id < self.map_height:
            return self.BOARD[y_id][x_id].type
        else: return "out_of_map"

    def get_tile_degradation_level(self, coord):
    # return the tile degradation level
        x_id, y_id = self.world2id(coord)
        if 0 <= x_id  and x_id < self.map_width and 0 <= y_id and y_id < self.map_height:
            return self.BOARD[y_id][x_id].degradation_level
        else: return -1

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

# ==========================================================

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
        if scale == 4:
            temp_surface_S = pygame.Surface((WIN_WIDTH // 2, WIN_HEIGHT // 2))
            temp_surface_S.blit(self.MIPMAP_BOARD[4], (0, 0), (- offset_x * 2, - offset_y * 2, WIN_WIDTH // 2, WIN_HEIGHT // 2)) # 2 is scale for used surface
            temp_surface_L = pygame.transform.scale2x(temp_surface_S)      
            win.blit(temp_surface_L, (0, 0))
            # print(str(temp_surface_L.get_width()))
        else:
            win.blit(self.MIPMAP_BOARD[self.scale2mipmap(scale)], (0, 0), (- offset_x * scale, - offset_y * scale, WIN_WIDTH, WIN_HEIGHT))

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
        mipmap_level = int(math.log(scale, 2)) + 3
        return mipmap_level

    def mipmap2scale(self, mipmap_level):
    # calculate scale from mipmap level to regular scale
    # return regular scale
        scale = pow(2, mipmap_level - 3)
        return scale