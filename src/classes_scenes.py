import pygame

class SceneBase:
    def __init__(self):
        self.next = self
        print("init base")
    
    def process_input(self, events, pressed_keys):
    # receive all the events that happened since the last frame
    # handle all received events
        print("not overwritten process_input")

    def update(self):
    # game logic for the scene
        print("not overwritten update")

    def render(self, screen):
    # draw scene on the screen
        print("not overwritten render")

    def switch_scene(self, next_scene):
        self.next = next_scene
    
    def terminate(self):
        self.switch_scene(None)

# ======================================================================

class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        print("init title")
    
    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # move to the next scene when the user pressed Enter
                self.switch_scene(ChooseMapScene())
    
    def update(self):
        pass
    
    def render(self, screen):
        screen.fill((255, 0, 0)) # red

# ======================================================================

class ChooseMapScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        print("init choose map")
    
    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # move to the next scene when the user pressed Enter
                self.switch_scene(GameScene())
    
    def update(self):
        pass
    
    def render(self, screen):
        screen.fill((0, 255, 0)) # green

# ======================================================================

class GameScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        print("init game")
    
    def process_input(self, events, pressed_keys):
        pass
        
    def update(self):
        pass
    
    def render(self, screen):
        screen.fill((0, 0, 255)) # blue