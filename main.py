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
from classes_map import *


def run():
# main function - runs the game
    
    # initialize the pygame
    pygame.init()
    pygame.display.set_caption("Trains 2022")
    ICON_IMGS = pygame.image.load(ICON_PATH)
    pygame.display.set_icon(ICON_IMGS)
    WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    CLOCK = pygame.time.Clock()
    CURRENT_FRAME = 0

    # window variables
    OFFSET_VERTICAL = 0
    OFFSET_HORIZONTAL = 90
    SCALE = 1

    # initialize the game
    MAP = Map(50, 50, 10)
    MAP.BOARD[1][10].color = BLUE

# main loop
    running = True
    while running:
        CLOCK.tick(FRAMERATE)
        CURRENT_FRAME += 1
        if CURRENT_FRAME == FRAMERATE:
            CURRENT_FRAME = 0
            print("FPS: %.2f" % CLOCK.get_fps(), end="\t")
            print("TIME: " + str(pygame.time.get_ticks() // 1000))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

 # mouse
            if event.type == pygame.MOUSEBUTTONUP:
                # 1 - left click
                if event.button == 1:
                    pass
                    # running = False
                    # pygame.quit()
                    # quit()

                # 2 - middle click
                if event.button == 2:
                    # define new view center
                    mouse_pos = pygame.mouse.get_pos()
                    OFFSET_HORIZONTAL -= (mouse_pos[0] - WIN_WIDTH/2) / SCALE
                    OFFSET_VERTICAL -= (mouse_pos[1] - WIN_HEIGHT/2) / SCALE

                # 3 - right click
                if event.button == 3:
                    pass

                # 4 - scroll up
                if event.button == 4:

                    old_scale = SCALE
                    # mouse_pos = pygame.mouse.get_pos()

                    SCALE += 0.25
                    # if SCALE == 1.5: SCALE = 1
                    # elif SCALE == 1.25: SCALE = 0.5
                    if SCALE >= 3: SCALE = 3

                    if old_scale - SCALE:
                        # OFFSET_HORIZONTAL -= mouse_pos[0] / old_scale - WIN_WIDTH/2 / SCALE
                        # OFFSET_VERTICAL -= mouse_pos[1] / old_scale - WIN_HEIGHT/2 / SCALE
                        OFFSET_HORIZONTAL -= WIN_WIDTH/2 / old_scale - WIN_WIDTH/2 / SCALE
                        OFFSET_VERTICAL -= WIN_HEIGHT/2 / old_scale - WIN_HEIGHT/2 / SCALE

                # 5 - scroll down
                if event.button == 5:

                    old_scale = SCALE
                    mouse_pos = pygame.mouse.get_pos()

                    SCALE -= 0.25
                    # if SCALE == 0: SCALE = 0.5
                    # elif SCALE == -0.5: SCALE = 0.25
                    if SCALE <= 0: SCALE = 0.25

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

# keys that can be pressed multiple times
        keys_pressed=pygame.key.get_pressed()
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
        # center
        if keys_pressed[pygame.K_c]:
            OFFSET_HORIZONTAL = 100
            OFFSET_VERTICAL = 100
            SCALE = 1

# run the simulation
        

# draw the screen

        # clear screen
        WIN.fill(BLACK)

        # calculate new position of the map on the screen
        MAP.update_screen_corners(OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)
        # draw the map
        MAP.draw(WIN)

        # flip the screen
        pygame.display.update()
    

if __name__ == "__main__":
    run()

