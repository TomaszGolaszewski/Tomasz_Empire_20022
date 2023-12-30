import pygame
import math

from perlin_noise import PerlinNoise

from settings import *
from classes_hex import *

class Map:
    def __init__(self, map_width, map_height, type="mars_plain", tile_edge_length=30, clean=False, forest_on=False):
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
        elif self.type == "lake" or self.type == "island" or self.type == "bridge": self.make_map_based_on_ellipse(forest_on=forest_on)
        elif self.type == "forest" or self.type == "snow_forest": self.make_forest_map()
        elif self.type == "noise": self.make_noise_map()
        else: self.make_plain()

        # preparing land for buildings
        self.places_to_start = []
        self.places_for_naval_factories = []
        self.places_for_land_factories = []
        self.places_for_generators = []
        self.find_places_to_start()
        if not clean:
            self.find_places_for_land_factories()
            self.find_places_for_naval_factories()     
            self.find_places_for_generators()
            self.make_buildings_foundation()

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

    def make_map_based_on_ellipse(self, forest_on=False):
    # method preparing the board with an ellipse-based shape
        noise = PerlinNoise(octaves=12)
        center_x = self.map_width // 2
        center_y = self.map_height // 2
        if self.type == "lake": 
            # method preparing the board in shape of lake
            function = lambda x, y: 0.5 * max([abs(center_x - x) / center_x, abs(center_y - y) / center_y]) + \
                                    0.3 * ((center_x - x)**2 / center_x**2 + (center_y - y)**2 / center_y**2) - 0.2
            factor = 0.4
            forest_correction = 0.1
        elif self.type == "island": 
            # method preparing the board in shape of island
            function = lambda x, y: 1 - (center_x - x)**2 / center_x**2 - (center_y - y)**2 / center_y**2 - 0.3
            factor = 0.45
            forest_correction = 0.2
        elif self.type == "bridge":
            # method preparing the board in shape of bridge
            function = lambda x, y: (center_x - abs(center_x - x))**2 / (center_x**2) * 0.5 + 1 * abs(center_y - y)**2 / (center_y**2)
            factor = 0.6
            forest_correction = 0.1
        elif self.type == "corners":
            # method preparing the board in shape of 4 corners
            function = lambda x, y: abs((center_x - x)*(center_y - y)) / (center_x * center_y)
            factor = 0.6
            forest_correction = 0

        for y in range(self.map_height):
            row = []
            for x in range(self.map_width):
                tile_type, depth = self.decide_type_tile(function(x, y) + 0.125 * noise([x / self.map_width, y / self.map_height]), \
                                                        factor, forest_on=forest_on, forest_correction=forest_correction)
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

    def decide_type_tile(self, fun, factor, forest_on=False, forest_correction=0):
    # return type of tile depending on the result of the function
        depth = int(abs(factor - fun) * 20 / factor)
        if (fun > factor * 1.9 - forest_correction) and forest_on: tile_type = "forest"
        elif fun > factor * 1.3: tile_type = "grass"
        elif fun > factor: tile_type = "sand"
        elif fun > factor * 0.7: tile_type = "shallow"
        else: tile_type = "water"

        return tile_type, depth
    
    def find_places_to_start(self):
    # find the best starting locations for each player 

        if self.type == "lake": 
            temp_x = self.map_width // 10
            temp_y = self.map_height // 10
        elif self.type == "island": 
            temp_x = self.map_width // 3 + 2
            temp_y = self.map_height // 3 + 2
        elif self.type == "bridge":
            temp_x = self.map_width // 10 + 2
            temp_y = self.map_height // 15 + 2
        else:
            temp_x = self.map_width // 6
            temp_y = self.map_height // 6

        self.places_to_start.append(self.id2world([temp_x, temp_y])) # NW # blue
        self.places_to_start.append(self.id2world([temp_x, self.map_height - temp_y])) # SW # green
        self.places_to_start.append(self.id2world([self.map_width - temp_x, temp_y])) # NE # red
        self.places_to_start.append(self.id2world([self.map_width - temp_x, self.map_height - temp_y])) # SE # yellow
        
    def find_places_for_naval_factories(self, factories_per_player=3, min_dist=7):
    # find places for naval factories
        places_found = 0
        x_id = 4
        while x_id < self.map_width // 2 - min_dist // 2 and places_found < factories_per_player:
            y_id = 7
            while y_id < self.map_height // 3 - min_dist // 2 and places_found < factories_per_player:
                if self.BOARD[y_id][x_id].type == "shallow" and \
                            self.BOARD[y_id][x_id].depth in [3] and \
                            self.check_collision_with_buildings_on_list(self.places_for_land_factories, [x_id, y_id], min_dist) and \
                            self.check_collision_with_buildings_on_list(self.places_for_naval_factories, [x_id, y_id], min_dist):
                    self.append_buildings_mirrored_vertically_and_horizontally(self.places_for_naval_factories, [x_id, y_id])
                    places_found += 1
                y_id += 1
            x_id += 10

    def find_places_for_land_factories(self, buildings_in_group=3, group_radius=200):
    # find places for land factories
        if self.type == "bridge":
            # factories in line
            distance_in_tiles = group_radius // self.outer_tile_radius
            x_id, y_id = self.world2id(self.places_to_start[0])
            for i in range(buildings_in_group):
                temp_x = x_id + i * distance_in_tiles - distance_in_tiles // 2
                temp_y = max(y_id - distance_in_tiles, 5)
                self.append_buildings_mirrored_vertically_and_horizontally(self.places_for_land_factories, [temp_x, temp_y])
        else:
            # factories in circle
            angle_offset = 2 * math.pi / buildings_in_group
            center_x = self.map_width // 2
            center_y = self.map_height // 2
            center_world = self.id2world([center_x, center_y])
            for place in self.places_to_start:
                start_angle = angle_to_target(place, center_world)
                for i in range(buildings_in_group):
                    new_point = move_point(place, group_radius, start_angle + i  * angle_offset)
                    corrected_new_point = self.id2world(self.world2id(new_point))
                    # if self.BOARD[y_id][x_id].type != "water" and self.BOARD[y_id][x_id].type != "shallow":
                    self.places_for_land_factories.append(corrected_new_point)
                
    def find_places_for_generators(self, generators_per_player=6, min_dist=7, margin=5):
    # find places for generators       
        places_found = 0
        max_errors = 100
        current_error = 0
        center_x = self.map_width // 2
        center_y = self.map_height // 2
        min_dist_from_center = min_dist // 2
         
        while places_found < generators_per_player and current_error < max_errors:
            temp_x = random.randint(margin, center_x - min_dist_from_center)
            temp_y = random.randint(margin, center_y - min_dist_from_center)
            if self.BOARD[temp_y][temp_x].type != "water" and self.BOARD[temp_y][temp_x].type != "shallow" and \
                        self.check_collision_with_buildings_on_list(self.places_for_naval_factories, [temp_x, temp_y], min_dist) and \
                        self.check_collision_with_buildings_on_list(self.places_for_land_factories, [temp_x, temp_y], min_dist) and \
                        self.check_collision_with_buildings_on_list(self.places_for_generators, [temp_x, temp_y], min_dist):
                self.append_buildings_mirrored_vertically_and_horizontally(self.places_for_generators, [temp_x, temp_y])
                places_found += 1
                current_error = 0
            else:
                current_error += 1

    def check_collision_with_buildings_on_list(self, building_list_in_world, test_coord_in_id, min_distance):
    # check for collisions with buildings on list
    # return True if position is good
        for building_coord in building_list_in_world:
            building_x, building_y = self.world2id(building_coord) 
            if abs(building_x - test_coord_in_id[0]) < min_distance and abs(building_y - test_coord_in_id[1]) < min_distance: 
                return False
        return True
    
    def append_buildings_mirrored_vertically_and_horizontally(self, list_with_places, start_coord_in_id):
    # append buildings on a list mirrored using vertical and horizontal axis of symmetry of the map
        temp_x, temp_y = start_coord_in_id
        list_with_places.append(self.id2world([temp_x, temp_y])) # NW
        list_with_places.append(self.id2world([self.map_width - temp_x, temp_y])) # NE
        list_with_places.append(self.id2world([self.map_width - temp_x, self.map_height - temp_y])) # SE
        list_with_places.append(self.id2world([temp_x, self.map_height - temp_y])) # SW

    def check_land_path(self, start_point, end_point):
    # return True if land path between points is safe
    # return False if it is not safe
        dist = math.hypot(start_point[0]-end_point[0], start_point[1]-end_point[1])
        traveled_dist = 0
        angle = angle_to_target(start_point, end_point)
        temp_coord = start_point #.copy()
        while traveled_dist < dist:
            temp_coord = move_point(temp_coord, self.tile_edge_length, angle)
            traveled_dist += self.tile_edge_length
            temp_file_type = self.get_tile_type(temp_coord)
            if temp_file_type in ["water", "concrete", "submerged_concrete"]: return False
        return True
    
    def check_water_path(self, start_point, end_point):
    # return True if water path between points is safe
    # return False if it is not safe
        dist = math.hypot(start_point[0]-end_point[0], start_point[1]-end_point[1])
        traveled_dist = 0
        angle = angle_to_target(start_point, end_point)
        temp_coord = start_point #.copy()
        while traveled_dist < dist:
            temp_coord = move_point(temp_coord, self.tile_edge_length, angle)
            traveled_dist += self.tile_edge_length
            temp_file_type = self.get_tile_type(temp_coord)
            if temp_file_type != "water" and temp_file_type != "shallow": return False
        return True
    
    def find_safe_middle_point(self, start_point, angle, is_land_unit=True):
    # return safe point closest to start_point on traverse to angle
        if is_land_unit:
            safe_tile_function = lambda temp_file_type: temp_file_type not in ["water", "concrete", "submerged_concrete", "out_of_map"]
        else:
            safe_tile_function = lambda temp_file_type: temp_file_type == "water" # or temp_file_type == "shallow"
        # check start point
        temp_file_type = self.get_tile_type(start_point)
        if safe_tile_function(temp_file_type):
            return start_point #.copy()
        # check left side
        left_angle = angle - math.pi / 2
        left_i = 0
        left_file_type = self.get_tile_type(start_point)
        left_point = start_point #.copy()
        while left_file_type != "out_of_map":
            left_point = move_point(left_point, self.tile_edge_length * 3, left_angle)
            left_i += 1
            left_file_type = self.get_tile_type(left_point)
            if safe_tile_function(left_file_type): break
        else:
            left_i += 50 # penalty points for leaving the map
        # check right side
        right_angle = angle + math.pi / 2
        right_i = 0
        right_file_type = self.get_tile_type(start_point)
        right_point = start_point #.copy()
        while right_file_type != "out_of_map":
            right_point = move_point(right_point, self.tile_edge_length * 3, right_angle)
            right_i += 1
            right_file_type = self.get_tile_type(right_point)
            if safe_tile_function(right_file_type): break
        else:
            right_i += 50 # penalty points for leaving the map
        # choose closer point
        if left_i < right_i: return left_point
        else: return right_point

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

    def make_buildings_foundation(self):
    # change area around buildings into concrete
        for naval_factory_coord in self.places_for_naval_factories:
            self.change_tiles_around_point(naval_factory_coord, "submerged_concrete", 1)
        for land_factory_coord in self.places_for_land_factories:
            self.change_tiles_around_point(land_factory_coord, "concrete", 1)
        for generator_coord in self.places_for_generators:
            self.change_tiles_around_point(generator_coord, "concrete", 0)

    def change_tiles_around_point(self, coord, new_type, radius):
    # change type of tiles around point inside radius
        x_id, y_id = self.world2id(coord)
        list_with_tiles = self.get_list_with_tiles_around([x_id, y_id], radius)
        for tile_ids in list_with_tiles:
            x_id, y_id = tile_ids
            if self.BOARD[y_id][x_id].type == "submerged_concrete": depth = 2
            else: depth = 0
            self.change_tile_type(x_id, y_id, new_type, depth)

    def get_list_with_tiles_around(self, tile_ids, radius):
    # return list with ids ot tiles around point inside radius
        coord = self.id2world(tile_ids)
        radius_in_pixels = radius * self.inner_tile_radius * 2 + 1
        list_with_tiles = []
        for y in range(self.map_height):
            for x in range(self.map_width):
                checked_tile_coord = self.id2world((x, y))
                if math.hypot(coord[0]-checked_tile_coord[0], coord[1]-checked_tile_coord[1]) < radius_in_pixels:
                    list_with_tiles.append([x, y])
        return list_with_tiles

    def change_tile_type(self, x_id, y_id, new_type, depth=0):
    # change type of tile
        if 0 <= x_id and x_id < self.map_width and 0 <= y_id  and y_id < self.map_height:
            self.BOARD[y_id][x_id].set_type(new_type, depth)

    def change_tile_type_during_simulation(self, x_id, y_id, new_type, depth=0):
    # change type of tile during simulation
        self.change_tile_type(x_id, y_id, new_type, depth)

    def get_tile_type(self, coord):
    # return the tile type
        x_id, y_id = self.world2id(coord)
        if 0 <= x_id and x_id < self.map_width and 0 <= y_id and y_id < self.map_height:
            return self.BOARD[y_id][x_id].type
        else: return "out_of_map"

    def get_tile_degradation_level(self, coord):
    # return the tile degradation level
        x_id, y_id = self.world2id(coord)
        if 0 <= x_id and x_id < self.map_width and 0 <= y_id and y_id < self.map_height:
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
    def __init__(self, map_width, map_height, type="snow_plain", tile_edge_length=25, clean=False, forest_on=False):
    # initialization of the map
        Map.__init__(self, map_width, map_height, type, tile_edge_length, clean, forest_on=forest_on)

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

    def change_tile_type_during_simulation(self, x_id, y_id, new_type, depth=0):
    # change type of tile during simulation
        if 0 <= x_id  and x_id < self.map_width and 0 <= y_id  and y_id < self.map_height:
            self.BOARD[y_id][x_id].set_type(new_type, depth)
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