import pygame
import random

# from settings import *
from setup import *
from settings import *
from functions_math import *

class HexTile:
    def __init__(self, coord_id, coord_world, edge_length, type="mars", depth=0):
    # initialization of the HexTile
        self.coord_id = coord_id
        self.coord_world = coord_world
        self.coord_screen = coord_world

        self.edge_length_world = edge_length

        self.corners_world = self.compute_corners(coord_world, edge_length)
        self.corners_screen = self.corners_world.copy()
        self.is_on_screen = True
   
        self.degradation_level = 0
        self.set_type(type, depth)

        # prepare sprite for forests
        if self.type == "forest" or self.type == "snow_forest":
            
            # load and prepare sprite sheet
            sprite_sheet = pygame.image.load(os.path.join(*TREES_PATH))

            # calculate frame size
            sprite_sheet_rect = sprite_sheet.get_rect()
            self.frame_width = sprite_sheet_rect.width // 8
            self.frame_height = sprite_sheet_rect.height

            # prepare sprite for forests
            if self.type == "forest": no_of_frame = 4
            elif self.type == "snow_forest": no_of_frame = 0
            self.sprite = pygame.Surface((self.frame_width, self.frame_height))
            self.sprite.blit(sprite_sheet, (0, 0), ((no_of_frame + random.randint(0,3)) * self.frame_width, 0, self.frame_width, self.frame_height))
            self.sprite.convert()
            self.sprite.set_colorkey(LIME)

    def draw(self, win, scale):
    # draw the HexTile on the screen
        corners = self.compute_corners([self.coord_world[0] * scale, self.coord_world[1] * scale], self.edge_length_world * scale)
        pygame.draw.polygon(win, self.color, corners)

        # draw the tree
        if not self.degradation_level:
            if self.type == "forest" or self.type == "snow_forest":
                scaled_image = pygame.transform.scale(self.sprite, (scale * self.frame_width * 1.1, scale * self.frame_height * 1.1))
                win.blit(scaled_image, [(self.coord_world[0] - self.frame_width // 2) * scale, (self.coord_world[1] - self.frame_height // 2) * scale])

    def draw_only(self, win):
    # draw the HexTile on the screen
        if self.is_on_screen:
            pygame.draw.polygon(win, self.color, self.corners_screen)

    def update_screen_corners(self, offset_x, offset_y, scale = 1):
    # update the hexagon's corners' coordinates in screen coordinate system
        self.coord_screen = world2screen(self.coord_world, offset_x, offset_y, scale)  

        margin = self.edge_length_world * scale
        x, y = self.coord_screen
        if x < -margin or y < -margin or x > WIN_WIDTH+margin or y > WIN_HEIGHT+margin:
            self.is_on_screen = False
        else:
            self.corners_screen = self.compute_corners(self.coord_screen, self.edge_length_world * scale)
            self.is_on_screen = True

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

    def set_type(self, type, depth=0):
    # set color of the tile depending on the type of terrain
        self.type = type
        self.depth = depth
        if type == "mars": self.color = [MARS_RED[0] - random.randint(0, 20), MARS_RED[1] + random.randint(0, 20), MARS_RED[2]]
        elif type == "snow": self.color = [SNOW_WHITE[0] - random.randint(0, 40), SNOW_WHITE[1] - random.randint(0, 10), SNOW_WHITE[2] - random.randint(0, 5)]
        elif type == "sand": self.color = [SAND[0] - random.randint(0, 15), SAND[1] - random.randint(0, 15), SAND[2] - random.randint(0, 15)]
        elif type == "grass": self.color = [GRASS[0], GRASS[1] - random.randint(0, 10), GRASS[2] - random.randint(0, 10)]
        # elif type == "forest": self.color = [GREEN[0], GREEN[1] - random.randint(0, 20), GREEN[2]]
        elif type == "forest": self.color = [GRASS[0], GRASS[1] - random.randint(0, 10) - 10, GRASS[2] - random.randint(0, 10)]
        elif type == "snow_forest": self.color = [SNOW_WHITE[0] - random.randint(0, 40) - 20, SNOW_WHITE[1] - random.randint(0, 10) - 10, SNOW_WHITE[2] - random.randint(0, 5)]
        elif type == "concrete": 
            rand = random.randint(0, 10)
            self.color = [GRAY[0] - rand, GRAY[1] - rand, GRAY[2] - rand]
        elif type == "submerged_concrete":
            rand = random.randint(0, 10)
            # self.color = [GRAY[0] - rand, GRAY[1] - rand, GRAY[2] - rand]
            self.color = [SHALLOW[0]- 4 * depth - rand, SHALLOW[1] - 8 * depth - rand, SHALLOW[2] - 8 * depth - rand] 
        elif type == "water": 
            depth -= 5
            self.color = [WATER[0], WATER[1] - 4 * depth, WATER[2] - 8 * depth]
        elif type == "shallow": 
            self.color = [SHALLOW[0]- 4 * depth, SHALLOW[1] - 8 * depth, SHALLOW[2] - 8 * depth]        
        else: self.color = RED

    def degrade(self, level):
    # degrade the tile - it will be darker
        if self.type != "water" and self.degradation_level < level:
            self.degradation_level += 1

            r, g, b = self.color
            r -= 20
            g -= 20
            b -= 20
            if r < 0: r = 0
            if g < 0: g = 0
            if b < 0: b = 0
            self.color = [r, g, b]
