# Tomasz Empire RTS 2022
# By Tomasz Golaszewski
# 10.2022

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
from functions_graphics import *
from functions_test import *
from functions_other import *
from classes_map import *
from classes_units import *

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

    # window variables
    OFFSET_VERTICAL = 150
    OFFSET_HORIZONTAL = 200
    SCALE = 0.5
    SHOW_EXTRA_DATA = False # True
    SHOW_HP_BARS = True

    left_mouse_button_down = False

    # initialize the game
    size = "L"
    type_of_map = "island" # "lake" "bridge" "island" "noise" "forest" "snow_forest"

    if size == "S": dimensions = (30, 40)
    elif size == "M": dimensions = (45, 75)
    elif size == "L": dimensions = (80, 100)
    elif size == "XL": dimensions = (120, 150)
    elif size == "XXL": dimensions = (150, 200)

    # MAP = Map(40, 60, tile_edge_length=30)
    # MAP2 = Map_v2(5, 10, tile_edge_length=30)
    MAP2 = Map_v2(*dimensions, type=type_of_map)

    LIST_WITH_UNITS = make_test_units()
    # LIST_WITH_UNITS = [Light_tank([500, 300], math.pi/2, 1, 1)]
    LIST_WITH_BULLETS = []


# main loop
    running = True
    while running:
        CLOCK.tick(FRAMERATE)
        CURRENT_FRAME += 1
        if CURRENT_FRAME == FRAMERATE:
            CURRENT_FRAME = 0

            # print empty line
            print()

            # print infos about fps and time
            print("FPS: %.2f" % CLOCK.get_fps(), end="\t")
            print("TIME: " + str(pygame.time.get_ticks() // 1000))

            # print infos about view position
            print("HORIZ:", end=" ")
            print(OFFSET_HORIZONTAL, end="\t")
            print("VERT:", end=" ")
            print(OFFSET_VERTICAL, end="\t")
            print("SCALE:", end=" ")
            print(SCALE)

            # print infos about amount of objects
            print("BULLETS:", end=" ")
            print(len(LIST_WITH_BULLETS), end="\t")
            print("UNITS:", end=" ")
            print(len(LIST_WITH_UNITS))

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
                    left_mouse_button_down = True

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
                    set_new_target(LIST_WITH_UNITS, screen2world(pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE), keys_pressed[pygame.K_LCTRL])

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
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    running = False
                    pygame.quit()
                    quit()
                # center
                if event.key == pygame.K_c:
                    OFFSET_HORIZONTAL = 100
                    OFFSET_VERTICAL = 100
                    SCALE = 1
                # show extra data
                if event.key == pygame.K_m:
                    if SHOW_EXTRA_DATA: SHOW_EXTRA_DATA = False
                    else: SHOW_EXTRA_DATA = True
                # show HP bars
                if event.key == pygame.K_h:
                    if SHOW_HP_BARS: SHOW_HP_BARS = False
                    else: SHOW_HP_BARS = True

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

        # life-cycles of bullets
        for bullet in LIST_WITH_BULLETS:
            bullet.run(MAP2, LIST_WITH_UNITS)

        # life-cycles of units
        for unit in LIST_WITH_UNITS:
            unit.run(MAP2, LIST_WITH_UNITS, LIST_WITH_BULLETS)
        

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
            for unit in LIST_WITH_UNITS:
                unit.draw_extra_data(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)

        # draw land and naval units
        for unit in LIST_WITH_UNITS:
            if unit.unit_type == "land" or unit.unit_type == "navy": unit.draw(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)

        # draw air units
        for unit in LIST_WITH_UNITS:
            if unit.unit_type == "air": unit.draw(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)

        # show HP bars
        if SHOW_HP_BARS and SCALE >= 1:
            for unit in LIST_WITH_UNITS:
                unit.draw_HP(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)

        # draw bullets
        for bullet in LIST_WITH_BULLETS:
            bullet.draw(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)


# draw UI

        # draw selection
        if left_mouse_button_down:
            unit_selection(WIN, LIST_WITH_UNITS, left_mouse_button_coord, pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE, -1)


# flip the screen
        pygame.display.update()


# clear dead elements

        # dead bullets
        remove_few_dead_elements(LIST_WITH_BULLETS)
        # LIST_WITH_BULLETS = remove_many_dead_elements(LIST_WITH_BULLETS)

        # dead units
        remove_few_dead_elements(LIST_WITH_UNITS)
    

if __name__ == "__main__":
    run()

