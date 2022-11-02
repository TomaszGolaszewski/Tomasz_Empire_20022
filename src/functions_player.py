from settings import *
from functions_graphics import *
from functions_math import *


def player_color(player_id):
# return player color
    if player_id == 0:
        return BLACK
    elif player_id == 1:
        return BLUE
    elif player_id == 2:
        return GREEN
    elif player_id == 3:
        return RED
    else: return WHITE


def unit_selection(win, list_with_units, corner1, corner2, offset_x, offset_y, scale, player_id):
# draw selection rectangle, then set units to selection mode

    rect = set_rectangle_with_two_corners(corner1, corner2)

    # if selection is point
    if dist_two_points(corner1, corner2) < 5:
        point = screen2world(corner1, offset_x, offset_y, scale)
        for unit in list_with_units:
            if (player_id == -1 or unit.player_id == player_id) and dist_two_points(point, unit.coord) < unit.hit_box_radius:
                unit.is_selected = True
            else:
                unit.is_selected = False

    # if selection is rectangle
    else:
        for unit in list_with_units:
            if (player_id == -1 or unit.player_id == player_id) and rect.collidepoint(world2screen(unit.coord, offset_x, offset_y, scale)):
                unit.is_selected = True
            else:
                unit.is_selected = False

    pygame.draw.rect(win, LIME, rect, 3)


def set_new_target(list_with_units, target, is_ctrl_down):
# set new movement target to all selected units


    # set new target
    for unit in list_with_units:
        if unit.is_selected:
            if is_ctrl_down:
                unit.base.movement_target.append(target)
            else:
                unit.base.movement_target = [target]
