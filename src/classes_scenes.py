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
        self.start_button = AdvancedButton((WIN_WIDTH/2, WIN_HEIGHT/2 + 100), "[Prepare Game]", 30, color=GRAY)
        self.quick_start_button = AdvancedButton((WIN_WIDTH/2, WIN_HEIGHT/2 + 150), "[Quick Start]", 30, color=GRAY)
        self.exit_button = AdvancedButton((WIN_WIDTH/2, WIN_HEIGHT/2 + 200), "[Exit]", 30, color=GRAY)
        self.seconds_since_start = 0
        self.current_frame = 0

        # setup for animation of battle
        self.map = Map(10, 10, clean=True)
        self.dict_with_units = {}
        self.list_with_bullets = []
        self.dict_with_game_state = {
            "lowest_free_id": 1,
            "list_with_player_type": [False, "AI", "AI", "AI", "AI"],
        }
    
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
                # exit
                elif self.exit_button.is_inside(mouse_coord):
                    self.terminate()
                # move to the next scene
                else:
                    self.switch_scene(ChooseMapScene())

    def update(self):
    # game logic for the scene
        # check hovering of the mouse
        mouse_coord = pygame.mouse.get_pos()
        self.start_button.check_hovering(mouse_coord)
        self.quick_start_button.check_hovering(mouse_coord)
        self.exit_button.check_hovering(mouse_coord)

        self.current_frame += 1
        if self.current_frame == FRAMERATE:
            self.current_frame = 0
            self.seconds_since_start += 1
            # make more units
            make_more_units_for_title_scene(self.map, self.dict_with_game_state, self.dict_with_units)
            # print debug infos
            print_infos_about_amount_of_objects(self.dict_with_game_state, self.dict_with_units, self.list_with_bullets, [])

        # run the simulation
        if self.seconds_since_start > 4:
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
    
    def render(self, win):
    # draw scene on the screen
        # clear screen
        win.fill(BLACK)

        # draw animation
        # draw air units
        for unit_id in self.dict_with_units:
            self.dict_with_units[unit_id].draw(win, 0, 0, 1)
        # draw bullets
        for bullet in self.list_with_bullets:
            bullet.draw(win, 0, 0, 1)

        # print titles and buttons
        self.title.draw(win)
        self.subtitle.draw(win)
        if self.seconds_since_start > 2:
            self.start_button.draw(win)
            self.quick_start_button.draw(win)
            self.exit_button.draw(win)


# ======================================================================


class ChooseMapScene(SceneBase):
    def __init__(self):
    # initialization of the scene
        SceneBase.__init__(self)
        self.title = FixText((WIN_WIDTH/2, 60), "Choose map", 50)
        # self.start_button = AdvancedButton((WIN_WIDTH/2, WIN_HEIGHT - 75), "[Start Game]", 30, color=GRAY)
        self.start_button = AdvancedButton((WIN_WIDTH/2, WIN_HEIGHT - 75), "[Next]", 30, color=LIME, color_hover=LIME, width=WIN_WIDTH/2 + 360)

        self.list_with_maps = ["island", "mars_poles", "mars_plain", "grass_plain", "snow_plain"] # "lake", "bridge", "noise", "concrete_floor"]
        self.list_with_buttons = []
        for i, map in enumerate(self.list_with_maps):
            self.list_with_buttons.append(AdvancedButton((WIN_WIDTH/4, 150 + 50*i), "["+map.replace("_", " ").capitalize()+"]", 30, color=GRAY, option=map))
        # set first map as active as default
        global GAME_MAP
        GAME_MAP = self.list_with_maps[0]
        self.list_with_buttons[0].active = True

        # initialize map
        self.map = Map_v2(25, 32, type=self.list_with_maps[0], tile_edge_length=10, clean=True)

    def process_input(self, events, keys_pressed):
    # receive all the events that happened since the last frame
    # handle all received events
        global GAME_MAP
        for event in events:
            # keys that can be pressed only ones
            if event.type == pygame.KEYDOWN:
                # move to the next scene
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.switch_scene(ChooseSizeScene())

            # mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_coord = pygame.mouse.get_pos()
                # move to the next scene
                if self.start_button.is_inside(mouse_coord):
                    self.switch_scene(ChooseSizeScene())
                # choose map
                for button in self.list_with_buttons:
                    if button.check_pressing(mouse_coord):
                        self.map = Map_v2(25, 32, type=button.option, tile_edge_length=10, clean=True)
                        GAME_MAP = button.option
     
    def update(self):
    # game logic for the scene
        # check hovering of the mouse
        mouse_coord = pygame.mouse.get_pos()
        self.start_button.check_hovering(mouse_coord)
        for button in self.list_with_buttons:
            button.check_hovering(mouse_coord)
    
    def render(self, win):
    # draw scene on the screen
        # clear screen
        win.fill(BLACK)
        # print titles and buttons
        self.title.draw(win)
        self.start_button.draw(win)
        for button in self.list_with_buttons:
            button.draw(win)
        # draw the map
        self.map.draw(win, WIN_WIDTH/2 + 80, 120, 1)


# ======================================================================


class ChooseSizeScene(SceneBase):
    def __init__(self):
    # initialization of the scene
        SceneBase.__init__(self)
        self.start_button = AdvancedButton((WIN_WIDTH/2, WIN_HEIGHT - 75), "[Next]", 30, color=LIME, color_hover=LIME, width=WIN_WIDTH/2 + 300) # + 360

        # create groups of buttons for shape and size
        self.title_shape = FixText((WIN_WIDTH/2, 60), "Choose shape", 50)
        self.shape_button_groups = [
                AdvancedButton((WIN_WIDTH/4, 150), "[Horizontal]", 30, color=GRAY, option="horizontal", width=300),
                AdvancedButton((WIN_WIDTH/2, 150), "[Vertical]", 30, color=GRAY, option="vertical", width=300),
                AdvancedButton((WIN_WIDTH/4 + WIN_WIDTH/2, 150), "[Square]", 30, color=GRAY, option="square", width=300),
        ]
        self.title_size = FixText((WIN_WIDTH/2, 260), "Choose size", 50)
        self.size_button_groups = [
                AdvancedButton((WIN_WIDTH/4, 350), "[Small]", 30, color=GRAY, option="S", width=300),
                AdvancedButton((WIN_WIDTH/2, 350), "[Medium]", 30, color=GRAY, option="M", width=300),
                AdvancedButton((WIN_WIDTH/4 + WIN_WIDTH/2, 350), "[Large]", 30, color=GRAY, option="L", width=300),
        ]
        # set default - large vertical
        self.size_button_groups[2].active = True
        self.shape_button_groups[0].active = True
        self.save_choices_to_global()

    def process_input(self, events, keys_pressed):
    # receive all the events that happened since the last frame
    # handle all received events
        for event in events:
            # keys that can be pressed only ones
            if event.type == pygame.KEYDOWN:
                # move to the next scene
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.save_choices_to_global()
                    self.switch_scene(ChoosePlayersScene())

            # mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_coord = pygame.mouse.get_pos()
                # move to the next scene
                if self.start_button.is_inside(mouse_coord):
                    self.save_choices_to_global()
                    self.switch_scene(ChoosePlayersScene())
                # press shape buttons
                if any(button.is_inside(mouse_coord) for button in self.shape_button_groups):
                    for button in self.shape_button_groups:
                        button.check_pressing(mouse_coord)
                # press size buttons
                if any(button.is_inside(mouse_coord) for button in self.size_button_groups):
                    for button in self.size_button_groups:
                        button.check_pressing(mouse_coord)

    def update(self):
    # game logic for the scene
        # check hovering over buttons
        mouse_coord = pygame.mouse.get_pos()
        self.start_button.check_hovering(mouse_coord)
        for button in self.shape_button_groups:
            button.check_hovering(mouse_coord)
        for button in self.size_button_groups:
            button.check_hovering(mouse_coord)

    def render(self, win):
    # draw scene on the screen
        # clear screen
        win.fill(BLACK)
        # print titles and buttons
        self.title_shape.draw(win)
        self.title_size.draw(win)
        for button in self.shape_button_groups:
            button.draw(win)
        self.start_button.draw(win)
        for button in self.size_button_groups:
            button.draw(win)

    def save_choices_to_global(self):
    # save chosen options to global values
        global GAME_SIZE
        for button in self.size_button_groups:
            if button.active: GAME_SIZE = button.option


# ======================================================================


class ChoosePlayersScene(SceneBase):
    def __init__(self):
    # initialization of the scene
        SceneBase.__init__(self)
        self.title = FixText((WIN_WIDTH/2, 60), "Select Players", 50)
        self.start_button = AdvancedButton((WIN_WIDTH/2, WIN_HEIGHT - 75), "[Start Game]", 30, color=LIME, color_hover=LIME, width=WIN_WIDTH/2 + 200) #  + 360
        self.map = Map_v2(25, 32, type=GAME_MAP, tile_edge_length=10, clean=True)

        # create groups of buttons for each player
        self.players_button_groups = []
        for i in range(0,4):
            self.players_button_groups.append([
                AdvancedButton((WIN_WIDTH/4 + i//2*WIN_WIDTH/2, 150 + i%2*300), "[Player]", 30, color=GRAY, color_active=player_color(i+1), option="player", width=200),
                AdvancedButton((WIN_WIDTH/4 + i//2*WIN_WIDTH/2, 150 + i%2*300 + 50), "[AI]", 30, color=GRAY, color_active=player_color(i+1), option="AI", width=200),
                AdvancedButton((WIN_WIDTH/4 + i//2*WIN_WIDTH/2, 150 + i%2*300 + 100), "[None]", 30, color=GRAY, color_active=player_color(i+1), option="empty", width=200),
            ])

        # set default - player no 3 (index = 2) as the Player and the rest as AI
        for group in self.players_button_groups:
            group[1].active = True
        self.players_button_groups[2][0].active = True
        self.players_button_groups[2][1].active = False
        self.save_choices_to_global()
        
    def process_input(self, events, keys_pressed):
    # receive all the events that happened since the last frame
    # handle all received events
        for event in events:
            # keys that can be pressed only ones
            if event.type == pygame.KEYDOWN:
                # move to the next scene
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.save_choices_to_global()
                    self.switch_scene(LoadingScene())

            # mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_coord = pygame.mouse.get_pos()
                # move to the next scene
                if self.start_button.is_inside(mouse_coord):
                    self.save_choices_to_global()
                    self.switch_scene(LoadingScene())
                # choose type of players
                for group in self.players_button_groups:
                    if any(button.is_inside(mouse_coord) for button in group):
                        for button in group:
                            button.check_pressing(mouse_coord)

    def update(self):
    # game logic for the scene
        # check hovering of the mouse
        mouse_coord = pygame.mouse.get_pos()
        self.start_button.check_hovering(mouse_coord)
        # check hovering over buttons
        for group in self.players_button_groups:
            for button in group:
                button.check_hovering(mouse_coord)

    def render(self, win):
    # draw scene on the screen
        # clear screen
        win.fill(BLACK)
        # print titles and buttons
        self.title.draw(win)
        self.start_button.draw(win)
        # draw the map
        self.map.draw(win, WIN_WIDTH/2 - self.map.map_sprite_width_world//2, 120, 1)
        # draw groups of buttons
        for group in self.players_button_groups:
            for button in group:
                button.draw(win)

    def save_choices_to_global(self):
    # save chosen options to global values
        global GAME_PLAYERS
        for i, group in enumerate(self.players_button_groups):
            for button in group:
                if button.active:
                    GAME_PLAYERS[i] = button.option


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