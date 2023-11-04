import pygame

from settings import *
from setup import *
# from functions_graphics import *
# from functions_make_units import *
# from functions_test import *
# from functions_windows import *
# from functions_other import *
from classes_scenes_features import *
# from classes_map import *
# from classes_units import *
# from classes_buildings import *
# from classes_ui import *
# from classes_base import *


class SceneBase:
    def __init__(self):
    # initialization of the scene
        self.next = self
    
    def process_input(self, events, pressed_keys):
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
    
    def process_input(self, events, pressed_keys):
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
                    self.switch_scene(GameScene())

            # mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_coord = pygame.mouse.get_pos()
                # quick start
                if self.quick_start_button.is_inside(mouse_coord):
                    self.switch_scene(GameScene())
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

    
    def process_input(self, events, pressed_keys):
    # receive all the events that happened since the last frame
    # handle all received events
        for event in events:
            # keys that can be pressed only ones
            if event.type == pygame.KEYDOWN:
                # move to the next scene
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.switch_scene(GameScene())

            # mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_coord = pygame.mouse.get_pos()
                # move to the next scene
                if self.start_button.is_inside(mouse_coord):
                    self.switch_scene(GameScene())
                
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

# ======================================================================

class GameScene(SceneBase):
    def __init__(self):
    # initialization of the scene
        SceneBase.__init__(self)
    
    def process_input(self, events, pressed_keys):
    # receive all the events that happened since the last frame
    # handle all received events
        pass
        
    def update(self):
    # game logic for the scene
        pass
    
    def render(self, win):
    # draw scene on the screen
        win.fill(RED)

# ======================================================================

class TemplateScene(SceneBase):
    def __init__(self):
    # initialization of the scene
        SceneBase.__init__(self)
    
    def process_input(self, events, pressed_keys):
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