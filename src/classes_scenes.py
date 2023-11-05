import pygame

from settings import *
from setup import *
# from functions_graphics import *
from functions_make_units import *
from functions_test import *
from functions_windows import *
from functions_other import *
from classes_scenes_features import *
from classes_map import *
# from classes_units import *
# from classes_buildings import *
# from classes_ui import *
# from classes_base import *


class SceneBase:
    def __init__(self):
    # initialization of the scene
        self.next = self
    
    def process_input(self, events, keys_pressed):
    # receive all the events that happened since the last frame
    # handle all received events
        print("not overwritten process_input")

    def update(self):
    # game logic for the scene
        print("not overwritten update")

    def render(self, win):
    # draw scene on the screen
        print("not overwritten render")

    def switch_scene(self, next_scene):
    # change scene
        self.next = next_scene
    
    def terminate(self):
    # close the game by changing scene tu None
        self.switch_scene(None)


# ======================================================================


class TitleScene(SceneBase):
    def __init__(self):
    # initialization of the scene
        SceneBase.__init__(self)
        self.title = FixText((WIN_WIDTH/2, WIN_HEIGHT/2 - 30), "TOMASZ EMPIRE 20022", 70)
        self.subtitle = FixText((WIN_WIDTH/2, WIN_HEIGHT/2 + 20), "Supreme Commander", 40)
        self.start_button = BaseButton((WIN_WIDTH/2, WIN_HEIGHT/2 + 100), "[Start Game]", 30, color=GRAY)
        self.quick_start_button = BaseButton((WIN_WIDTH/2, WIN_HEIGHT/2 + 140), "[Quick Start]", 30, color=GRAY)

        self.ticks = 0
    
    def process_input(self, events, keys_pressed):
    # receive all the events that happened since the last frame
    # handle all received events
        for event in events:
            # keys that can be pressed only ones
            if event.type == pygame.KEYDOWN:
                # move to the next scene
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.switch_scene(ChooseMapScene())
                # quick start
                if event.key == pygame.K_q:
                    self.switch_scene(LoadingScene())

            # mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_coord = pygame.mouse.get_pos()
                # quick start
                if self.quick_start_button.is_inside(mouse_coord):
                    self.switch_scene(LoadingScene())
                # move to the next scene
                else:
                    self.switch_scene(ChooseMapScene())

    def update(self):
    # game logic for the scene
        self.ticks += 1
    
    def render(self, win):
    # draw scene on the screen
        # clear screen
        win.fill(BLACK)
        # print titles and buttons
        self.title.draw(win)
        self.subtitle.draw(win)
        if self.ticks > 3*FRAMERATE:
            self.start_button.draw(win)
            self.quick_start_button.draw(win)


# ======================================================================


class ChooseMapScene(SceneBase):
    def __init__(self):
    # initialization of the scene
        SceneBase.__init__(self)
        self.title = FixText((WIN_WIDTH/2, 100), "Choose map", 70)
        self.start_button = BaseButton((WIN_WIDTH/2, WIN_HEIGHT - 100), "[Start Game]", 30, color=GRAY)
        self.island_button = BaseButton((WIN_WIDTH/2, 200), "[Island]", 30, color=GRAY)

    def process_input(self, events, keys_pressed):
    # receive all the events that happened since the last frame
    # handle all received events
        for event in events:
            # keys that can be pressed only ones
            if event.type == pygame.KEYDOWN:
                # move to the next scene
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.switch_scene(LoadingScene())

            # mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_coord = pygame.mouse.get_pos()
                # move to the next scene
                if self.start_button.is_inside(mouse_coord):
                    self.switch_scene(LoadingScene())
                if self.island_button.is_inside(mouse_coord):
                    global GAME_MAP
                    GAME_MAP = "mars_poles"
                
    def update(self):
    # game logic for the scene
        pass
    
    def render(self, win):
    # draw scene on the screen
        # clear screen
        win.fill(BLACK)
        # print titles and buttons
        self.title.draw(win)
        self.start_button.draw(win)
        self.island_button.draw(win)


# ======================================================================


class LoadingScene(SceneBase):
    def __init__(self):
    # initialization of the scene
        SceneBase.__init__(self)
        self.loading_text = FixText((WIN_WIDTH/2, WIN_HEIGHT/2), "Loading ...", 30)
        self.ticks = 0
    
    def process_input(self, events, keys_pressed):
    # receive all the events that happened since the last frame
    # handle all received events
        pass
        
    def update(self):
    # game logic for the scene
        self.ticks += 1
        # automatically jump to the GameScene after the first cycle
        if self.ticks > 1:
            self.switch_scene(GameScene())
    
    def render(self, win):
    # draw scene on the screen
        # clear screen
        win.fill(BLACK)
        # print loading text
        self.loading_text.draw(win)


# ======================================================================


class GameScene(SceneBase):
    def __init__(self):
    # initialization of the scene
        SceneBase.__init__(self)

        # display variables
        self.scale = 0.5
        self.show_extra_data = False
        self.show_movement_target = False
        self.show_hp_bars = True
        self.pause = False
        self.current_frame = 0

        self.left_mouse_button_down = False
        self.right_mouse_button_down = False
        self.number_of_selected_units = 0
        self.left_mouse_button_coord = pygame.mouse.get_pos()

        # initialize the map
        size = GAME_SIZE
        if size == "S": dimensions = (30, 40)
        elif size == "M": dimensions = (45, 75)
        elif size == "L": dimensions = (80, 100)
        elif size == "XL": dimensions = (120, 150)
        elif size == "XXL": dimensions = (150, 200)
        elif size == "width": dimensions = (120, 75)

        self.map = Map_v2(*dimensions, type=GAME_MAP)

        # initialize information about game
        self.dict_with_game_state = {
            "lowest_free_id": 1,
            "list_with_score": [0, 0, 0, 0, 0],
            "list_with_energy": [0, 10000, 10000, 10000, 10000],
            "list_with_energy_last": [0, 10000, 10000, 10000, 10000],
            "list_with_energy_current_production": [0, 0, 0, 0, 0],
            "list_with_energy_spent": [0, 0, 0, 0, 0],
            "list_with_player_type": [False, *GAME_PLAYERS],
            "dict_with_new_units": {},
        }
        
        self.player_id = self.dict_with_game_state["list_with_player_type"].index("player") \
                                            if "player" in self.dict_with_game_state["list_with_player_type"] else 0
        
        # on-screen infos
        self.pause_text = FixText((WIN_WIDTH/2, 50), "[PAUSE]", 20)
        self.player_energy_text = DynamicText((WIN_WIDTH//2, 25), 
                                            "E: %d" % self.dict_with_game_state["list_with_energy"][self.player_id], 30, 
                                            color=player_color(self.player_id))

        # create initial units
        self.dict_with_units = {}
        make_naval_factories(self.map, self.dict_with_game_state, self.dict_with_units)
        make_land_factories(self.map, self.dict_with_game_state, self.dict_with_units)
        make_generators(self.map, self.dict_with_game_state, self.dict_with_units)
        make_start_units(self.map, self.dict_with_game_state, self.dict_with_units)
        self.offset_horizontal, self.offset_vertical = center_view_on_commander(self.dict_with_units, self.scale, self.player_id)

        self.list_with_bullets = []
        self.list_with_windows = []
    

    def process_input(self, events, keys_pressed):
    # receive all the events that happened since the last frame
    # handle all received events
        for event in events:

            # mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 1 - left click
                if event.button == 1:
                    self.left_mouse_button_coord = pygame.mouse.get_pos()
                    self.left_mouse_button_down = False
                    
                    # press UI windows (based on notebooks)
                    for ui_win in self.list_with_windows:
                        self.left_mouse_button_down |= ui_win.press_left(self.dict_with_game_state, self.dict_with_units, self.left_mouse_button_coord)

                    self.left_mouse_button_down = not self.left_mouse_button_down

                # 3 - right click
                if event.button == 3:
                    right_mouse_button_coord = pygame.mouse.get_pos()
                    make_windows_from_right_mouse_button(self.dict_with_units, self.list_with_windows, right_mouse_button_coord, \
                                                screen2world(right_mouse_button_coord, self.offset_horizontal, self.offset_vertical, self.scale))

            # mouse button up
            if event.type == pygame.MOUSEBUTTONUP:
                # 1 - left click
                if event.button == 1:
                    self.left_mouse_button_down = False

                # 2 - middle click
                if event.button == 2:
                    # define new view center
                    mouse_pos = pygame.mouse.get_pos()
                    self.offset_horizontal -= (mouse_pos[0] - WIN_WIDTH/2) / self.scale
                    self.offset_vertical -= (mouse_pos[1] - WIN_HEIGHT/2) / self.scale

                # 3 - right click
                if event.button == 3:
                    # press UI windows (based on slide)
                    for ui_win in self.list_with_windows:
                        ui_win.press_right(self.map, self.dict_with_units, pygame.mouse.get_pos(), keys_pressed[pygame.K_LCTRL])

                # 4 - scroll up
                if event.button == 4:
                    old_scale = self.scale
                    # mouse_pos = pygame.mouse.get_pos()

                    self.scale *= 2
                    if self.scale >= 4: self.scale = 4

                    if old_scale - self.scale:
                        # OFFSET_HORIZONTAL -= mouse_pos[0] / old_scale - WIN_WIDTH/2 / SCALE
                        # OFFSET_VERTICAL -= mouse_pos[1] / old_scale - WIN_HEIGHT/2 / SCALE
                        self.offset_horizontal -= WIN_WIDTH/2 / old_scale - WIN_WIDTH/2 / self.scale
                        self.offset_vertical -= WIN_HEIGHT/2 / old_scale - WIN_HEIGHT/2 / self.scale

                # 5 - scroll down
                if event.button == 5:
                    old_scale = self.scale
                    # mouse_pos = pygame.mouse.get_pos()

                    self.scale /= 2
                    # if SCALE <= 0.25: SCALE = 0.25
                    if self.scale <= 0.125: self.scale = 0.125

                    if old_scale - self.scale:
                        # OFFSET_HORIZONTAL -= mouse_pos[0] / old_scale - WIN_WIDTH/2 / SCALE
                        # OFFSET_VERTICAL -= mouse_pos[1] / old_scale - WIN_HEIGHT/2 / SCALE
                        self.offset_horizontal -= WIN_WIDTH/2 / old_scale - WIN_WIDTH/2 / self.scale
                        self.offset_vertical -= WIN_HEIGHT/2 / old_scale - WIN_HEIGHT/2 / self.scale


            # keys that can be pressed only ones
            if event.type == pygame.KEYDOWN:
                # pause
                if event.key == pygame.K_SPACE:
                    if self.pause: self.pause = False
                    else: self.pause = True
                # center
                if event.key == pygame.K_c:
                    self.scale = 1
                    self.offset_horizontal, self.offset_vertical = center_view_on_commander(self.dict_with_units, self.scale, self.player_id)
                # show extra data
                if event.key == pygame.K_m:
                    if self.show_extra_data: self.show_extra_data = False
                    else: self.show_extra_data = True
                # show movement target
                if event.key == pygame.K_q:
                    if self.show_movement_target: self.show_movement_target = False
                    else: self.show_movement_target = True
                # show HP bars
                if event.key == pygame.K_h:
                    if self.show_hp_bars: self.show_hp_bars = False
                    else: self.show_hp_bars = True
                # cheat/debuging tool - give extra energy
                if event.key == pygame.K_g:
                    self.dict_with_game_state["list_with_energy"][self.player_id] += 100000

    # keys that can be pressed multiple times
        # move
        move_speed = 5 / self.scale
        # move left
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.offset_horizontal += move_speed
        # move right
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.offset_horizontal -= move_speed
        # move up
        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            self.offset_vertical += move_speed
        # move down
        if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            self.offset_vertical -= move_speed
        

    def update(self):
    # game logic for the scene

        self.current_frame += 1
        if self.current_frame == FRAMERATE:
            self.current_frame = 0

            # calculate energy
            if not self.pause:
                calculate_energy(self.dict_with_game_state)
                calculate_score(self.dict_with_game_state, self.dict_with_units)
                self.player_energy_text.set_text("E: %d" % self.dict_with_game_state["list_with_energy"][self.player_id])

            # print debug infos
            print_infos_about_view_position(self.offset_horizontal, self.offset_vertical, self.scale)
            print_infos_about_amount_of_objects(self.dict_with_game_state, self.dict_with_units, self.list_with_bullets, self.list_with_windows)
            print_infos_about_players(self.dict_with_game_state)

    # run the simulation
        if not self.pause:
            # life-cycles of units AI
            for unit_id in self.dict_with_units:
                self.dict_with_units[unit_id].AI_run(self.map, self.dict_with_game_state, self.dict_with_units)

            # life-cycles of bullets
            for bullet in self.list_with_bullets:
                bullet.run(self.map, self.dict_with_units)

            # life-cycles of units
            for unit_id in self.dict_with_units:
                self.dict_with_units[unit_id].run(self.map, self.dict_with_game_state, self.dict_with_units, self.list_with_bullets)

    # clear dead elements

        # dead bullets
        remove_few_dead_elements_from_list(self.list_with_bullets)

        # dead units
        remove_dead_elements_from_dict(self.dict_with_units)

        # unnecessary UI windows
        remove_few_dead_elements_from_list(self.list_with_windows)

    # add new units - move new units form self.dict_with_game_state["dict_with_new_units"] to self.dict_with_units
        self.dict_with_units |= self.dict_with_game_state["dict_with_new_units"]
        self.dict_with_game_state["dict_with_new_units"] = {}
    

    def render(self, win):
    # draw scene on the screen

        # clear screen
        win.fill(BLACK)

        # draw the map
        self.map.draw(win, self.offset_horizontal, self.offset_vertical, self.scale)

        # show extra data
        if self.show_extra_data:
            for unit_id in self.dict_with_units:
                self.dict_with_units[unit_id].draw_extra_data(win, self.offset_horizontal, self.offset_vertical, self.scale)

        # show movement target
        if self.show_movement_target:
            for unit_id in self.dict_with_units:
                if self.dict_with_units[unit_id].player_id == self.player_id:
                    self.dict_with_units[unit_id].draw_movement_target(win, self.offset_horizontal, self.offset_vertical, self.scale)

        # draw land and naval units
        for unit_id in self.dict_with_units:
            if self.dict_with_units[unit_id].unit_type == "land" or \
                        self.dict_with_units[unit_id].unit_type == "navy" or \
                        self.dict_with_units[unit_id].unit_type == "building": 
                self.dict_with_units[unit_id].draw(win, self.offset_horizontal, self.offset_vertical, self.scale)

        # draw air units
        for unit_id in self.dict_with_units:
            if self.dict_with_units[unit_id].unit_type == "air": 
                self.dict_with_units[unit_id].draw(win, self.offset_horizontal, self.offset_vertical, self.scale)

        # show HP bars
        if self.show_hp_bars and self.scale >= 1:
            for unit_id in self.dict_with_units:
                self.dict_with_units[unit_id].draw_HP(win, self.offset_horizontal, self.offset_vertical, self.scale)

        # draw bullets
        for bullet in self.list_with_bullets:
            bullet.draw(win, self.offset_horizontal, self.offset_vertical, self.scale)

    # draw UI
        # draw selection
        if self.left_mouse_button_down:
            unit_selection(win, self.dict_with_units, self.left_mouse_button_coord, 
                           pygame.mouse.get_pos(), self.offset_horizontal, self.offset_vertical, self.scale, -1)
        else:
            make_windows_from_dict_with_units(self.dict_with_units, self.list_with_windows)

        # draw UI windows
        for ui_win in self.list_with_windows:
            ui_win.draw(win, self.dict_with_game_state, self.dict_with_units)

        # draw infos about players
        draw_infos_about_players(win, self.dict_with_game_state)

        # draw player's energy
        self.player_energy_text.draw(win)

        # draw pause
        if self.pause:
            self.pause_text.draw(win)


# ======================================================================


class TemplateScene(SceneBase):
    def __init__(self):
    # initialization of the scene
        SceneBase.__init__(self)
    
    def process_input(self, events, keys_pressed):
    # receive all the events that happened since the last frame
    # handle all received events
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # move to the next scene when the user pressed Enter
                self.switch_scene(GameScene())
        
    def update(self):
    # game logic for the scene
        pass
    
    def render(self, win):
    # draw scene on the screen
        win.fill(HOTPINK)