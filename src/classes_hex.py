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

        self.is_on_screen = True

        self.color = [MARS_RED[0] - random.randint(0, 20), MARS_RED[1] + random.randint(0, 20), MARS_RED[2]]
        self.degradation_level = 0

    def draw(self, win):
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

    def degrade(self, level):
    # degrade the tile - it will be darker

        if self.degradation_level < level:
            self.degradation_level += 1

            r, g, b = self.color
            r -= 20
            g -= 20
            b -= 20
            if r < 0: r = 0
            if g < 0: g = 0
            if b < 0: b = 0
            self.color = [r, g, b]
            # for i_rgb in range(3):
            #     self.color[i_rgb] = 20

            # self.color = BLUE


class HexTile_v2(HexTile):
    def __init__(self, coord_id, coord_world, edge_length):
    # initialization of the HexTile
        HexTile.__init__(self, coord_id, coord_world, edge_length)
        self.color = [SNOW_WHITE[0] - random.randint(0, 40), SNOW_WHITE[1] - random.randint(0, 10), SNOW_WHITE[2] - random.randint(0, 5)]

    def draw(self, win, scale):
    # draw the HexTile on the screen
        corners = self.compute_corners([self.coord_world[0] * scale, self.coord_world[1] * scale], self.edge_length_world * scale)
        pygame.draw.polygon(win, self.color, corners)


# class HexTile_v3(HexTile):

#     def __init__(self, coord_id, coord_world, edge_length):
#     # initialization of the HexTile
#         HexTile.__init__(self, coord_id, coord_world, edge_length)

#         self.width = self.edge_length_world * SQRT3 + 1
#         self.height = 2 * self.edge_length_world + 1

#         # load and prepare sprite
#         self.sprite = pygame.Surface([self.width, self.height])
#         self.sprite.fill(BLACK)
#         self.sprite.convert()
#         self.sprite.set_colorkey(BLACK)

#         self.color = [SNOW_WHITE[0] - random.randint(0, 40), SNOW_WHITE[1] - random.randint(0, 10), SNOW_WHITE[2] - random.randint(0, 5)]

#         self.sprite_update()

#         # # load and prepare sprite
#         # self.sprite = pygame.image.load(os.path.join(*self.path))

#     def draw(self, win, offset_x, offset_y, scale):
#     # draw the HexTile on the screen
#         if self.is_on_screen:
#             scaled_image = pygame.transform.scale(self.sprite, (scale * self.width, scale * self.height))
#             # new_rect = scaled_image.get_rect(center = world2screen(self.coord_screen, offset_x, offset_y, scale))
#             new_rect = scaled_image.get_rect(center = self.coord_screen)
#             win.blit(scaled_image, new_rect.topleft)
    
#     def sprite_update(self):
#     # draw the HexTile on the sprite surface
#         # corners_sprite = self.compute_corners([self.edge_length_world * SQRT3 / 2, self.edge_length_world], self.edge_length_world)
#         corners_sprite = [
#                 (self.width / 2, 0),
#                 (self.width, self.edge_length_world / 2),
#                 (self.width, self.edge_length_world * 3 / 2),
#                 (self.width / 2, self.height),
#                 (0, self.edge_length_world * 3 / 2),
#                 (0, self.edge_length_world / 2),
#             ]
#         pygame.draw.polygon(self.sprite, self.color, corners_sprite)

#     def update_screen_corners(self, offset_x, offset_y, scale = 1):
#     # update the hexagon's corners' coordinates in screen coordinate system
#         self.coord_screen = world2screen(self.coord_world, offset_x, offset_y, scale)  

#         margin = self.edge_length_world * scale
#         x, y = self.coord_screen
#         if x < -margin or y < -margin or x > WIN_WIDTH+margin or y > WIN_HEIGHT+margin:
#             self.is_on_screen = False
#         else:
#             # self.corners_screen = self.compute_corners(self.coord_screen, self.edge_length_world * scale)
#             self.is_on_screen = True

#     def degrade(self, level):
#     # degrade the tile - it will be darker
#         HexTile.degrade(self, level)
#         self.sprite_update()
