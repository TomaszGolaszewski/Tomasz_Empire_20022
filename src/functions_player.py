# from settings import *
from setup import *
from functions_graphics import *
from functions_math import *


def calculate_score(dict_with_game_state, dict_with_units):
# calculate current score for each player
    dict_with_game_state["list_with_score"] = [0, 0, 0, 0, 0]
    for unit_id in dict_with_units:
        if dict_with_units[unit_id].is_alive:
            dict_with_game_state["list_with_score"][dict_with_units[unit_id].player_id] += dict_with_units[unit_id].price


def calculate_energy(dict_with_game_state):
# calculate current energy production for each player
    for i in range(1,5):
        dict_with_game_state["list_with_energy_current_production"][i] = dict_with_game_state["list_with_energy"][i] - dict_with_game_state["list_with_energy_last"][i]
    dict_with_game_state["list_with_energy_last"] = dict_with_game_state["list_with_energy"].copy()


def draw_infos_about_players(win, font, dict_with_game_state):
# write information about the energy processed by players on the screen 
    for player in range(1,5):
        text_line = font.render("PLAYER %d [%s]: %d (%d/s)" % (
                    player,
                    dict_with_game_state["list_with_player_type"][player],
                    # dict_with_game_state["list_with_energy"][player], 
                    # dict_with_game_state["list_with_energy_last"][player], 
                    dict_with_game_state["list_with_score"][player],
                    dict_with_game_state["list_with_energy_current_production"][player]
                ), True, player_color(player))
        win.blit(text_line, (WIN_WIDTH - 260, 25 * player - 15))
    

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
    elif player_id == 4:
        return YELLOW
    else: return WHITE


def unit_selection(win, dict_with_units, corner1, corner2, offset_x, offset_y, scale, player_id):
# draw selection rectangle, then set units to selection mode
# return number of selected units

    def unit_selection_by_type(unit_type):
    # help tool to select units by type
    # return number of selected units
        is_some_unit_selected = False
        for unit_id in dict_with_units:
            if (player_id == -1 or dict_with_units[unit_id].player_id == player_id) \
                        and dict_with_units[unit_id].unit_type == unit_type \
                        and rect.collidepoint(world2screen(dict_with_units[unit_id].coord, offset_x, offset_y, scale)):
                dict_with_units[unit_id].is_selected = True
                is_some_unit_selected = True
            else:
                dict_with_units[unit_id].is_selected = False
        return is_some_unit_selected

    rect = set_rectangle_with_two_corners(corner1, corner2)

    # TODO: fix selection is point
    # if selection is point
    if dist_two_points(corner1, corner2) < 5:
        point = screen2world(corner1, offset_x, offset_y, scale)
        for unit_id in dict_with_units:
            if (player_id == -1 or dict_with_units[unit_id].player_id == player_id) and dist_two_points(point, dict_with_units[unit_id].coord) < dict_with_units[unit_id].hit_box_radius:
                dict_with_units[unit_id].is_selected = True
            else:
                dict_with_units[unit_id].is_selected = False

    # if selection is rectangle
    else:
        # priority of selection: air > land > navy > building
        is_air_selected = unit_selection_by_type("air")
        if not is_air_selected: 
            is_land_selected = unit_selection_by_type("land")
            if not is_land_selected: 
                is_navy_selectes = unit_selection_by_type("navy")
                if not is_navy_selectes: unit_selection_by_type("building")

    pygame.draw.rect(win, LIME, rect, 3)

    # count selected units
    result = 0
    for unit_id in dict_with_units:
        if dict_with_units[unit_id].is_selected: result += 1
    return result


def set_new_target_factory(map, dict_with_units, target, is_ctrl_down):
# set new movement target for units to all selected factories
    number_of_selected_units = 0
    # search search through the list with units
    for unit_id in dict_with_units:
        if dict_with_units[unit_id].is_selected:
            number_of_selected_units += 1
            if is_ctrl_down:
                dict_with_units[unit_id].target_for_units.append(target)
            else:
                dict_with_units[unit_id].target_for_units = [target]


def set_new_target_move(map, dict_with_units, target, is_ctrl_down):
# set new movement target to all selected units
# units will move in original arrangement
    number_of_selected_units = 0
    # biggest_unit_radius = 0
    slowest_unit_speed = 100
    top_left = 99999
    top_right = -99999
    top_top = 99999
    top_bottom = -99999
    # search search through the list with units
    for unit_id in dict_with_units:
        if dict_with_units[unit_id].is_selected:
            number_of_selected_units += 1
            # if unit.body_radius > biggest_unit_radius: biggest_unit_radius = unit.body_radius
            if dict_with_units[unit_id].v_max < slowest_unit_speed: slowest_unit_speed = dict_with_units[unit_id].v_max
            if dict_with_units[unit_id].coord[0] < top_left: top_left = dict_with_units[unit_id].coord[0]
            if dict_with_units[unit_id].coord[0] > top_right: top_right = dict_with_units[unit_id].coord[0]
            if dict_with_units[unit_id].coord[1] < top_top: top_top = dict_with_units[unit_id].coord[1]
            if dict_with_units[unit_id].coord[1] > top_bottom: top_bottom = dict_with_units[unit_id].coord[1]
    
    coord_of_squad = [top_left + (top_right - top_left) / 2, top_top + (top_bottom - top_top) / 2]
    translation_vector = [target[0] - coord_of_squad[0], target[1] - coord_of_squad[1]]

    # set new target
    for unit_id in dict_with_units:
        if dict_with_units[unit_id].is_selected:
            new_target = [dict_with_units[unit_id].coord[0] + translation_vector[0], dict_with_units[unit_id].coord[1] + translation_vector[1]]
            if is_ctrl_down:
                dict_with_units[unit_id].set_new_target(new_target)
            else:
                dict_with_units[unit_id].set_new_target(new_target, overwrite=True)

            # when only first segment of movement target is changed
            if len(dict_with_units[unit_id].base.movement_target) == 1: 
                dict_with_units[unit_id].set_new_path_with_path_checking(map, new_target)

            dict_with_units[unit_id].set_v_max_squad(slowest_unit_speed)


def set_new_target_regroup(map, dict_with_units, target, is_ctrl_down):
# set new movement target to all selected units
# units will regroup into spiral
    number_of_selected_units = 0
    current_unit = 0
    biggest_unit_radius = 0
    slowest_unit_speed = 100
    # search search through the list with units
    for unit_id in dict_with_units:
        if dict_with_units[unit_id].is_selected:
            number_of_selected_units += 1
            if dict_with_units[unit_id].body_radius > biggest_unit_radius: biggest_unit_radius = dict_with_units[unit_id].body_radius
            if dict_with_units[unit_id].v_max < slowest_unit_speed: slowest_unit_speed = dict_with_units[unit_id].v_max

    # set new target
    for unit_id in dict_with_units:
        if dict_with_units[unit_id].is_selected:
            new_unit_target = get_coord_on_spiral(current_unit, target, 5 * biggest_unit_radius)
            if is_ctrl_down:
                dict_with_units[unit_id].set_new_target(new_unit_target)
            else:
                dict_with_units[unit_id].set_new_target(new_unit_target, overwrite=True)

            # when only first segment of movement target is changed
            if len(dict_with_units[unit_id].base.movement_target) == 1:
                dict_with_units[unit_id].set_new_path_with_path_checking(map, new_unit_target)
                
            dict_with_units[unit_id].set_v_max_squad(slowest_unit_speed)
            current_unit += 1


def get_coord_on_spiral(unit_n, center, step_size):
# return coord of unit_n-th unit on spiral

    # set up spiral
    x = center[0]
    y = center[1]
    current_n = 1
    direction = 0
    turn_counter = 0
    steps_in_line = 1

    while current_n <= unit_n:
        # move according to direction
        if direction == 0:
            x += step_size
        elif direction == 1:
            y -= step_size
        elif direction == 2:
            x -= step_size
        elif direction == 3:
            y += step_size

        # change direction
        if current_n % steps_in_line == 0:
            direction += 1
            if direction == 4: direction = 0
            turn_counter += 1
            if turn_counter % 2:
                steps_in_line += 1

        # next number
        current_n += 1

    return (x, y)


def center_view_on_commander(dict_with_units, scale, player_id):
    for unit_id in dict_with_units:
        if dict_with_units[unit_id].player_id == player_id \
                    and dict_with_units[unit_id].name == "Commander":
            x, y = dict_with_units[unit_id].coord 
            return -x + WIN_WIDTH // scale // 2, -y + WIN_HEIGHT // scale // 2
