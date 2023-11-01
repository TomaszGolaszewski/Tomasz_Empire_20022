# Tomasz Empire RTS 2022
# By Tomasz Golaszewski
# 10.2022 - 12.2023

# 

import pygame
import time
import os

from sys import path

# check the system and add files to path
if os.name == "posix":
    path.append('./src')
    print("Linux")
elif os.name == "nt":
    path.append('.\\src')
    print("Windows")
else:
    path.append('.\\src')
    print("other")

from settings import *
from setup import *
from functions_graphics import *
from functions_make_units import *
from functions_test import *
from functions_windows import *
from functions_other import *
from classes_map import *
from classes_units import *
from classes_buildings import *
from classes_ui import *
from classes_base import *


def run():
# main function - runs the game
    
    # initialize the pygame
    pygame.init()
    pygame.display.set_caption("Tomasz Empire 20022")
    ICON_IMGS = pygame.image.load(os.path.join(*ICON_PATH))
    pygame.display.set_icon(ICON_IMGS)
    WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    CLOCK = pygame.time.Clock()
    CURRENT_FRAME = 0
    CURRENT_FPS = 0

    # fonts
    FONT_ARIAL_20 = pygame.font.SysFont('arial', 20)
    FONT_ARIAL_30 = pygame.font.SysFont('arial', 30)

    # window variables
    SCALE = 0.5
    SHOW_EXTRA_DATA = False
    SHOW_MOVEMENT_TARGET = False
    SHOW_HP_BARS = True

    left_mouse_button_down = False
    right_mouse_button_down = False
    number_of_selected_units = 0

    # initialize the game
    PLAYER_ID = 3
    size = "L"
    type_of_map = "island" # "mars_poles" "lake" "bridge" "island" "noise" "forest" "snow_forest"

    if size == "S": dimensions = (30, 40)
    elif size == "M": dimensions = (45, 75)
    elif size == "L": dimensions = (80, 100)
    elif size == "XL": dimensions = (120, 150)
    elif size == "XXL": dimensions = (150, 200)
    elif size == "width": dimensions = (120, 75)

    # MAP = Map(40, 60, tile_edge_length=30)
    # MAP2 = Map_v2(5, 10, tile_edge_length=30)
    MAP2 = Map_v2(*dimensions, type=type_of_map)

    DICT_WITH_GAME_STATE = {
        "lowest_free_id": 1,
        "list_with_score": [0, 0, 0, 0, 0],
        "list_with_energy": [0, 10000, 10000, 10000, 10000],
        "list_with_energy_last": [0, 10000, 10000, 10000, 10000], # [0, 0, 0, 0, 0],
        "list_with_energy_current_production": [0, 0, 0, 0, 0],
        "list_with_energy_spent": [0, 0, 0, 0, 0],
        # "list_with_player_type": [False, "AI", "AI", "AI", "AI"],
        "list_with_player_type": [False, "AI", "AI", "player", "AI"],
        # "list_with_player_type": [False, "empty", "AI", "player", "empty"],
        # "list_with_player_type": [False, "empty", "empty", "player", "empty"],
        "dict_with_new_units": {},
    }
    DICT_WITH_GAME_STATE["list_with_player_type"][PLAYER_ID] = "player"

    DICT_WITH_UNITS = {}
    # make_test_units(DICT_WITH_GAME_STATE, DICT_WITH_UNITS)
    # make_test_units_2(DICT_WITH_GAME_STATE, DICT_WITH_UNITS)
    make_naval_factories(MAP2, DICT_WITH_GAME_STATE, DICT_WITH_UNITS)
    make_land_factories(MAP2, DICT_WITH_GAME_STATE, DICT_WITH_UNITS)
    make_generators(MAP2, DICT_WITH_GAME_STATE, DICT_WITH_UNITS)
    make_start_units(MAP2, DICT_WITH_GAME_STATE, DICT_WITH_UNITS)
    OFFSET_HORIZONTAL, OFFSET_VERTICAL = center_view_on_commander(DICT_WITH_UNITS, SCALE, PLAYER_ID)

    LIST_WITH_BULLETS = []
    LIST_WITH_WINDOWS = []

# main loop
    running = True
    pause = False
    while running:
        CLOCK.tick(FRAMERATE)
        CURRENT_FRAME += 1
        if CURRENT_FRAME == FRAMERATE:
            CURRENT_FRAME = 0

            # print empty line
            print()

            # print infos about fps and time
            CURRENT_FPS = CLOCK.get_fps()
            print("FPS: %.2f" % CURRENT_FPS, end="\t")
            seconds_from_start = pygame.time.get_ticks() // 1000
            minuts_from_start = seconds_from_start // 60
            print("TIME: " + str(seconds_from_start) + "s (" + str(minuts_from_start) + "min)" )

            print_infos_about_view_position(OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)
            print_infos_about_amount_of_objects(DICT_WITH_GAME_STATE, DICT_WITH_UNITS, LIST_WITH_BULLETS, LIST_WITH_WINDOWS)
            
            # calculate energy
            if not pause:
                calculate_energy(DICT_WITH_GAME_STATE)
                calculate_score(DICT_WITH_GAME_STATE, DICT_WITH_UNITS)

            # print_infos_about_players(DICT_WITH_GAME_STATE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

# mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 1 - left click
                if event.button == 1:
                    left_mouse_button_coord = pygame.mouse.get_pos()
                    left_mouse_button_down = False
                    
                    # press UI windows (based on notebooks)
                    for ui_win in LIST_WITH_WINDOWS:
                        left_mouse_button_down |= ui_win.press_left(DICT_WITH_GAME_STATE, DICT_WITH_UNITS, left_mouse_button_coord)

                    left_mouse_button_down = not left_mouse_button_down

                # 3 - right click
                if event.button == 3:
                    right_mouse_button_coord = pygame.mouse.get_pos()
                    make_windows_from_right_mouse_button(DICT_WITH_UNITS, LIST_WITH_WINDOWS, right_mouse_button_coord, \
                                                screen2world(right_mouse_button_coord, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE))

# mouse button up
            if event.type == pygame.MOUSEBUTTONUP:
                # 1 - left click
                if event.button == 1:
                    left_mouse_button_down = False

                # 2 - middle click
                if event.button == 2:
                    # define new view center
                    mouse_pos = pygame.mouse.get_pos()
                    OFFSET_HORIZONTAL -= (mouse_pos[0] - WIN_WIDTH/2) / SCALE
                    OFFSET_VERTICAL -= (mouse_pos[1] - WIN_HEIGHT/2) / SCALE

                # 3 - right click
                if event.button == 3:
                    # set new movement target
                    keys_pressed = pygame.key.get_pressed()

                    # press UI windows (based on slide)
                    for ui_win in LIST_WITH_WINDOWS:
                        ui_win.press_right(MAP2, DICT_WITH_UNITS, pygame.mouse.get_pos(), keys_pressed[pygame.K_LCTRL])

                # 4 - scroll up
                if event.button == 4:
                    old_scale = SCALE
                    # mouse_pos = pygame.mouse.get_pos()

                    SCALE *= 2
                    if SCALE >= 4: SCALE = 4

                    if old_scale - SCALE:
                        # OFFSET_HORIZONTAL -= mouse_pos[0] / old_scale - WIN_WIDTH/2 / SCALE
                        # OFFSET_VERTICAL -= mouse_pos[1] / old_scale - WIN_HEIGHT/2 / SCALE
                        OFFSET_HORIZONTAL -= WIN_WIDTH/2 / old_scale - WIN_WIDTH/2 / SCALE
                        OFFSET_VERTICAL -= WIN_HEIGHT/2 / old_scale - WIN_HEIGHT/2 / SCALE

                # 5 - scroll down
                if event.button == 5:
                    old_scale = SCALE
                    # mouse_pos = pygame.mouse.get_pos()

                    SCALE /= 2
                    # if SCALE <= 0.25: SCALE = 0.25
                    if SCALE <= 0.125: SCALE = 0.125

                    if old_scale - SCALE:
                        # OFFSET_HORIZONTAL -= mouse_pos[0] / old_scale - WIN_WIDTH/2 / SCALE
                        # OFFSET_VERTICAL -= mouse_pos[1] / old_scale - WIN_HEIGHT/2 / SCALE
                        OFFSET_HORIZONTAL -= WIN_WIDTH/2 / old_scale - WIN_WIDTH/2 / SCALE
                        OFFSET_VERTICAL -= WIN_HEIGHT/2 / old_scale - WIN_HEIGHT/2 / SCALE


# keys that can be pressed only ones
            if event.type == pygame.KEYDOWN:
                # manual close
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN: # or event.key == pygame.K_q:
                    running = False
                    pygame.quit()
                    quit()
                # pause
                if event.key == pygame.K_SPACE:
                    if pause: pause = False
                    else: pause = True
                # center
                if event.key == pygame.K_c:
                    SCALE = 1
                    OFFSET_HORIZONTAL, OFFSET_VERTICAL = center_view_on_commander(DICT_WITH_UNITS, SCALE, PLAYER_ID)
                # show extra data
                if event.key == pygame.K_m:
                    if SHOW_EXTRA_DATA: SHOW_EXTRA_DATA = False
                    else: SHOW_EXTRA_DATA = True
                # show movement target
                if event.key == pygame.K_q:
                    if SHOW_MOVEMENT_TARGET: SHOW_MOVEMENT_TARGET = False
                    else: SHOW_MOVEMENT_TARGET = True
                # show HP bars
                if event.key == pygame.K_h:
                    if SHOW_HP_BARS: SHOW_HP_BARS = False
                    else: SHOW_HP_BARS = True
                # cheat/debuging tool - give extra energy
                if event.key == pygame.K_g:
                    DICT_WITH_GAME_STATE["list_with_energy"][PLAYER_ID] += 100000

# keys that can be pressed multiple times
        keys_pressed = pygame.key.get_pressed()
        # move
        move_speed = 5 / SCALE
        # move left
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            OFFSET_HORIZONTAL += move_speed
        # move right
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            OFFSET_HORIZONTAL -= move_speed
        # move up
        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            OFFSET_VERTICAL += move_speed
        # move down
        if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            OFFSET_VERTICAL -= move_speed


# run the simulation
        if not pause:
            # life-cycles of units AI
            for unit_id in DICT_WITH_UNITS:
                DICT_WITH_UNITS[unit_id].AI_run(MAP2, DICT_WITH_GAME_STATE, DICT_WITH_UNITS)

            # life-cycles of bullets
            for bullet in LIST_WITH_BULLETS:
                bullet.run(MAP2, DICT_WITH_UNITS)

            # life-cycles of units
            for unit_id in DICT_WITH_UNITS:
                DICT_WITH_UNITS[unit_id].run(MAP2, DICT_WITH_GAME_STATE, DICT_WITH_UNITS, LIST_WITH_BULLETS)
        

# draw the screen

        # clear screen
        WIN.fill(BLACK)

        # calculate new position of the map on the screen
        # MAP.update_screen_corners(OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)
        # draw the map
        # MAP.draw(WIN)
        MAP2.draw(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)

        # show extra data
        if SHOW_EXTRA_DATA:
            for unit_id in DICT_WITH_UNITS:
                DICT_WITH_UNITS[unit_id].draw_extra_data(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)

        # show movement target
        if SHOW_MOVEMENT_TARGET:
            for unit_id in DICT_WITH_UNITS:
                if DICT_WITH_UNITS[unit_id].player_id == PLAYER_ID:
                    DICT_WITH_UNITS[unit_id].draw_movement_target(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)

        # draw land and naval units
        for unit_id in DICT_WITH_UNITS:
            if DICT_WITH_UNITS[unit_id].unit_type == "land" or \
                        DICT_WITH_UNITS[unit_id].unit_type == "navy" or \
                        DICT_WITH_UNITS[unit_id].unit_type == "building": 
                DICT_WITH_UNITS[unit_id].draw(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)

        # draw air units
        for unit_id in DICT_WITH_UNITS:
            if DICT_WITH_UNITS[unit_id].unit_type == "air": 
                DICT_WITH_UNITS[unit_id].draw(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)

        # show HP bars
        if SHOW_HP_BARS and SCALE >= 1:
            for unit_id in DICT_WITH_UNITS:
                DICT_WITH_UNITS[unit_id].draw_HP(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)

        # draw bullets
        for bullet in LIST_WITH_BULLETS:
            bullet.draw(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)


# draw UI
        # draw selection
        if left_mouse_button_down: # and not len(LIST_WITH_WINDOWS):
            # number_of_selected_units = 
            unit_selection(WIN, DICT_WITH_UNITS, left_mouse_button_coord, pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE, -1)
        else:
            make_windows_from_dict_with_units(DICT_WITH_UNITS, LIST_WITH_WINDOWS)

        # draw UI windows
        for ui_win in LIST_WITH_WINDOWS:
            ui_win.draw(WIN, DICT_WITH_GAME_STATE, DICT_WITH_UNITS)

        # draw infos about players
        draw_infos_about_players(WIN, FONT_ARIAL_20, DICT_WITH_GAME_STATE)

        # draw player's energy
        text = FONT_ARIAL_30.render("E: %d" % DICT_WITH_GAME_STATE["list_with_energy"][PLAYER_ID], True, player_color(PLAYER_ID))
        WIN.blit(text, (WIN_WIDTH//2 - 50, 10))

        # draw FPS     
        text = FONT_ARIAL_20.render("FPS: %.2f" % CURRENT_FPS, True, LIME)
        WIN.blit(text, (10, 10))

        # draw pause
        if pause:
            text_pause = FONT_ARIAL_20.render("[PAUSE]", True, LIME)
            WIN.blit(text_pause, (10, 30))
            WIN.blit(text_pause, (WIN_WIDTH//2 - 25, 40))


# flip the screen
        pygame.display.update()


# clear dead elements

        # dead bullets
        remove_few_dead_elements_from_list(LIST_WITH_BULLETS)
        # LIST_WITH_BULLETS = remove_many_dead_elements(LIST_WITH_BULLETS)

        # dead units
        remove_dead_elements_from_dict(DICT_WITH_UNITS)

        # unnecessary UI windows
        remove_few_dead_elements_from_list(LIST_WITH_WINDOWS)

# add new units - move new units form DICT_WITH_GAME_STATE["dict_with_new_units"] to DICT_WITH_UNITS
        DICT_WITH_UNITS |= DICT_WITH_GAME_STATE["dict_with_new_units"]
        DICT_WITH_GAME_STATE["dict_with_new_units"] = {}


if __name__ == "__main__":
    run()

